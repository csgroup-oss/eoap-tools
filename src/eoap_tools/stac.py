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

"""EOAP Tools stac module."""

import datetime
import logging
import mimetypes
import shutil
import sys
import time
import uuid
from pathlib import Path
from typing import cast

import pystac
import requests

from eoap_tools.utils import is_url

logger = logging.getLogger(__name__)


def prepare_assets(stac_input: str, output_path: Path) -> None:
    """Prepare STAC input assets in `output_path`."""
    if is_url(stac_input):
        logger.info("remote STAC item: %s", stac_input)
        stac_item = cast("pystac.Item", pystac.read_file(stac_input))
    else:
        stac_catalog_path = Path(stac_input) / "catalog.json"
        logger.info("local STAC catalog: %s", stac_catalog_path)
        if not stac_catalog_path.is_file():
            logger.error("STAC catalog not found: %s", stac_catalog_path)
            sys.exit(-1)

        stac_catalog = cast("pystac.Catalog", pystac.read_file(stac_catalog_path))
        stac_item = next(stac_catalog.get_items())

    for asset_name, asset in stac_item.assets.items():
        asset_href = asset.get_absolute_href()
        if not asset_href:
            continue

        if is_url(asset_href):
            dest_path: Path = output_path / asset_name
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info("download '%s' to '%s'", asset_href, dest_path)
            response = requests.get(asset_href, timeout=10, stream=True)
            response.raise_for_status()
            with dest_path.open("wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        else:
            asset_path = Path(asset_href)
            dest_path = output_path / asset_path.name
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info("copy '%s' to '%s'", asset_href, dest_path)
            shutil.copyfile(asset_path, dest_path)


def generate_catalog(assets_path: Path, catalog_path: Path) -> None:
    """Generate STAC catalog from directory of assets."""
    if not assets_path.is_dir():
        logger.error("assets path does not exists: %s", assets_path)
        sys.exit(-1)

    stac_catalog = pystac.Catalog(
        id=f"eoap-{str(uuid.uuid4())[:8]}-{int(time.time())}",
        description="Processing output STAC catalog.",
    )
    stac_item = pystac.Item(
        id="output",
        geometry=None,
        bbox=None,
        datetime=datetime.datetime.now(tz=datetime.UTC),
        properties={},
    )

    for asset_path in assets_path.iterdir():
        if asset_path.is_file():
            mime_type, _ = mimetypes.guess_type(asset_path)
            media_type = mime_type if mime_type else "application/octet-stream"
            stac_item.add_asset(
                key=asset_path.name,
                asset=pystac.Asset(href=asset_path.name, media_type=media_type),
            )
            dest_path: Path = catalog_path / stac_item.id / asset_path.name
            logger.info("copy '%s' to: %s", asset_path, dest_path)
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(asset_path, dest_path)

    stac_catalog.add_item(stac_item)
    stac_catalog.normalize_and_save(
        str(catalog_path), catalog_type=pystac.CatalogType.SELF_CONTAINED
    )
    logger.info("STAC catalog saved to: %s", catalog_path)
