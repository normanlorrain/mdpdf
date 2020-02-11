import fitz

# _BASE14 = fitz.Base14_fontdict

# Font attribute names
NAME = "fontname"
SIZE = "fontsize"
INDENT = "indent"
STRONG = "bold"
EMPHASIS = "italic"


COURIER = "cour"
TIMES = "tiro"
HELVETICA = "helv"
SYMBOL = "symb"
ZAPFDINGBATS = "zadb"

_BOLD = "bo"
_ITALIC = "it"
BOLD_ITALIC = "bi"


class Base14:
    def __init__(self, name):
        if name not in [COURIER, TIMES, HELVETICA, SYMBOL, ZAPFDINGBATS]:
            raise Exception("not valid Base14")

        self._name = name
        self._bold = False
        self._italic = False

    # def setModifier(self):
    #     if self._root not in [COURIER, TIMES, HELVETICA]:
    #         return  # TODO: raise?  symbol and zapf don't have modifiers
    #     if self._bold and self._italic:
    #         self._name = self._name[:2] + BOLD_ITALIC
    #     elif self._bold:
    #         self._name = self._name[:2] + _BOLD
    #     elif self._italic:
    #         self._name = self._name[:2] + _ITALIC
    #     else:
    #         self._name = self._root

    def setItalic(self, state):
        self._italic = state
        # self.setModifier()

    def setBold(self, state):
        self._bold = state
        # self.setModifier()

    @property
    def name(self):
        if self._name in [ZAPFDINGBATS, SYMBOL]:
            return self._name
        if self._name not in [COURIER, TIMES, HELVETICA]:
            return  # TODO: raise?  symbol and zapf don't have modifiers
        if self._bold and self._italic:
            name = self._name[:2] + BOLD_ITALIC
        elif self._bold:
            name = self._name[:2] + _BOLD
        elif self._italic:
            name = self._name[:2] + _ITALIC
        else:
            name = self._name
        return name
