"""Test the the module can be imported."""


def test_can_import():
    """Import the module and check for a version."""
    import kniteditor
    assert kniteditor.__version__
