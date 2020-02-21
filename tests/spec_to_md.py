import re
from pathlib import Path


def convertSpecExamples(infile, outfile):

    # a = r"````+ example\n((.*\n)+?)(?=^\.\n)(.*\n)((.*\n)+?)(?=(````+$))"
    b = r"````+ example\n(.*?)^\.(.*?````+)"

    # Note : https://regex101.com/r/wsVyL9/1

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


if __name__ == "__main__":
    convertSpecExamples()

