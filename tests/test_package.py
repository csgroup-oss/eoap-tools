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

"""Basic package test."""


def test_package_import() -> None:
    """Import package."""
    import eoap_tools  # noqa: F401, PLC0415


def test_package_version_is_defined() -> None:
    """Check imported package have __version__ defined."""
    import eoap_tools  # noqa: PLC0415

    assert eoap_tools.__version__ != "undefined"
