import fitz
import datetime

# This dict is specific to pyMuPDF.
# Keys can only be : format, encryption, title, author, subject, keywords, creator, producer, creationDate, modDate

document = {
    "creationDate": fitz.get_pdf_now(),  # current timestamp
    "modDate": fitz.get_pdf_now(),  # current timestamp
    "creator": "Python mdfpdf package: https://pypi.org/project/mdpdf",
    "producer": "PyMuPDF library: https://pypi.org/project/PyMuPDF",
    "title": None,
    "subject": None,
    "author": None,
    "keywords": None,
}

# These properties are used for the header and footer
# these are available on the command-line switch --header and --footer
page = 1
heading = "some heading"
date = datetime.datetime.now().date()

paperSize = "letter"


def setPaperSize(text):
    global paperSize
    paperSize = text


def setSection(text):
    global heading
    heading = text


def setTitle(text):
    document["title"] = text


def setSubject(text):
    document["subject"] = text


def setAuthor(text):
    document["author"] = text


def setKeywords(text):
    document["keywords"] = text
