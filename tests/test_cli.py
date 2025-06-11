"""CLI test."""

from importlib.metadata import metadata

from click.testing import CliRunner

from eoap_tools._cli import main

runner = CliRunner()


def test_cli() -> None:
    """Running CLI with --help print help."""
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert result.stdout.startswith("Usage:")


def test_cli_version() -> None:
    """Running CLI with arg "version" print package name and version number."""
    m = metadata("eoap_tools")
    pkg_name = m["Name"]
    pkg_version = m["version"]
    pkg_summary = m["Summary"]

    result = runner.invoke(main, ["version"])

    assert result.exit_code == 0
    assert pkg_name in result.stdout
    assert pkg_version in result.stdout
    assert pkg_summary in result.stdout
