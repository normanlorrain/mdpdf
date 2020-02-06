# Refer here: https://github.com/commonmark/commonmark.js

def processText(literal):
    print("Text:",literal)


def processSoftbreak(literal):
    pass


def processLinebreak(literal):
    pass


def processEmph(literal):
    pass


def processStrong(literal):
    pass


def processHtml_inline(literal):
    pass


def processLink(literal):
    pass


def processImage(literal):
    pass


def processCode(literal):
    pass


def processDocument(literal):
    pass


def processParagraph(literal):
    pass


def processBlock_quote(literal):
    pass


def processItem(literal):
    pass


def processList(literal):
    pass


def processHeading(literal):
    pass


def processCode_block(literal):
    pass


def processHtml_block(literal):
    pass


def processThematic_break(literal):
    pass


elements = {
    "text": processText,
    "softbreak": processSoftbreak,
    "linebreak": processLinebreak,
    "emph": processEmph,
    "strong": processStrong,
    "html_inline": processHtml_inline,
    "link": processLink,
    "image": processImage,
    "code": processCode,
    "document": processDocument,
    "paragraph": processParagraph,
    "block_quote": processBlock_quote,
    "item": processItem,
    "list": processList,
    "heading": processHeading,
    "code_block": processCode_block,
    "html_block": processHtml_block,
    "thematic_break": processThematic_break,
}
