import pytest
from pathlib import Path

from mdpdf.elements import *

def test_all():
    for eType,eFunction in elements.items():
        eFunction("blah")
