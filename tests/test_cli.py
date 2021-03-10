#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: test_cli
.. moduleauthor:: Norman Lorrain <normanlorrain@gmail.com>

This is the test module for the project's command-line interface (CLI)
module.
"""
from pathlib import Path
import mdpdf.cli as cli

from click.testing import CliRunner, Result


# To learn more about testing Click applications, visit the link below.
# http://click.pocoo.org/5/testing/


def test_cliMultiple():
    runner: CliRunner = CliRunner()

    result: Result = runner.invoke(
        cli.cli,
        ["-o", "output", "-h", ",bar,baz", "-f", "baz,foo,bar", "aaaa", "bbbb", "cccc"],
    )


def test_cli():
    indir = Path(__file__).parent.absolute() / "input"
    outdir = Path(__file__).parent.absolute() / "output"
    outdir.mkdir(exist_ok=True)
    infilename = indir / "quick.md"
    outfilename = outdir / "quick.pdf"

    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(cli.cli, ["-o", outfilename, infilename])

    pass


if __name__ == "__main__":
    test_cli()
    pass
