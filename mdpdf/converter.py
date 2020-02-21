from pathlib import Path

import commonmark
import fitz  # pymupdf

from . import log
from .pdf_renderer import PdfRenderer


class Converter:
    def __init__(self, outputFileName):
        self.parser = commonmark.Parser()
        self.renderer = PdfRenderer(outputFileName)

    def convert(self, inputFile):
        log.info(inputFile)
        indir = Path(inputFile).parent.resolve()
        mdFile = open(inputFile, "r", encoding="utf-8")
        entireFile = mdFile.read()
        ast = self.parser.parse(entireFile)
        self.renderer.render(ast, indir)

    def convertSingle(self, inputFileName):
        self.convert(inputFileName)

    def convertMultiple(self, inputFileNames):
        for i in inputFileNames:
            self.convert(i)


def convertMarkdown2Pdf(inputFileName, outputFileName):
    parser = commonmark.Parser()

    mdFile = open(inputFileName, "r", encoding="utf-8")
    entireFile = mdFile.read()
    ast = parser.parse(entireFile)

    renderer = PdfRenderer(outputFileName)
    renderer.render(ast, inputFileName.parent)
