from . import font
import copy

_styleList = []
_styleNumber = 0


class Style:
    def __init__(self, **kwargs):
        if kwargs:
            self.setAttributes(**kwargs)

    def setAttributes(self, **kwargs):
        for var, val in kwargs.items():
            # log.info(f"{var}, {val}")
            if var == "fontname":
                self.font = font.Base14(val)
            elif var == "fontsize":
                self.fontsize = val
            elif var == "italic":
                self.font.setItalic(val)
            elif var == "bold":
                self.font.setBold(val)
            elif var == "indent":
                self.indent = val
            else:
                raise Exception("not valid Style attribute")


def push(**kwargs):
    if len(_styleList):
        newStyle = copy.deepcopy(currentStyle())
        newStyle.setAttributes(**kwargs)
    else:
        newStyle = Style(**kwargs)

    _styleList.append(newStyle)


def pop():
    global _styleNumber
    _styleNumber -= 1

    _styleList.pop()


def currentStyle():
    return _styleList[-1]


if __name__ == "__main__":

    push(fontname=font.HELVETICA, fontsize=12)
    style = currentStyle()
    push(indent=36)
    push(italic=True)
    style = currentStyle()
    pop()
    style = currentStyle()

    pass
