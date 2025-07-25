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

from eoap_tools.sharinghub import configure_dvc, download_repository
from eoap_tools.stac import generate_catalog, prepare_assets

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


@stac.command("prepare-assets")
@click.argument("stac_input")
@click.option(
    "--output",
    "output_path",
    type=click.Path(file_okay=False, dir_okay=True, writable=True, path_type=Path),
    help="Path to the directory where the assets will be downloaded.",
)
def stac_prepare_assets(stac_input: str, output_path: Path | None) -> None:
    """Prepare STAC item assets to output."""
    if not output_path:
        output_path = Path("stac-assets")
    if output_path.exists():
        logger.error("output path already exists")
        sys.exit(-1)

    logger.info("preparing %s at: %s", stac_input, output_path)
    prepare_assets(stac_input, output_path)


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


@main.group()
def sharinghub() -> None:
    """SharingHub utilities."""


@sharinghub.command("download-dataset")
@click.argument("DATASET_URL")
@click.option(
    "--pull",
    is_flag=True,
    help="Pull with DVC.",
)
@click.option(
    "--version",
    metavar="REVISION",
    help="Version of the dataset (Git revision).",
)
@click.option(
    "--user",
    metavar="USERNAME",
    help="Username used to download the repository.",
)
@click.option(
    "--access-token",
    metavar="TOKEN",
    help=(
        "Access token used to download the repository. "
        "Also used for DVC if the dataset uses SharingHub store API."
    ),
)
@click.option(
    "--access-key-id",
    metavar="TOKEN",
    help="Access Key ID for DVC S3 configuration.",
)
@click.option(
    "--secret-access-key",
    metavar="TOKEN",
    help="Secret Access Key for DVC S3 configuration.",
)
@click.option(
    "--output",
    "output_path",
    type=click.Path(file_okay=False, dir_okay=True, writable=True, path_type=Path),
    help="Path to the directory where the dataset will be downloaded.",
)
def sharinghub_download_dataset(  # noqa: PLR0913
    dataset_url: str,
    pull: bool,
    version: str | None,
    user: str | None,
    access_token: str | None,
    access_key_id: str | None,
    secret_access_key: str | None,
    output_path: Path | None,
) -> None:
    """Download SharingHub dataset from repository URL."""
    logger.info("dataset url: %s", dataset_url)

    user = os.environ.get("USER", user)
    user = os.environ.get("EOAP_TOOLS__USER", user)
    access_token = os.environ.get("ACCESS_TOKEN", access_token)
    access_token = os.environ.get("EOAP_TOOLS__ACCESS_TOKEN", access_token)
    access_key_id = os.environ.get("ACCESS_KEY_ID", access_key_id)
    access_key_id = os.environ.get("AWS_ACCESS_KEY_ID", access_key_id)
    access_key_id = os.environ.get("EOAP_TOOLS__ACCESS_KEY_ID", access_key_id)
    access_key_id = access_key_id or access_token
    secret_access_key = os.environ.get("SECRET_ACCESS_KEY", secret_access_key)
    secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY", secret_access_key)
    secret_access_key = os.environ.get("EOAP_TOOLS__SECRET_ACCESS_KEY", secret_access_key)
    secret_access_key = secret_access_key or access_token
    logger.debug("git user: %s", user)
    logger.debug("git access token: %s", access_token)
    logger.debug("access key id: %s", access_key_id)
    logger.debug("secret access key: %s", secret_access_key)

    git_repo = download_repository(
        url=dataset_url,
        path=output_path,
        user=user,
        token=access_token,
    )
    git_repo_path = Path(git_repo.working_dir)
    logger.info("repository: %s", git_repo_path)

    if version:
        logger.info("checkout repository revision: %s", version)
        git_repo.git.checkout(version)

    dvc_repo = configure_dvc(
        git_repo,
        password=access_token,
        s3_access_key_id=access_key_id,
        s3_secret_access_key=secret_access_key,
    )
    if not dvc_repo:
        logger.warning("invalid dvc repository: %s", git_repo.working_dir)
        sys.exit(0)

    if pull:
        logger.info("dvc pull...")
        dvc_repo.pull(force=True)
