_styleList = []


def pushStyle(name, styles):
    if len(_styleList):
        cls = type(name, (_styleList[-1],), styles)
    else:
        cls = type(name, (), styles)
    _styleList.append(cls)


def popStyle():
    _styleList.pop()


def currentStyle():
    return _styleList[-1]


if __name__ == "__main__":

    pushStyle("base", {"fontName": "Helvetica", "fontSize": 12, "indent": 0})
    style = currentStyle()
    pushStyle("indend1", {"indent": 36})
    style = currentStyle()
    popStyle()
    style = currentStyle()

    pass
