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

# TODO: consider pip install click-config-file


@click.command()
@click.option("--output", "-o", help="Destination for file output.")
@click.option("--header", "-h", help="Header template.")
@click.option("--footer", "-f", help="Footer template.")
@click.argument("inputs", nargs=-1)
def cli(output: str, header: str, footer: str, inputs):
    """Convert Markdown to PDF.."""
    if not output:
        ctx = click.get_current_context()
        ctx.fail("No output specified.")

    if header:
        Header.setFmt(header)
    if footer:
        Footer.setFmt(footer)

    if inputs:
        globlist = []
        for i in inputs:
            print(i)
            globlist.extend(glob.glob(i))

        converter = Converter(output)
        converter.convertMultiple(globlist)
    else:
        ctx = click.get_current_context()
        ctx.fail("No input specified.")

