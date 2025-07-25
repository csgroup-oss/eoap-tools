# EOAP Tools

[![Language](https://img.shields.io/badge/language-python≥3.12-3776ab?style=flat-square)](https://www.python.org/)
![License](https://img.shields.io/badge/license-Apache--2.0-yellow?style=flat-square)
![Style](https://img.shields.io/badge/style-ruff-9a9a9a?style=flat-square)
![Lint](https://img.shields.io/badge/lint-ruff,%20mypy-brightgreen?style=flat-square)
![Security](https://img.shields.io/badge/security-bandit,%20pip--audit-purple?style=flat-square)
[![Tests](https://img.shields.io/github/actions/workflow/status/csgroup-oss/eoap-tools/check.yml?branch=main&label=Test)](https://github.com/csgroup-oss/eoap-tools/actions/workflows/check.yml)
[![Coverage](https://raw.githubusercontent.com/csgroup-oss/eoap-tools/refs/heads/gh-tests-coverages/data/main/badge.svg)](https://github.com/csgroup-oss/eoap-tools/actions/workflows/check.yml)

[Pull Request](https://github.com/csgroup-oss/eoap-tools/pulls) **·**
[Bug Report](https://github.com/csgroup-oss/eoap-tools/issues/new?template=bug_report.md) **·**
[Feature Request](https://github.com/csgroup-oss/eoap-tools/issues/new?template=feature_request.md)

Earth Observation Application Package tooling for CWL files.

The tool `eoap-tools` is a command-line interface designed to simplify the steps needed
when writing an [EOAP](https://eoap.github.io/) workflow.

## Usage

Global commands:

```sh
Usage: eoap-tools [OPTIONS] COMMAND [ARGS]...

  EOAP Tools CLI.

Options:
  -v, --verbose  Set log level to DEBUG.
  --help         Show this message and exit.

Commands:
  sharinghub  SharingHub utilities.
  stac        STAC utilities.
  version     Print version and exit.
```

STAC utilities:

```sh
Usage: eoap-tools stac [OPTIONS] COMMAND [ARGS]...

  STAC utilities.

Options:
  --help  Show this message and exit.

Commands:
  generate-catalog  Generate STAC catalog from directory of assets to output.
  prepare-assets    Prepare STAC item assets to output.
```

SharingHub utilities:

```sh
Usage: eoap-tools sharinghub [OPTIONS] COMMAND [ARGS]...

  SharingHub utilities.

Options:
  --help  Show this message and exit.

Commands:
  download-dataset  Download SharingHub dataset from repository URL.
```

## Environment variables

| Scope | Name | Description | Values |
|---|---|---|---|
| Global | `DEBUG` | Enable verbose logging. | `true`, `false` |
| sharinghub.download-dataset | `USER`, `EOAP_TOOLS__USER` | Git clone username. | string |
| sharinghub.download-dataset | `ACCESS_TOKEN`, `EOAP_TOOLS__ACCESS_TOKEN` | Git clone token.<br>DVC `password` credential for HTTP remotes. | string |
| sharinghub.download-dataset | `ACCESS_KEY_ID`, `AWS_ACCESS_KEY_ID`, `EOAP_TOOLS__ACCESS_KEY_ID` | DVC `access_key_id` credential for S3 remotes.` | string |
| sharinghub.download-dataset | `SECRET_ACCESS_KEY`, `AWS_SECRET_ACCESS_KEY`, `EOAP_TOOLS__SECRET_ACCESS_KEY` | DVC `secret_access_key` credential for S3 remotes. | string |

## Contributing

If you want to contribute to this project please check [CONTRIBUTING.md](CONTRIBUTING.md).

Everyone contributing to this project is expected to treat other people with respect,
and more generally to follow the guidelines articulated by our [Code of Conduct](./CODE_OF_CONDUCT.md).

## License

Copyright &copy; 2025, CS GROUP - FRANCE

EOAP Tools is licensed under the Apache-2.0 license. A copy of this license is provided in the [LICENSE](./LICENSE) file.

## Acknowledgements

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter)
from the project template [CGuichard/cookiecutter-pypackage](https://github.com/CGuichard/cookiecutter-pypackage).
