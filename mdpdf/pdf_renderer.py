# inspired from https://github.com/readthedocs/commonmark.py/blob/master/commonmark/render/html.py

from __future__ import unicode_literals


import re
from builtins import str
import fitz
import sys

from .renderer import Renderer


reUnsafeProtocol = re.compile(r"^javascript:|vbscript:|file:|data:", re.IGNORECASE)
reSafeDataProtocol = re.compile(r"^data:image\/(?:png|gif|jpeg|webp)", re.IGNORECASE)


def potentially_unsafe(url):
    return re.search(reUnsafeProtocol, url) and (not re.search(reSafeDataProtocol, url))


width, height = fitz.PaperSize("letter")  # choose paper format
fontsz = 10  # choose font size of text
headingFontSizes = [18, 16, 14, 12]
lineheight = fontsz * 1.2  # line height is 20% larger
margin = 72

# choose a nice mono-spaced font of the system, instead of 'Courier'.
# To use a standard PDF base14 font, e.g. set font='Courier' and ffile=None
ffile = "C:/windows/fonts/consola.ttf"  # font file
font = "F0"  # fontname


class PdfRenderer(Renderer):
    def __init__(self, pdf):
        self.list_data = list()  # to store the states of ordered/unordered list
        self.pdf = pdf
        self.doc = fitz.open()
        self.currentPage = self.doc.newPage(-1, width, height)
        self.disable_tags = 0
        self.last_out = "\n"
        self.indent = 0
        self.insertPoint = fitz.Point(margin, margin + lineheight)
        self.insertRectangle = fitz.Rect(
            margin, margin + lineheight, width - margin, height - margin,
        )

    def __del__(self):
        m = {
            "creationDate": fitz.getPDFnow(),  # current timestamp
            "modDate": fitz.getPDFnow(),  # current timestamp
            "creator": "mdpdf",
            "producer": "Markdown to PDF",
            "title": "title goes here",
            "subject": "subject here",
            "author": "author here",
        }

        self.doc.setMetadata(m)
        self.doc.save(str(self.pdf), garbage=4, deflate=True)
        self.doc.close()

    def escape(self, text):
        return text

    def tag(self, name, attrs=None, selfclosing=None):
        """Helper function to produce an HTML tag."""
        if self.disable_tags > 0:
            return

        self.buf += "<" + name
        # if attrs and len(attrs) > 0:
        #     for attrib in attrs:
        #         self.buf += " " + attrib[0] + '="' + attrib[1] + '"'

        if selfclosing:
            self.buf += " /"

        self.buf += ">"
        self.last_out = ">"

    # Node methods #

    def text(self, node, entering=None):
        # TODO Word > printable area
        line = node.literal
        lineWidth = fitz.getTextlength(line, fontsize=fontsz)
        budget = width - margin - self.insertPoint.x
        if lineWidth < budget:
            self.currentPage.insertText(self.insertPoint, line, fontsize=fontsz)
            self.insertPoint.x += lineWidth
        else:
            prefix = line
            suffix = line
            while True:
                index = line.rfind(" ", 0, len(prefix))
                if index == -1:
                    break
                prefix = line[:index]
                prefixWidth = fitz.getTextlength(prefix, fontsize=fontsz)
                if prefixWidth > budget:
                    continue
                else:
                    self.currentPage.insertText(
                        self.insertPoint, prefix, fontsize=fontsz
                    )
                    self.insertPoint.x += prefixWidth

                    suffix = line[index + 1 :]
                    break
            self.cr(chr(0xAC))
            self.currentPage.insertText(self.insertPoint, suffix, fontsize=fontsz)
            self.insertPoint.x += fitz.getTextlength(suffix, fontsize=fontsz)

    # Softbreaks are just CRs in the input, within paragraph
    def softbreak(self, node=None, entering=None):
        self.currentPage.insertText(self.insertPoint, " ", fontsize=fontsz)
        self.insertPoint.x += fitz.getTextlength(" ", fontsize=fontsz)

    def linebreak(self, node=None, entering=None):
        self.cr("linebreak")

    def link(self, node, entering):
        # attrs = self.attrs(node)
        if entering:
            # if not (self.options.get("safe") and potentially_unsafe(node.destination)):
            #     attrs.append(["href", self.escape(node.destination)])

            # if node.title:
            #     attrs.append(["title", self.escape(node.title)])

            self.print(f"LINK:{node.destination}")
            # There's also a node.title attribute, not relevant to PDFs
        else:
            pass

    def image(self, node, entering):
        if entering:
            self.print(f"IMAGE:{node.destination}")
        # node.title

    def emph(self, node, entering):
        self.tag("em" if entering else "/em")

    def strong(self, node, entering):
        self.tag("strong" if entering else "/strong")

    def paragraph(self, node, entering):
        grandparent = node.parent.parent
        if grandparent is not None and grandparent.t == "list":
            if grandparent.list_data["tight"]:
                return

        if entering:
            self.crHalfLine()
        else:
            self.cr("p-")

    def heading(self, node, entering):
        global fontsz
        if entering:
            if self.insertPoint.y > margin + lineheight:
                self.cr("H+")
            fontsz += headingFontSizes[node.level]
        else:
            self.cr("H-")
            fontsz -= headingFontSizes[node.level]

    def code(self, node, entering):
        self.tag("code")
        self.out(node.literal)
        self.tag("/code")

    def code_block(self, node, entering):
        info_words = node.info.split() if node.info else []
        # # attrs = self.attrs(node)
        # if len(info_words) > 0 and len(info_words[0]) > 0:
        #     attrs.append(["class", "language-" + self.escape(info_words[0])])

        self.cr("code/")

        self.out(node.literal)

        self.cr("/code")

    def thematic_break(self, node, entering):
        # attrs = self.attrs(node)
        self.cr("tb")

    def block_quote(self, node, entering):
        # attrs = self.attrs(node)
        if entering:
            self.crHalfLine()
            self.indent += 32
            self.insertPoint.x += 32

        else:
            self.indent -= 32
            self.insertPoint.x -= 32
            self.cr("bq-")

    def list(self, node, entering):
        # node.list_data

        if entering:
            self.list_data.append(node.list_data)
            self.crHalfLine()
            self.indent += 32
            self.insertPoint.x += 32
        else:
            self.list_data.pop()
            self.indent -= 32
            self.insertPoint.x -= 32

    def item(self, node, entering):
        # attrs = self.attrs(node)
        # node.sourcepos
        if entering:
            if self.list_data[-1]["type"] == "ordered":
                self.print(f" {node.list_data['start']} ")
            else:
                self.print("\u00b7 ")
        else:
            self.cr("li-")

    def html_inline(self, node, entering):
        if self.options.get("safe"):
            self.lit("<!-- raw HTML omitted -->")
        else:
            self.lit(node.literal)

    def html_block(self, node, entering):
        self.cr("block")

        self.lit(node.literal)
        self.cr("block")

    def custom_inline(self, node, entering):
        if entering and node.on_enter:
            self.lit(node.on_enter)
        elif (not entering) and node.on_exit:
            self.lit(node.on_exit)

    def custom_block(self, node, entering):
        self.cr()
        if entering and node.on_enter:
            self.lit(node.on_enter)
        elif (not entering) and node.on_exit:
            self.lit(node.on_exit)
        self.cr()

    # Helper methods #

    def out(self, s):
        self.lit(self.escape(s))

    def cr(self, note):
        self.currentPage.insertText(self.insertPoint, note, fontsize=6)
        self.insertPoint.x = margin + self.indent
        self.insertPoint.y += lineheight
        if self.insertPoint.y > height - margin:
            self.currentPage = self.doc.newPage(-1, width, height)
            self.insertPoint = fitz.Point(margin + self.indent, margin + lineheight)

    def crHalfLine(self):
        self.insertPoint.x = margin + self.indent
        self.insertPoint.y += lineheight / 2
        if self.insertPoint.y > height - margin:
            self.currentPage = self.doc.newPage(-1, width, height)
            self.insertPoint = fitz.Point(margin + self.indent, margin + lineheight)

    def print(self, text):
        self.currentPage.insertText(self.insertPoint, text, fontsize=fontsz)
        self.insertPoint.x += fitz.getTextlength(text, fontsize=fontsz)

    def lit(self, s):
        self.print(s)
