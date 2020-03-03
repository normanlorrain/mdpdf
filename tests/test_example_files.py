import pytest

from pathlib import Path
import mdpdf.cli as cli
from click.testing import CliRunner, Result


def inPath(name):
    fullpath = Path(__file__).parent.absolute() / "input" / name
    return str(fullpath)


def outPath(name):
    fullpath = Path(__file__).parent.absolute() / "output"
    fullpath.mkdir(exist_ok=True)
    fullpath /= name
    return str(fullpath)


@pytest.mark.parametrize(
    "inFile,outFile",
    [
        ("quick.md", "quick.pdf"),
        ("lorem.md", "lorem.pdf"),
        ("spec.txt.md", "spec.pdf"),
    ],
)
def test_example_Files(inFile, outFile):
    print(inFile, outFile)
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(cli.cli, ["-o", outPath(outFile), inPath(inFile)])
    print(result)
