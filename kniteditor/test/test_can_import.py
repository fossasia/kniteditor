import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", ".."))


def test_can_import():
    import kniteditor
    assert kniteditor.__version__
