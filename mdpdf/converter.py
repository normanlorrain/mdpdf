import commonmark
import fitz  # pymupdf

from .pdf_renderer import PdfRenderer


class Converter:
    def __init__(self, outputFileName):
        self.parser = commonmark.Parser()
        self.renderer = PdfRenderer(outputFileName)

    def convert(self, inputFile):
        mdFile = open(inputFile, "r", encoding="utf-8")
        entireFile = mdFile.read()
        ast = self.parser.parse(entireFile)
        self.renderer.render(ast)

    def convertSingle(self, inputFileName):
        self.renderer.setInputDir(inputFileName.parent)
        self.convert(inputFileName)

    def convertMultiple(inputFileNames):
        for i in inputFileNames:
            self.convert(i)


def convertMarkdown2Pdf(inputFileName, outputFileName):
    parser = commonmark.Parser()

    mdFile = open(inputFileName, "r", encoding="utf-8")
    entireFile = mdFile.read()
    ast = parser.parse(entireFile)

    renderer = PdfRenderer(outputFileName)
    renderer.setInputDir(inputFileName.parent)
    renderer.render(ast)
