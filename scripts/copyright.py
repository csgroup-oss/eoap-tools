#!/usr/bin/env python3
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

"""Add copyright header to files."""

import argparse
import pathlib
import re
import sys
from collections.abc import Sequence
from datetime import datetime, timezone

COMMENTS_HEADER_REGEX = re.compile(r"^#(.\n?)*(?=\n\n|\n\Z)")
COPYRIGHT_HEADER_VALIDATION_REGEX = re.compile(r"^Copyright")
COPYRIGHT_HEADER_FILE_REGEX = re.compile(
    r"^# Copyright(.\n?)*(?=\n\n|\n\Z)", re.MULTILINE
)


def read_copyright_header(filepath: str) -> str:
    _filepath = pathlib.Path(filepath)
    copyright_header_template = _filepath.read_text()
    copyright_header = copyright_header_template.format(
        year=datetime.now(tz=timezone.utc).year
    )
    if COPYRIGHT_HEADER_VALIDATION_REGEX.search(copyright_header):
        return "\n".join(
            f"# {line}".rstrip() for line in copyright_header.rstrip().split("\n")
        ).rstrip()
    msg = 'Copyright header should start by "Copyright".'
    raise ValueError(msg)


def add_copyright_header(filepath_: str, /, copyright_header: str) -> bool:
    filepath = pathlib.Path(filepath_)
    file_content = filepath.read_text()
    file_content_stripped = file_content.strip()
    if not file_content_stripped:
        filepath.write_text(copyright_header + "\n")
    elif file_content_stripped == copyright_header:
        return False
    elif m := COPYRIGHT_HEADER_FILE_REGEX.search(file_content):
        file_copyright_header = m.group()
        if file_copyright_header == copyright_header:
            return False
        new_file_content = file_content.replace(
            file_copyright_header, copyright_header, 1
        )
        filepath.write_text(new_file_content)
    elif m := COMMENTS_HEADER_REGEX.search(file_content):
        comments_header = m.group().rstrip()
        body = file_content.replace(comments_header, "", 1).lstrip()
        body = f"\n\n{body}" if body else "\n"
        new_file_content = f"{comments_header}\n{copyright_header}{body}"
        filepath.write_text(new_file_content)
    else:
        filepath.write_text(f"{copyright_header}\n\n{file_content}")
    return True


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Add copyright header to given files.")
    parser.add_argument(
        "filenames",
        nargs="*",
        help="List of files changed.",
    )
    parser.add_argument(
        "--file",
        default="copyright.txt",
        help="Path to a file containing the copyright header.",
    )
    args = parser.parse_args(argv)

    passed = True
    copyright_header = read_copyright_header(filepath=args.file)
    for filepath in args.filenames:
        if add_copyright_header(filepath, copyright_header):
            passed = False
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
