from logging import *
from pathlib import Path

# set up logging to file - see previous section for more details
LONGFORMAT = (
    "%(levelname)8s: " "%(asctime)s: " "%(filename)20s: " "%(lineno)4d: " "%(message)s"
)
SHORTFORMAT = "%(message)s"

# Root logger gets everything.  Handlers defined below will filter it out...

getLogger("").setLevel(DEBUG)


def init(filename=Path("mdpdf.log")):
    filehandler = FileHandler(filename, mode="w")
    filehandler.setLevel(DEBUG)
    filehandler.setFormatter(Formatter(LONGFORMAT))
    getLogger("").addHandler(filehandler)
    info(f"Logging to {filename.absolute()}")


# define a Handler which writes to sys.stderr
console = StreamHandler()
console.setLevel(INFO)
console.setFormatter(Formatter(SHORTFORMAT))
# add the handler to the root logger
getLogger("").addHandler(console)
