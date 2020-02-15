class Base:
    @classmethod
    def setFmt(self, fmt):
        self._left, self._mid, self._right = fmt.split(",")

    @classmethod
    def left(cls, **metaData):
        return cls._left.format(**metaData)

    @classmethod
    def mid(cls, **metaData):
        return cls._mid.format(**metaData)

    @classmethod
    def right(cls, **metaData):
        return cls._right.format(**metaData)


class Header(Base):
    pass


class Foot(Base):
    pass


if __name__ == "__main__":
    Header.setFmt("{date},blah,{page}")

    date = "2020-02-15"
    page = 12
    header = "chapter 1"

    metaData = {"date": date, "page": page, "header": header}

    l = Header.left(**metaData)
    m = Header.mid(**metaData)
    r = Header.right(**metaData)

    metaData["page"] += 1
    r = Header.right(**metaData)

    pass
