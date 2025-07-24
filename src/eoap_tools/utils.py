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

"""EOAP Tools utils module."""

import urllib.parse


def is_url(href: str) -> bool:
    """Returns True if `href` is an URL, False otherwise."""
    parsed_url = urllib.parse.urlparse(href)
    return bool(parsed_url.scheme.startswith("http") and parsed_url.netloc)
