# inspired from
# https://github.com/readthedocs/commonmark.py/blob/master/commonmark/render/html.py
# https://github.com/readthedocs/commonmark.py/blob/master/commonmark/render/renderer.py

import re
from builtins import str
import fitz
from pathlib import Path


from . import log
from . import style
from . import font
from . import properties
from .headfoot import Header, Footer


fontSize = 10  # choose font size of text
headingfontSizes = [18, 16, 14, 12, 10, 10, 10, 10]
lineheight = fontSize * 1.2  # line height is 20% larger
margin = 72

# For images, we are looking for a pattern in the alt text,
# e.g. Some text { width =31% }
# grab the number for image scale, and grab the remainder for the caption.
# This should be "compatible" with other Markdown variants.
# e.g. Pandoc uses alt text for image caption.
imageWidthRe = re.compile(r"(.*){.*width\s*=\s*(\d+)%.*}")
# https://regex101.com/r/8zgA9P/2


class PdfRenderer:
    def __init__(self, pdf):
        self.list_data = list()  # to store the states of ordered/unordered list
        # TODO: put this in render() Directory containing markdown (and images)
        self.indir = None
        self.pdf = pdf
        self.doc = fitz.open()
        self.toc = []
        self.currentPage = None

        global width, height
        width, height = fitz.paper_size(properties.paperSize)  # choose paper format

    def __del__(self):

        # Close the file.  If an exception occured, the attribute might not be present,
        # so check first.
        if hasattr(self, "doc"):
            # If still None, we haven't processed an ast
            if self.doc.page_count:
                for i in range(len(self.toc)):
                    log.debug(f"{i}, {self.toc[i]}")
                try:
                    self.doc.set_toc(self.toc)
                except ValueError as e:
                    log.exception("Bad heading level.  More information:")
                    lastspace = str(e).rfind(" ")
                    log.info(self.toc[int(str(e)[lastspace:])])
                self.doc.set_metadata(properties.document)
                try:
                    self.doc.save(str(self.pdf), garbage=4, deflate=True)
                except RuntimeError as e:
                    log.exception(e)
                self.doc.close()
            else:
                log.info("No pages to save")

    def render(self, ast, inputFile):
        self.infile = Path(inputFile).absolute()
        self.indir = Path(inputFile).parent.resolve()
        for node, entering in ast.walker():
            getattr(self, node.t)(node, entering)

        return

    def escape(self, text):
        return text

    def tag(self, name, attrs=None, selfclosing=None):
        return

    def text(self, node, entering=None):
        # TODO: what to do with text in image "alt" field?
        # we are currently using it for non-standard "width"
        # and remaining text could be printed.  For now, drop it.
        if node.parent is not None:
            if node.parent.t == "image":
                self.cr("caption")
                self.printCentre(node.literal)
                self.cr("caption")
                return
        line = node.literal
        self.printLine(line)

    # print a line that may break
    def printLine(self, line):
        sty = style.currentStyle()
        fontName = sty.font.name
        fontSize = sty.fontsize
        lineWidth = fitz.get_text_length(line, fontName, fontSize)
        budget = width - margin - self.indent - self.insertPoint.x
        if lineWidth < budget:
            self.printSegment(line)
        else:
            prefix = line
            suffix = line
            while True:
                index = line.rfind(" ", 0, len(prefix))
                if index == -1:  # No spaces found.  Print it on the next line
                    self.cr(chr(0xAC))
                    self.printSegment(suffix)
                    break
                prefix = line[:index]
                prefixWidth = fitz.get_text_length(
                    prefix, fontname=fontName, fontsize=fontSize
                )
                if prefixWidth > budget:  # Still too large.  Chop again.
                    continue
                else:
                    self.printSegment(prefix)
                    suffix = line[index + 1 :]
                    # Recurse for the remainder.  It might be too long as well.
                    self.cr(chr(0xAC))
                    self.printLine(suffix)
                    break

    # Softbreaks are just CRs in the input, within paragraph
    # it becomes a space.
    def softbreak(self, node=None, entering=None):
        sty = style.currentStyle()
        fontName = sty.font.name
        fontSize = sty.fontsize
        lineWidth = fitz.get_text_length(" ", fontname=fontName, fontsize=fontSize)
        budget = width - margin - self.insertPoint.x
        if lineWidth < budget:
            self.printSegment(" ")
        else:
            pass  # We're about to to a hard break anyway.
        # self.currentPage.insertText(self.insertPoint, " ", fontSize=fontSize)
        # self.insertPoint.x += fitz.get_text_length(" ", fontSize=fontSize)

    def linebreak(self, node=None, entering=None):
        self.cr("linebreak")

    def link(self, node, entering):
        if entering:
            self.linkDestination = node.destination  # TODO: deal with "#fragments"
        else:
            # the link on the page can be split over several words & lines
            # So we need to create the clickable areas.

            if ":" in self.linkDestination:
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
                    self.currentPage.insert_link(newLink)
                self.linkRects.clear()
            else:
                filename = Path(self.indir) / self.linkDestination
                try:

                    # This is ugly but whatever
                    pin = fitz.Point(
                        self.insertPoint.x, self.insertPoint.y - lineheight
                    )
                    self.currentPage.add_file_annot(
                        pin,
                        buffer=open(filename, mode="rb").read(),
                        # This goes in Description  TODO: file issue with PyMuPDF
                        filename=node.first_child.literal,
                        ufilename=filename.name,
                        # Not working.  See TODO: file issue with PyMuPDF
                        desc="deschere",
                        icon="Paperclip",
                    )

                    # This doesn't work but keeping as comments for future reference.
                    # (Linking to an embedded PDF only works on PDF >= 1.6)
                    # rc = self.doc.embeddedFileAdd(
                    #     self.linkDestination,  # entry identifier
                    #     buffer=open(filename, mode="rb").read(),
                    #     filename="NLTEST",  # Optional
                    #     desc=node.first_child.literal,  # Optional
                    # )
                    # for rect in self.linkRects:
                    #     newLink = {
                    #         "kind": fitz.LINK_GOTO,  # See PyMuPDF 6.11.2
                    #         "from": rect,  # the area on the page that is "clickable"
                    #         "page": 1,
                    #         # "to": , # For LINK_GOTOR, defaults to Point(0,0), OK
                    #         "file": self.linkDestination,
                    #         # "uri": None,  # Only for URI, otherwise ignored
                    #         # "xref": None,  # OK
                    #     }
                    #     self.currentPage.insertLink(newLink)

                except FileNotFoundError as err:
                    self.markdownError(node, f"{node.destination}: {err.strerror}")

            self.linkDestination = None

    def findSource(self, node):
        if node.sourcepos:
            return node.sourcepos[1][0]
        else:
            return self.findSource(node.parent)

    def markdownError(self, node, msg):
        log.error(f"{self.infile}:{self.findSource(node)}: {msg}")

    def image(self, node, entering):
        from . import image

        if entering:
            # TODO: consider using the alt attribute to pass the rectangle
            # dimensions/alignment/etc. https://www.w3schools.com/tags/att_img_alt.asp
            # This means the next node would need to be "peaked" at, since that's how
            # commonmark parses it.
            # Also, the text callback would have to check if it's the child of an
            # image node, OR, this function would
            # jump to the next next child somehow (return??  ) /TODO

            try:
                widthAvailable = width - 2 * margin
                imagefile = Path(self.indir) / node.destination
                imageW, imageH = image.get_image_size(str(imagefile))
                log.debug(f"{imagefile}, {imageW}, {imageH}")
                imageRatio = imageW / imageH
                rectWidth, rectHeight = imageW, imageH  # default w,h

                # Use all available width if desired, otherwise centre image.
                if rectWidth > widthAvailable:
                    rectWidth = widthAvailable
                    rectHeight = rectWidth / imageRatio
                    rect = fitz.Rect(
                        self.insertPoint,
                        width - margin,
                        self.insertPoint.y + rectHeight,
                    )
                else:
                    self.insertPoint.x = (width - rectWidth) / 2
                    rect = fitz.Rect(
                        self.insertPoint,
                        self.insertPoint.x + rectWidth,
                        self.insertPoint.y + rectHeight,
                    )

                # If the alt field (next node) has width specified, use it
                # This is the width of the image relative to printable area
                if node.first_child:
                    desiredWidth = imageWidthRe.match(node.first_child.literal)
                    if desiredWidth:
                        node.first_child.literal = imageWidthRe.sub(
                            desiredWidth.group(1), node.first_child.literal
                        )
                        rectScale = float(desiredWidth.group(2)) / 100
                        rectWidth = widthAvailable * rectScale
                        rectHeight = rectWidth / imageRatio
                        self.insertPoint.x = (width - rectWidth) / 2
                        rect = fitz.Rect(
                            self.insertPoint,
                            self.insertPoint.x + rectWidth,
                            self.insertPoint.y + rectHeight,
                        )

                # If we're running out of room start a new page
                if rectHeight > height - margin - self.insertPoint.y:
                    self.newPage()
                    self.insertPoint.x = (width - rectWidth) / 2
                    rect = fitz.Rect(
                        self.insertPoint,
                        self.insertPoint.x + rectWidth,
                        self.insertPoint.y + rectHeight,
                    )

                self.currentPage.insert_image(
                    rect, filename=str(imagefile), keep_proportion=True
                )
                self.insertPoint.y += rectHeight
            except FileNotFoundError as err:
                self.markdownError(node, f"{node.destination}: {err.strerror}")

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
                    # if grandparent.list_data["tight"]:
                    # TODO maybe deal with tight/loose lists
                    return
            self.crHalfLine("paragraphhalf+")
        else:
            # if node.parent.parent is None:  #
            #     self.cr("p-")
            # elif node.parent.parent.t == "list":
            self.cr("p-")

    def heading(self, node, entering):
        global fontSize

        if not hasattr(node.first_child, "literal"):
            self.markdownError(node, "Empty heading")
            return

        if entering:
            style.push(fontname=font.HELVETICA, fontsize=headingfontSizes[node.level])
            lineheight = style.currentStyle().lineheight
            if self.insertPoint.y > margin + lineheight:
                self.cr("H+")
            if node.level == 1:
                properties.setSection(node.first_child.literal)
        else:
            self.toc.append(
                [
                    node.level,
                    node.first_child.literal,
                    self.doc.page_count,
                    self.insertPoint.y - headingfontSizes[node.level],
                ]
            )
            self.cr("H-")
            style.pop()
            lineheight = style.currentStyle().lineheight

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
        shape = self.currentPage.new_shape()
        shape.draw_line(pntFrom, pntTo)
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
        if entering:
            if self.list_data[-1]["type"] == "ordered":
                self.printSegment(f" {node.list_data['start']} ")
            else:
                style.push(fontname=font.ZAPFDINGBATS)
                self.printSegment("l")  # Bullet:
                #  https://help.adobe.com/en_US/framemaker/2015/using/using-framemaker-2015/Appendix/frm_character_sets_cs/frm_character_sets_cs-5.htm
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
        lineheight = style.currentStyle().lineheight

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
        lineWidth = fitz.get_text_length(line, fontname=fontName, fontsize=fontSize)

        # self.currentPage.insertText(
        #     self.insertPoint,
        #     str(self.insertPoint.x),
        #     fontname="cobo",
        #     fontsize=fontSize * 2,
        # )
        log.debug(f"printSegment: {line}")
        self.currentPage.insert_text(
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

            self.currentPage = self.doc.new_page(-1, width, height)
            style.push(fontname=font.TIMES, fontsize=10, indent=0)
        else:
            self.finishPage()
            style.pop()  # We should be done anyway

    def finishPage(self):
        link = self.currentPage.first_link
        while link:
            link.setBorder({"width": 0.5, "style": "U"})
            link = link.next

        # Generate Header and Footer
        properties.page = self.doc.page_count

        style.push(fontname=font.HELVETICA, fontsize=8, indent=0)
        if Header.enabled:
            self.insertPoint.y = margin / 2 + lineheight / 2
            left = Header.left(properties)
            middle = Header.mid(properties)
            right = Header.right(properties)
            self.printLeft(left)
            self.printCentre(middle)
            self.printRight(right)

            pntFrom = fitz.Point(margin, 0.75 * margin)
            pntTo = fitz.Point(width - margin, 0.75 * margin)
            self.currentPage.draw_line(pntFrom, pntTo, width=1)

        if Footer.enabled:
            self.insertPoint.y = height - (margin / 2) + lineheight / 2
            left = Footer.left(properties)
            middle = Footer.mid(properties)
            right = Footer.right(properties)
            self.printLeft(left)
            self.printCentre(middle)
            self.printRight(right)

            pntFrom = fitz.Point(margin, height - (0.75 * margin))
            pntTo = fitz.Point(width - margin, height - (0.75 * margin))
            self.currentPage.draw_line(pntFrom, pntTo, width=1)
        style.pop()

    def newPage(self):
        self.finishPage()
        self.currentPage = self.doc.new_page(-1, width, height)
        self.insertPoint = fitz.Point(margin + self.indent, margin + lineheight)

    def printLeft(self, line):
        sty = style.currentStyle()
        self.insertPoint.x = margin
        self.currentPage.insert_text(
            self.insertPoint, line, fontname=sty.font.name, fontsize=sty.fontsize
        )

    def printCentre(self, line):
        sty = style.currentStyle()
        lineWidth = fitz.get_text_length(
            line, fontname=sty.font.name, fontsize=sty.fontsize
        )
        self.insertPoint.x = width / 2 - lineWidth / 2
        self.currentPage.insert_text(
            self.insertPoint, line, fontname=sty.font.name, fontsize=sty.fontsize
        )

    def printRight(self, line):
        sty = style.currentStyle()
        lineWidth = fitz.get_text_length(
            line, fontname=sty.font.name, fontsize=sty.fontsize
        )
        self.insertPoint.x = width - margin - lineWidth
        self.currentPage.insert_text(
            self.insertPoint, line, fontname=sty.font.name, fontsize=sty.fontsize
        )
