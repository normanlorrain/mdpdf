class Base:
    @classmethod
    def setFmt(self, fmt):
        self._left, self._mid, self._right = fmt.split(",")

    @classmethod
    def left(cls, m):
        return cls._left.format(**m.__dict__)

    @classmethod
    def mid(cls, m):
        return cls._mid.format(**m.__dict__)

    @classmethod
    def right(cls, m):
        return cls._right.format(**m.__dict__)


class Header(Base):
    pass


class Footer(Base):
    pass


Header.setFmt("{page},{title},{date}")
Footer.setFmt(",,")


if __name__ == "__main__":
    Header.setFmt("{date},blah,{page}")

    class MetaData(object):
        pass

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
