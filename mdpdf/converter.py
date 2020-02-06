import commonmark
import fitz  # pymupdf

from .elements import elements


parser = commonmark.Parser()


def convertMarkdown2Pdf(inputFileName, outputFileName):
    mdFile = open(inputFileName, "r")
    entireFile = mdFile.read()
    ast = parser.parse(entireFile)

    # renderer = commonmark.HtmlRenderer()
    # html = renderer.render(ast)
    # # print(html)

    # inspecting the abstract syntax tree
    # json = commonmark.dumpJSON(ast)
    # commonmark.dumpAST(ast)  # pretty print generated AST structure

    for node, entering in commonmark.node.NodeWalker(ast):
        if entering:
            elements[node.t](node.literal)
