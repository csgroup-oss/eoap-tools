"""Command-line interface."""

from importlib.metadata import metadata

import click


@click.group()
def main() -> None:
    """EOAP Tools CLI."""


@main.command()
def version() -> None:
    """Print version and exit."""
    m = metadata(__package__)
    pkg_name = m["Name"]
    pkg_version = m["Version"]
    pkg_summary = m["Summary"]
    print(f"{pkg_name}: {pkg_version}")
    print(pkg_summary)
