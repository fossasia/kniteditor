"""Test the the module can be imported."""


def test_can_import():
    """Import themodule and check for a version."""
    import kniteditor
    assert kniteditor.__version__
