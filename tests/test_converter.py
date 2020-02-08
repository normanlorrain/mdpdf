import pytest
from pathlib import Path

from mdpdf.converter import convertMarkdown2Pdf

indir = Path(__file__).parent.absolute() / "input"
outdir = Path(__file__).parent.absolute() / "output"
outdir.mkdir(exist_ok=True)


def test_entire_spec():
    infilename = indir / "spec.txt"
    outfilename = outdir / "spec.pdf"
    convertMarkdown2Pdf(infilename, outfilename)


def test_quick():
    infilename = indir / "quick.md"
    outfilename = outdir / "quick.pdf"
    convertMarkdown2Pdf(infilename, outfilename)


if __name__ == "__main__":

    test_entire_spec()

