# Copyright 2025, CS GROUP - France, https://www.csgroup.eu/
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Command-line interface."""

import logging
import os
import sys
from importlib.metadata import metadata
from pathlib import Path

import click

from eoap_tools.stac import download_assets, generate_catalog

logger = logging.getLogger(__name__)


@click.group()
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Set log level to DEBUG.",
)
def main(verbose: bool) -> None:
    """EOAP Tools CLI."""
    debug = verbose or (os.environ.get("DEBUG", "false").lower() in ["1", "true"])
    logging.basicConfig(
        format="[%(asctime)s] [%(levelname)s]\t%(message)s",
        level=logging.DEBUG if debug else logging.INFO,
    )


@main.command()
def version() -> None:
    """Print version and exit."""
    m = metadata(__package__)
    pkg_name = m["Name"]
    pkg_version = m["Version"]
    pkg_summary = m["Summary"]
    print(f"{pkg_name}: {pkg_version}")
    print(pkg_summary)


@main.group()
def stac() -> None:
    """STAC utilities."""


@stac.command("download-assets")
@click.argument("stac_input")
@click.option(
    "--output",
    "output_path",
    type=click.Path(file_okay=False, dir_okay=True, writable=True, path_type=Path),
    help="Path to the directory where the assets will be downloaded.",
)
def stac_download_assets(stac_input: str, output_path: Path | None) -> None:
    """Download STAC item assets to output."""
    if not output_path:
        output_path = Path("stac-assets")
    if output_path.exists():
        logger.error("output path already exists")
        sys.exit(-1)

    logger.info("downloading %s at: %s", stac_input, output_path)
    download_assets(stac_input, output_path)


@stac.command("generate-catalog")
@click.argument(
    "assets_path",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, readable=True, path_type=Path
    ),
)
@click.option(
    "--output",
    "output_path",
    type=click.Path(file_okay=False, dir_okay=True, writable=True, path_type=Path),
    help="Path to the directory where the catalog will be generated.",
)
def stac_generate_catalog(assets_path: Path, output_path: Path | None) -> None:
    """Generate STAC catalog from directory of assets to output."""
    if not output_path:
        output_path = Path("stac-catalog")
    if output_path.exists():
        logger.error("output path already exists")
        sys.exit(-1)

    logger.info("cataloging directory %s at: %s", assets_path, output_path)
    generate_catalog(assets_path, output_path)
