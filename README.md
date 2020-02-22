# mdpdf

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Python command line application to convert Markdown to PDF.

## Project Features

* Bare-bones: Only supports basic [CommonMark](https://commonmark.org/)
* *Not necessarily* beautiful: Left-aligned, PDF-base14 fonts. Reasonably pretty, but if you want more control, see alternatives below.
* Minimal requirements
    - [commonmark](https://pypi.org/project/commonmark/)
    - [PyMuMDF](https://pypi.org/project/PyMuPDF/)
    - [click](https://pypi.org/project/click/)

## Alternatives
There are several projects that can be considered if you need something with more features.  Of note: 
* [pandoc](https://pandoc.org/) + [latex](https://www.latex-project.org/)
* [rst2pdf](https://github.com/rst2pdf/rst2pdf)
* [rinohtype](https://github.com/brechtm/rinohtype)

## Installation

    $ pip install mdpdf    # TODO 

## Usage
    $ mdpdf [options] [input-file]...

Where options are:
- `-o` *output file*
- `-h` *header format*
- `-f` *footer format*

For example, specify the output file with the `-o` option:

    $ mdpdf -o article.pdf article.md

