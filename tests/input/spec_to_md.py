import re
from pathlib import Path


inFile = "spec.txt"
outFile = inFile + ".md"
text = open(inFile, encoding="utf-8").read()

#
# Fix Examples, so they don't show HTML, they just get processed like the body
# text.
#
# Note : https://regex101.com/r/wsVyL9/1
regex = re.compile(
    r"````+ example\n(.*?)^\.(.*?````+)", flags=re.DOTALL | re.MULTILINE,
)
s = r"""
```
Example:
\1
```
---
\1
---"""
newtext = regex.sub(s, text)


#
# Fix anchors, since they don't apply (yet?)
#
# https://regex101.com/r/wsVyL9/4
regex = re.compile(r"\[([\s|\w]*?)\]\(@\)", flags=re.DOTALL | re.MULTILINE,)
newtext = regex.sub(r"**\1**", newtext)

# https://regex101.com/r/wsVyL9/3
regex = re.compile(r"\[([\s|\w]*?)\](?!\()", flags=re.DOTALL | re.MULTILINE,)
newtext = regex.sub(r"*\1*", newtext)

open(outFile, "w", encoding="utf-8").write(newtext)
