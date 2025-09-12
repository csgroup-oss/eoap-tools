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

"""CLI test."""

from importlib.metadata import metadata

from click.testing import CliRunner

from eoap_tools._cli import main

runner = CliRunner()


def test_cli() -> None:
    """Running CLI without argument print help."""
    result = runner.invoke(main)
    assert result.exit_code == 2
    assert result.stderr.startswith("Usage:")


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
