"""Basic package test."""


def test_package_import():
    """Import package."""
    import eoap_tools  # noqa: F401


def test_package_version_is_defined():
    """Check imported package have __version__ defined."""
    import eoap_tools

    assert eoap_tools.__version__ != "undefined"
