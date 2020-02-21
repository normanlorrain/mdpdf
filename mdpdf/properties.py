import fitz
import datetime

# This dict is specific to pyMuPDF.
# Keys can only be : format, encryption, title, author, subject, keywords, creator, producer, creationDate, modDate

document = {
    "creationDate": fitz.getPDFnow(),  # current timestamp
    "modDate": fitz.getPDFnow(),  # current timestamp
    "creator": "mdpdf",
    "producer": "mdpdf",
    "title": "title goes here",
    "subject": "subject here",
    "author": "author here",
}

# These properties are used for the header and footer
# these are available on the command-line switch --header and --footer
page = 1
heading = "some heading"
date = datetime.datetime.now().date()
title = "Doc title"
