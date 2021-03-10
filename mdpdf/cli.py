#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the entry point for the command-line interface (CLI) application.

Itcan be used as a handy facility for running the task from a command line.

    To learn more about Click visit the
    `project website <http://click.pocoo.org/5/>`_.  There is also a very
    helpful `tutorial video <https://www.youtube.com/watch?v=kNke39OZ2k0>`_.

"""
import click
import glob

from mdpdf.converter import Converter
from mdpdf.headfoot import Header, Footer
from mdpdf.properties import setTitle, setSubject, setAuthor, setKeywords, setPaperSize
from mdpdf import log

# TODO: consider pip install click-config-file


@click.command()
@click.option(
    "--output", "-o", metavar="FILE", required=True, help="Destination for file output."
)
@click.option("--header", "-h", metavar="<template>", help="Sets the header template.")
@click.option("--footer", "-f", metavar="<template>", help="Footer template.")
@click.option("--title", "-t", default="", help="PDF title.")
@click.option("--subject", "-s", default="", help="PDF subject.")
@click.option("--author", "-a", default="", help="PDF author.")
@click.option("--keywords", "-k", default="", help="PDF keywords.")
@click.option(
    "--paper",
    "-p",
    default="letter",
    type=click.Choice(["letter", "A4"], case_sensitive=False),
    help="Paper size (default letter).",
)
@click.version_option()
@click.argument("inputs", nargs=-1)
def cli(
    output: str,
    header: str,
    footer: str,
    title: str,
    subject: str,
    author: str,
    keywords: str,
    paper: str,
    inputs,
):
    """Convert Markdown to PDF.

    \b
    For options below, <template> is a quoted, comma-
    delimited string, containing the left, centre,
    and right, header/footer fields. Format is

      "[left],[middle],[right]"

    \b
    Possible values to put here are:
      - Empty string
      - Arbitrary text
      - {page} current page number
      - {header} current top-level body text heading
      - {date} current date"""

    ctx = click.get_current_context()
    if not output:
        ctx.fail("No output specified.")

    try:
        if header:
            Header.setFmt(header)
        if footer:
            Footer.setFmt(footer)
    except Exception as e:
        ctx.fail(f"{e} in header/footer template.")

    if title:
        setTitle(title)

    if author:
        setAuthor(author)

    if subject:
        setSubject(subject)

    if keywords:
        setKeywords(keywords)

    if paper:
        setPaperSize(paper)

    if inputs:
        log.init()
        globlist = []
        for i in inputs:
            log.debug(i)
            matches = glob.glob(i)
            if matches:
                globlist.extend(matches)
            else:
                ctx.fail(f"File not found: {i}.")
        converter = Converter(output)
        converter.convert(globlist)
    else:
        ctx.fail("No input specified.")


if __name__ == "__main__":
    import sys

    cli.main(sys.argv[1:])
