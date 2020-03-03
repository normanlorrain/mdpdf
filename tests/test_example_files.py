import pytest
from pathlib import Path
import mdpdf.cli as cli
from click.testing import CliRunner, Result

# pytestmark = pytest.mark.usefixtures("convertSpec")


def inPath(name):
    fullpath = Path(__file__).parent.absolute() / "input" / name
    return str(fullpath)


def outPath(name):
    fullpath = Path(__file__).parent.absolute() / "output"
    fullpath.mkdir(exist_ok=True)
    fullpath /= name
    return str(fullpath)


@pytest.fixture(scope="module")
def convertSpec(infile):
    b = r"````+ example\n(.*?)^\.(.*?````+)"  # Note : https://regex101.com/r/wsVyL9/1
    regex = re.compile(b, flags=re.DOTALL | re.MULTILINE,)
    text = open(infile, encoding="utf-8").read()
    s = r"\n```\nExample:\n\1\n```\n\1\n"
    s = r"""
```
Example:
\1
```
---
\1
---"""
    newtext = regex.sub(s, text)
    open(outfile, "w", encoding="utf-8").write(newtext)
    return outfile


@pytest.mark.parametrize(
    "inFile,outFile", [("quick.md", "quick.pdf"), ("lorem.md", "lorem.pdf")]
)
def test_example_Files(inFile, outFile):
    print(inFile, outFile)
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(cli.cli, ["-o", outPath(outFile), inPath(inFile)])
    print(result)
