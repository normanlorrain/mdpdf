import commonmark
import fitz  # pymupdf

from .pdf_renderer import PdfRenderer


parser = commonmark.Parser()


def convertMarkdown2Pdf(inputFileName, outputFileName):
    mdFile = open(inputFileName, "r")
    entireFile = mdFile.read()
    ast = parser.parse(entireFile)

    renderer = PdfRenderer(outputFileName)
    renderer.render(ast)
