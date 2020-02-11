import pytest
from pathlib import Path

from mdpdf.converter import convertMarkdown2Pdf

indir = Path(__file__).parent.absolute() / "input"
outdir = Path(__file__).parent.absolute() / "output"
outdir.mkdir(exist_ok=True)


def test_entire_spec():
    infilename = indir / "spec.txt"
    outfilename = outdir / "spec_raw.pdf"
    convertMarkdown2Pdf(infilename, outfilename)


def test_entire_spec_with_examples():
    import spec_to_md

    spec = indir / "spec.txt"
    md = outdir / "spec.md"
    pdf = outdir / "spec_examples.pdf"
    spec_to_md.convertSpecExamples(spec, md)
    convertMarkdown2Pdf(md, pdf)


def test_quick():
    infilename = indir / "quick.md"
    outfilename = outdir / "quick.pdf"
    convertMarkdown2Pdf(infilename, outfilename)


if __name__ == "__main__":

    test_quick()

