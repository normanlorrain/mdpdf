#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the entry point for the command-line interface (CLI) application.

Itcan be used as a handy facility for running the task from a command line.

.. note::

    To learn more about Click visit the
    `project website <http://click.pocoo.org/5/>`_.  There is also a very
    helpful `tutorial video <https://www.youtube.com/watch?v=kNke39OZ2k0>`_.

    To learn more about running Luigi, visit the Luigi project's
    `Read-The-Docs <http://luigi.readthedocs.io/en/stable/>`_ page.

.. currentmodule:: mdpdf.cli
.. moduleauthor:: Norman Lorrain <normanlorrain@gmail.com>
"""
import logging
import click
from .__init__ import __version__

# LOGGING_LEVELS = {
#     0: logging.NOTSET,
#     1: logging.ERROR,
#     2: logging.WARN,
#     3: logging.INFO,
#     4: logging.DEBUG,
# }  #: a mapping of `verbose` option counts to logging levels


@click.command()
@click.option("--output", "-o", help="Destination for file output.")
@click.option("--header", "-h", help="Header template.")
@click.option("--footer", "-f", help="Footer template.")
@click.option("--verbose", "-v", count=True, help="Enable verbose output.")
@click.argument("inputs", nargs=-1)
def cli(output: str, header: str, footer: str, verbose: int, inputs):
    """Convert Markdown to PDF.."""
    # Use the verbosity count to determine the logging level...
    if verbose > 0:
        # logging.basicConfig(
        #     level=LOGGING_LEVELS[verbose]
        #     if verbose in LOGGING_LEVELS
        #     else logging.DEBUG
        # )
        click.echo(
            click.style(
                f"Verbose logging is enabled. "
                f"(LEVEL={logging.getLogger().getEffectiveLevel()})",
                fg="yellow",
            )
        )
    # info.verbose = verbose
    if not output:
        ctx = click.get_current_context()
        ctx.fail("No output specified.")
    print(output, header, footer, inputs)

