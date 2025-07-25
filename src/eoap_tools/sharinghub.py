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

"""EOAP Tools sharinghub module."""

import logging
import sys
import urllib.parse
from pathlib import Path

import dvc.config
import dvc.repo
import git

from eoap_tools.utils import url_basic_auth

logger = logging.getLogger(__name__)


def download_repository(
    url: str,
    path: Path | None = None,
    user: str | None = None,
    token: str | None = None,
) -> git.Repo:
    """Download repository and return `git.Repo` instance."""
    if not path:
        url_path = Path(urllib.parse.urlparse(url).path)
        path = Path(url_path.stem)

    if path.is_dir():
        try:
            git_repo = git.Repo(path)
        except git.InvalidGitRepositoryError:
            logger.error("invalid repository: %s", path)
            sys.exit(-1)
        logger.info("repository found locally")
    else:
        if user and token:
            url = url_basic_auth(url, user=user, password=token)
            logger.debug("clone url: %s", url)
        else:
            logger.info("clone url: %s", url)

        logger.info("cloning repository...")
        git_repo = git.Repo.clone_from(
            url=url,
            to_path=path,
        )

    return git_repo


def configure_dvc(
    git_repo: git.Repo,
    password: str | None,
    s3_access_key_id: str | None,
    s3_secret_access_key: str | None,
) -> dvc.repo.Repo | None:
    """Configure DVC authentication for Git repository."""
    try:
        dvc_repo = dvc.repo.Repo(git_repo.working_dir)
        logger.info("dvc detected")
    except dvc.repo.NotDvcRepoError:
        return None

    dvc_remote: str | None = dvc_repo.config.get("core", {}).get("remote")
    logger.info("dvc remote: %s", dvc_remote)
    if not dvc_remote:
        logger.error("dvc: no remote configured")
        sys.exit(-1)

    dvc_url = dvc_repo.config["remote"][dvc_remote]["url"]
    dvc_scheme = urllib.parse.urlparse(dvc_url).scheme

    if s3_access_key_id and s3_secret_access_key:
        if dvc_scheme == "s3":
            dvc_credentials = {
                "access_key_id": s3_access_key_id,
                "secret_access_key": s3_secret_access_key,
            }
        else:
            dvc_credentials = {"password": s3_access_key_id}
    elif password:
        dvc_credentials = {"password": password}
    else:
        logger.error("dvc: no credentials given")
        sys.exit(-1)

    logger.debug("dvc credentials: %s", dvc_credentials)
    logger.info("dvc credentials configuration...")
    try:
        with dvc_repo.config.edit(level="local") as conf:
            conf["remote"][dvc_remote] = dvc_credentials
    except dvc.config.ConfigError as e:
        logger.error("dvc configuration error: %s", e)
        sys.exit(-1)

    logger.debug("dvc credentials configured")
    return dvc_repo
