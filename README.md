# mdpdf

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Python command line application to convert Markdown to PDF.

## Project Features

* Bare-bones: Only supports basic [CommonMark](https://commonmark.org/)
* *Not* beautiful: Left-aligned, PDF-base14 fonts. See alternatives below.
* Minimal requirements
    - [commonmark](https://pypi.org/project/commonmark/)
    - [PyMuMDF](https://pypi.org/project/PyMuPDF/)

## Alternatives
There are several projects that can be considered if you need something with more features.  Of note: 
* pandoc + latex
* rst2pdf
* rinohtype

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

