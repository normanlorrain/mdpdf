class Base:
    @classmethod
    def setFmt(self, fmt):
        self._left, self._mid, self._right = fmt.split(",")

    @classmethod
    def left(cls, metaData):
        return cls._left.format(**metaData.__dict__)

    @classmethod
    def mid(cls, metaData):
        return cls._mid.format(**metaData.__dict__)

    @classmethod
    def right(cls, metaData):
        return cls._right.format(**metaData.__dict__)


class Header(Base):
    pass


class Foot(Base):
    pass


class MetaData(object):
    pass


if __name__ == "__main__":
    Header.setFmt("{date},blah,{page}")

    metaData = MetaData()
    metaData.date = "2020-02-15"
    metaData.page = 12
    metaData.header = "chapter 1"

    # metaData = {"date": date, "page": page, "header": header}

    l = Header.left(metaData)
    m = Header.mid(metaData)
    r = Header.right(metaData)

    metaData.page += 1
    r = Header.right(metaData)

    pass
