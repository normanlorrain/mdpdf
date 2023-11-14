# mdpdf

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Python command line application to convert Markdown to PDF.

## Project Features

* Bare-bones: Only supports basic [CommonMark](https://commonmark.org/)
* "One-size-fits-all" style: Left-aligned, PDF-base14 fonts. Reasonably pretty, but if you want more control, see alternatives below.
* Headings are transformed to PDF bookmarks.
* File links are transformed into attachments with PDF links.
* Images links are transformed into embedded images with optional captions and width specifier.
* Minimal requirements
    - [commonmark](https://pypi.org/project/commonmark/)
    - [PyMuMDF](https://pypi.org/project/PyMuPDF/)
    - [click](https://pypi.org/project/click/)


## Alternatives
There are several projects that can be considered if you need something with more features.  Of note: 
* [pandoc](https://pandoc.org/) + [Typst](https://github.com/typst/typst)
* [pandoc](https://pandoc.org/) + [latex](https://www.latex-project.org/)
* [rst2pdf](https://github.com/rst2pdf/rst2pdf)
* [rinohtype](https://github.com/brechtm/rinohtype)
* [weasyprint](https://weasyprint.org/)


### To Investigate
* [pyfpdf](https://github.com/reingart/pyfpdf/blob/master/docs/FAQ.md)
* 
## Installation

    $ pip install mdpdf

## Usage
    $ mdpdf [OPTIONS] [INPUTS]...

### Options:
-  `-o, --output FILE       ` Destination for file output.  [required]
-  `-h, --header <template> ` Sets the header template.
-  `-f, --footer <template> ` Footer template.
-  `-t, --title TEXT        ` PDF title.
-  `-s, --subject TEXT      ` PDF subject.
-  `-a, --author TEXT       ` PDF author.
-  `-k, --keywords TEXT     ` PDF keywords.
-  `-p, --paper [letter|A4] ` Paper size (default letter).
-  `--version               ` Show the version and exit.
-  `--help                  ` Show this message and exit.

### Templates:

The `<template>` is a quoted, comma-
  delimited string, containing the left, centre,
  and right, fields for the header/footer. Format is `"[left],[middle],[right]"`.

Possible values to put here are:
- Empty string
- Arbitrary text
- Special variables:
    - `{page}` current page number
    - `{header}` current top-level body text heading
    - `{date}` current date

Example:

    $ mdpdf -o article.pdf article.md

    $ mdpdf -o article.pdf --footer "{date},{heading},{page}" article.md
