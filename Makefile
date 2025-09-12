##@ Project's Makefile, with utility commands for the project development lifecycle.

MAKEFLAGS += --no-print-directory

UV=uv
PYTHON=$(UV) run python
TOX=$(UV) run tox -qq
PRE_COMMIT=$(UV) run pre-commit
COMMITIZEN=$(UV) run cz

IMAGE=$(shell basename $(PWD))
TAG=latest

.PHONY: default help pipeline setup release clean shell
.PHONY: build install install-dev install-all pre-commit
.PHONY: lint lint-watch test docker

# ======================================================= #

default: help

pipeline: clean build lint test ## Run clean, build, lint, test.

setup: install-dev ## Run 'install-dev' and install pre-commit hooks.
	@$(PRE_COMMIT) install --install-hooks

release: ## Bump version, create tag and update 'CHANGELOG.md'.
	@$(COMMITIZEN) bump --yes --changelog
	@./scripts/update_latest_tag_msg.sh

clean: ## Clean temporary files, like python '__pycache__', dist build, tests reports.
	@find src tests -regex "^.*\(__pycache__\|\.py[co]\)$$" -delete
	@rm -rf dist tests-reports .*_cache

shell: ## Open Python shell.
	@$(PYTHON)

build: ## Build wheel and tar.gz in 'dist/'.
	@$(UV) build

install: ## Install in the python venv.
	@$(UV) sync --all-extras --no-dev --no-editable

install-dev: ## Install in editable mode inside the python venv with dev group dependencies.
	@$(UV) sync --all-extras

install-all: ## Install in editable mode inside the python venv with all extras and groups dependencies.
	@$(UV) sync --all-extras --all-groups

pre-commit: ## Run all pre-commit hooks.
	@$(PRE_COMMIT) run --all-files
	@$(PRE_COMMIT) run --hook-stage pre-push --all-files

lint: ## Lint python source code.
	@$(TOX) -e lint

lint-watch: ## Watch for src Python files changes and run `make lint`.
	@$(UV) run --script scripts/watch.py --clear --filter "*.py" src "make lint"

test: ## Invoke tox to run automated tests.
	@$(TOX)

docker: ## Build docker image.
	@docker build . -t $(IMAGE):$(TAG)

# ======================================================= #

HELP_COLUMN=11
help: ## Show this help.
	@printf "\033[1m################\n#     Help     #\n################\033[0m\n"
	@awk 'BEGIN {FS = ":.*##@"; printf "\n"} /^##@/ { printf "%s\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n\n  make \033[36m<target>\033[0m\n\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-$(HELP_COLUMN)s\033[0m %s\n", $$1, $$2 } ' $(MAKEFILE_LIST)
	@printf "\n"
