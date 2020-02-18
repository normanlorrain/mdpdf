#


class Base:
    enabled = False

    @classmethod
    def setFmt(cls, fmt):
        cls._left, cls._mid, cls._right = fmt.split(",")
        cls.enabled = True

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
