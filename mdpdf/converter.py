import commonmark

from . import log
from .pdf_renderer import PdfRenderer


class Converter:
    def __init__(self, outputFileName):
        self.parser = commonmark.Parser()
        self.renderer = PdfRenderer(outputFileName)

    def convert(self, inputFileNames):
        for inputFile in inputFileNames:
            log.info(inputFile)
            mdFile = open(inputFile, "r", encoding="utf-8")
            entireFile = mdFile.read()
            ast = self.parser.parse(entireFile)
            self.renderer.render(ast, inputFile)
