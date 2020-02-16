# inspired from https://github.com/readthedocs/commonmark.py/blob/master/commonmark/render/html.py
# https://github.com/readthedocs/commonmark.py/blob/master/commonmark/render/renderer.py

import re
from builtins import str
import fitz
import sys
from pathlib import Path


from . import style
from . import font
from . import properties
from .headfoot import Header, Footer


width, height = fitz.PaperSize("letter")  # choose paper format
fontSize = 10  # choose font size of text
headingfontSizes = [18, 16, 14, 12, 10, 10, 10, 10]
lineheight = fontSize * 1.2  # line height is 20% larger
margin = 72


class PdfRenderer:
    def __init__(self, pdf):
        self.list_data = list()  # to store the states of ordered/unordered list
        self.indir = None  # TODO: put this in render() Directory containing markdown (and images)
        self.pdf = pdf
        self.doc = fitz.open()
        self.disable_tags = 0

    def __del__(self):

        # Close the file.  If an exception occured, the attribute might not be present,
        # so check first.
        if hasattr(self, "doc"):
            self.doc.setMetadata(properties.document)
            self.doc.save(str(self.pdf), garbage=4, deflate=True)
            self.doc.close()

    def render(self, ast, indir):
        """Walks the AST and calls member methods for each Node type.

        @param ast {Node} The root of the abstract syntax tree.
        """
        self.indir = indir
        for node, entering in ast.walker():
            getattr(self, node.t)(node, entering)

        return

    def escape(self, text):
        return text

    def tag(self, name, attrs=None, selfclosing=None):
        return

    def text(self, node, entering=None):
        # TODO Word > printable area
        line = node.literal
        self.printLine(line)

    # print a line that may break
    def printLine(self, line):
        sty = style.currentStyle()
        fontName = sty.font.name
        fontSize = sty.fontsize
        lineWidth = fitz.getTextlength(line, fontName, fontSize)
        budget = width - margin - self.indent - self.insertPoint.x
        if lineWidth < budget:
            self.printSegment(line)
        else:
            prefix = line
            suffix = line
            while True:
                index = line.rfind(" ", 0, len(prefix))
                if index == -1:
                    break
                prefix = line[:index]
                prefixWidth = fitz.getTextlength(
                    prefix, fontname=fontName, fontsize=fontSize
                )
                if prefixWidth > budget:
                    continue
                else:
                    self.printSegment(prefix)
                    suffix = line[index + 1 :]
                    break
            self.cr(chr(0xAC))
            self.printSegment(suffix)

    # Softbreaks are just CRs in the input, within paragraph
    # it becomes a space.
    def softbreak(self, node=None, entering=None):
        sty = style.currentStyle()
        fontName = sty.font.name
        fontSize = sty.fontsize
        lineWidth = fitz.getTextlength(" ", fontname=fontName, fontsize=fontSize)
        budget = width - margin - self.insertPoint.x
        if lineWidth < budget:
            self.printSegment(" ")
        else:
            pass  # We're about to to a hard break anyway.
        # self.currentPage.insertText(self.insertPoint, " ", fontSize=fontSize)
        # self.insertPoint.x += fitz.getTextlength(" ", fontSize=fontSize)

    def linebreak(self, node=None, entering=None):
        self.cr("linebreak")

    def link(self, node, entering):
        if entering:
            # style.push(fontname=font.COURIER)
            self.linkDestination = node.destination  # TODO: deal with "#fragments"
        else:
            # the link on the page can be split over several words & lines
            # So we need to create the clickable areas.
            for rect in self.linkRects:
                newLink = {
                    "kind": fitz.LINK_URI,
                    "from": rect,  # the area on the page that is "clickable"
                    "page": None,
                    "to": None,
                    "file": None,
                    "uri": self.linkDestination,
                    "xref": None,
                }
                self.currentPage.insertLink(newLink)

            self.linkDestination = None
            self.linkRects.clear()
            # style.pop()

    def image(self, node, entering):
        from . import image

        if entering:
            # TODO: consider using the alt attribute to pass the rectangle dimensions/alignment/etc. https://www.w3schools.com/tags/att_img_alt.asp
            # This means the next node would need to be "peaked" at, since that's how
            # commonmark parses it.
            # Also, the text callback would have to check if it's the child of an image node, OR, this function would
            # jump to the next next child somehow (return??  ) /TODO

            try:
                imagefile = Path(self.indir) / node.destination
                imageW, imageH = image.get_image_size(str(imagefile))
                print(imagefile, imageW, imageH)

                if imageH > height - self.insertPoint.y:
                    self.newPage()

                if imageW > (width - (2 * margin)):
                    rect = fitz.Rect(
                        self.insertPoint, width - margin, self.insertPoint.y + imageH
                    )
                else:
                    self.insertPoint.x = (width - imageW) / 2
                    rect = fitz.Rect(
                        self.insertPoint,
                        self.insertPoint.x + imageW,
                        self.insertPoint.y + imageH,
                    )
                self.currentPage.insertImage(rect, str(imagefile), keep_proportion=True)
                self.insertPoint.y += imageH
            except FileNotFoundError as err:
                print(f"{err}")
                raise  # TODO: print node/line number

        # node.title

    def emph(self, node, entering):
        if entering:
            style.push(italic=True)
        else:
            style.pop()

    def strong(self, node, entering):
        if entering:
            style.push(bold=True)
        else:
            style.pop()

    def paragraph(self, node, entering):
        if entering:
            if node.parent is not None:
                if node.parent.t == "block_quote":
                    return
            if node.parent.parent is not None:
                if node.parent.parent.t == "list":
                    # if grandparent.list_data["tight"]:  # TODO maybe deal with tight/loose lists
                    return
            self.crHalfLine("paragraphhalf+")
        else:
            # if node.parent.parent is None:  #
            #     self.cr("p-")
            # elif node.parent.parent.t == "list":
            self.cr("p-")

    def heading(self, node, entering):
        global fontSize
        if entering:
            style.push(fontname=font.HELVETICA, fontsize=headingfontSizes[node.level])
            if self.insertPoint.y > margin + lineheight:
                self.cr("H+")

        else:
            self.cr("H-")
            style.pop()

    def code(self, node, entering):
        style.push(fontname=font.COURIER)
        self.printLine(node.literal)
        style.pop()

    def code_block(self, node, entering):
        if entering:
            style.push(fontname=font.COURIER)
            self.crHalfLine("codehalf+")
            self.indent += 32
            self.insertPoint.x += 32
            for line in node.literal.split("\n"):
                if len(line):
                    self.printLine(line)
                    self.cr("")

            # else: # doesn't get called with entering = False?
            self.indent -= 32
            self.insertPoint.x -= 32
            self.crHalfLine("codehalf-")
            style.pop()

    def thematic_break(self, node, entering):
        # attrs = self.attrs(node)
        pntFrom = fitz.Point(self.insertPoint.x, self.insertPoint.y - lineheight / 2)
        pntTo = fitz.Point(width - margin, pntFrom.y)
        shape = self.currentPage.newShape()
        shape.drawLine(pntFrom, pntTo)
        shape.finish()
        shape.commit()
        self.cr("")

    def block_quote(self, node, entering):
        # attrs = self.attrs(node)
        if entering:
            self.crHalfLine("bqhalf+")
            self.indent += 32
            self.insertPoint.x += 32

        else:
            self.indent -= 32
            self.insertPoint.x -= 32
            self.crHalfLine("bqhalf-")

    def list(self, node, entering):
        # node.list_data
        if entering:
            self.list_data.append(node.list_data)
            self.crHalfLine("listhalf+")
            self.indent += 16
            self.insertPoint.x = margin + self.indent
        else:
            self.list_data.pop()
            self.crHalfLine("listhalf-")
            self.indent -= 16
            self.insertPoint.x = margin + self.indent

    def item(self, node, entering):
        # attrs = self.attrs(node)
        # node.sourcepos
        if entering:
            if self.list_data[-1]["type"] == "ordered":
                self.printSegment(f" {node.list_data['start']} ")
            else:
                style.push(fontname=font.ZAPFDINGBATS)
                self.printSegment(
                    "l"
                )  # Bullet:  https://help.adobe.com/en_US/framemaker/2015/using/using-framemaker-2015/Appendix/frm_character_sets_cs/frm_character_sets_cs-5.htm
                style.pop()
            self.indent += 16
            self.insertPoint.x = margin + self.indent

        else:
            self.indent -= 16
            self.insertPoint.x = margin + self.indent

    # From spec: Text between < and > that looks like an HTML tag is parsed
    # as a raw HTML tag and will be rendered in HTML without escaping. Tag
    # and attribute names are not limited to current HTML tags, so custom
    # tags (and even, say, DocBook tags) may be used.

    def html_inline(self, node, entering):
        self.code(node, entering)  # TODO maybe warn user?

    def html_block(self, node, entering):
        self.code_block(node, entering)  # TODO maybe warn user?

    def custom_inline(self, node, entering):
        self.code(node, entering)  # TODO maybe warn user?

    def custom_block(self, node, entering):
        self.code(node, entering)  # TODO maybe warn user?

    # Helper methods #

    def cr(self, note):
        # self.currentPage.insertText(self.insertPoint, note, fontsize=3)
        self.insertPoint.x = margin + self.indent
        self.insertPoint.y += lineheight
        if self.insertPoint.y > height - margin:
            self.newPage()

    def crHalfLine(self, note="half"):
        # self.currentPage.insertText(self.insertPoint, note, fontsize=3)
        self.insertPoint.x = margin + self.indent
        self.insertPoint.y += lineheight / 2
        if self.insertPoint.y > height - margin:
            self.newPage()

    def printSegment(self, line):
        sty = style.currentStyle()
        fontName = sty.font.name
        fontSize = sty.fontsize
        lineWidth = fitz.getTextlength(line, fontname=fontName, fontsize=fontSize)

        # self.currentPage.insertText(
        #     self.insertPoint,
        #     str(self.insertPoint.x),
        #     fontname="cobo",
        #     fontsize=fontSize * 2,
        # )
        print("printSegment", line)
        self.currentPage.insertText(
            self.insertPoint, line, fontname=fontName, fontsize=fontSize
        )
        if self.linkDestination:
            self.linkRects.append(
                fitz.Rect(
                    self.insertPoint.x,
                    self.insertPoint.y - lineheight,
                    self.insertPoint.x + lineWidth,
                    self.insertPoint.y,
                )
            )
        self.insertPoint.x += lineWidth

    def document(self, node, entering):
        if entering:
            self.indent = 0
            self.insertPoint = fitz.Point(margin, margin + lineheight)
            self.linkDestination = None
            self.linkRects = []

            self.currentPage = self.doc.newPage(-1, width, height)
            style.push(fontname=font.TIMES, fontsize=10, indent=0)
        else:
            self.finishPage()
            style.pop()  # We should be done anyway

    def finishPage(self):
        link = self.currentPage.firstLink
        while link:
            link.setBorder({"width": 0.5, "style": "U"})
            link = link.next
        self.insertPoint.y = margin / 2 + lineheight / 2
        l = Header.left(properties)
        m = Header.mid(properties)
        r = Header.right(properties)
        self.printLeft(l)
        self.printCentre(m)
        self.printRight(r)

        pntFrom = fitz.Point(margin, 0.75 * margin)
        pntTo = fitz.Point(width - margin, 0.75 * margin)
        shape = self.currentPage.newShape()
        shape.drawLine(pntFrom, pntTo)
        shape.finish()
        shape.commit()

    def newPage(self):
        self.finishPage()
        self.currentPage = self.doc.newPage(-1, width, height)
        self.insertPoint = fitz.Point(margin + self.indent, margin + lineheight)

    def printLeft(self, line):
        sty = style.currentStyle()
        fontName = sty.font.name
        fontSize = sty.fontsize / 2
        lineWidth = fitz.getTextlength(line, fontname=fontName, fontsize=fontSize)
        self.insertPoint.x = margin
        self.currentPage.insertText(
            self.insertPoint, line, fontname=fontName, fontsize=fontSize
        )

    def printCentre(self, line):
        sty = style.currentStyle()
        fontName = sty.font.name
        fontSize = sty.fontsize / 2
        lineWidth = fitz.getTextlength(line, fontname=fontName, fontsize=fontSize)
        self.insertPoint.x = width / 2 - lineWidth / 2
        self.currentPage.insertText(
            self.insertPoint, line, fontname=fontName, fontsize=fontSize
        )

    def printRight(self, line):
        sty = style.currentStyle()
        fontName = sty.font.name
        fontSize = sty.fontsize / 2
        lineWidth = fitz.getTextlength(line, fontname=fontName, fontsize=fontSize)
        self.insertPoint.x = width - margin - lineWidth
        self.currentPage.insertText(
            self.insertPoint, line, fontname=fontName, fontsize=fontSize
        )

