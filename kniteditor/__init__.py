"""An editor for knitting projects."""
import sys

__version__ = "1.0.4"


def main(argv=sys.argv):
    """Open the editor window."""
    if "/test" in argv:
        import pytest
        errcode = pytest.main(["--pyargs", "knittingpattern", "kniteditor",
                               "AYABInterface"])
        sys.exit(errcode)
    else:
        from .EditorWindow import EditorWindow
        EditorWindow().run()

__all__ = ["main"]
