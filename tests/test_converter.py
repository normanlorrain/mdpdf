import pytest
from pathlib import Path

from mdpdf.converter import convertMarkdown2Pdf

indir = Path(__file__).parent.absolute()
outdir = Path(__file__).parent.absolute() / "output"
outdir.mkdir(exist_ok=True)


def test_entire_spec():
    infilename = indir / "syntax.md"
    outfilename = outdir / "syntax.pdf"
    convertMarkdown2Pdf(infilename, outfilename)


if __name__ == "__main__":
    test_entire_spec()
