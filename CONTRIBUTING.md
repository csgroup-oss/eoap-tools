# Contributing

First off, thanks for wanting to contribute! 🎉

We appreciate your contributions and engagement. Even if you don't know how to code,
contributions are not always about coding. Everyone can help in their own way,
by reporting typos, or improving the documentation for example. Every bug report,
suggestion, and discussion helps improve the project.

The following elements will allow you to contribute, with a little guide to learn how
to make an approved contribution. Don't hesitate to share some new ideas to improve it!

## Table of Contents

- [Getting started](#getting-started)
  - [Pre-requisites](#pre-requisites)
  - [Clone the repository](#clone-the-repository)
  - [Environment setup](#environment-setup)
- [How to contribute?](#how-to-contribute)
  - [Organization](#organization)
    - [Reporting issues](#reporting-issues)
    - [Suggesting Enhancements](#suggesting-enhancements)
    - [Working on issues](#working-on-issues)
  - [Writing code](#writing-code)
    - [References](#references)
    - [Quality Assurance](#quality-assurance)
      - [Lint](#lint)
      - [Tests](#tests)
      - [Security](#security)
    - [Release](#release)
  - [Git](#git)
    - [Hooks](#hooks)
    - [Pull](#pull)

## Getting started

### Pre-requisites

We recommend a Linux-based distribution. You will need the following tools on your system:

- [Git](https://git-scm.com/): version control system.
- [Make](https://www.gnu.org/software/make/): utility mandatory to run
  the `make` command, that we use for shortcuts of most-used commands
  in the project life-cycle.
- [Python](https://www.python.org/) (≥3.12): language of the project,
  you'll need the interpreter.
- [uv](https://docs.astral.sh/uv/) (≥0.8.0): package and project manager for Python.

### Clone the repository

```bash
git clone https://github.com/csgroup-oss/eoap-tools.git
```

### Environment setup

List available commands:

```bash
make help
```

To setup your development environment run `make setup`.

Here's what it does:

- `uv sync`: create an isolated Python virtual environment,
  install the project in editable mode, synchronize project dependencies,
  and also install `dev` dependency group.
- `pre-commit install --install-hooks`: install pre-commit hooks. Learn more [here](#hooks).

This project uses multiple tools for its development, and your virtual environment
created with the previous command is just here to give you a working development environment.
Some tools are handled in sub-virtual environments created by [Tox](https://tox.wiki),
a virtual env manager and automation tool. The `install-dev` only gives you the
tools that you will be directly using, delegating other installations inside of _Tox_
virtual envs.

## How to contribute?

### Organization

#### Reporting issues

Traceability is necessary for a healthy development environment. Each
bug encountered must be reported by the creation of a new issue. Details
on how to reproduce it must be provided, and if possible visuals
(screenshots) are welcome.

Open a [Bug Report](https://github.com/csgroup-oss/eoap-tools/issues/new?template=bug_report.md)
for issues that you encountered, if it's not already present in the issue tracker.

Before Submitting an Issue:

- **Check Existing Issues**: Your question or bug may already be reported.
- **Search the Documentation**: Ensure the answer isn’t already covered.

#### Suggesting Enhancements

If you have an idea to improve the project, we would love to hear it!
Please create a [Feature Request](https://github.com/csgroup-oss/eoap-tools/issues/new?template=feature_request.md)
if something comes to your mind.

#### Working on issues

You can work on every open issue. Keep in mind to reference them in your
commits and pull requests, by following the [GitHub autolink convention](https://docs.github.com/en/github/writing-on-github/autolinked-references-and-urls#issues-and-pull-requests).

1. **Fork the Repository** by clicking the "Fork" button on the repository page.
2. **Clone the Fork** to your local machine.

   ```bash
   git clone https://github.com/csgroup-oss/eoap-tools.git
   cd eoap-tools
   ```

3. **Follow the [Getting started](#getting-started) section** for project setup.
4. **Create a new branch** to work on.

   ```bash
   git checkout -b (fix-or-feat)/your-topic-name
   ```

5. **Commit your changes** with a clear and concise commit message.
6. **Push your changes** to your fork.

   ```bash
   git push origin (fix-or-feat)/your-topic-name
   ```

7. **Create a Pull Requests** from your fork's branch to the main repository's main
   branch. Provide a clear and concise description of your changes and the problem
   they address.

   Please follow these guidelines:

   - Use a clear and descriptive title.
   - Include every relevant issue number in the body, not in the title.
   - Give a complete description of every change made in the body.

### Writing code

#### References

Writing clean code is very important for a project. We read way more code than we write,
readable code is not a luxury, it is a necessity.

Let us be reminded of the Zen of Python, by Tim Peters:

```text
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```

You are not alone for this difficult task. In the next sections you will
find about our QA tools.

#### Quality Assurance

##### Lint

To ensure good code writing, we use a lot the following lint tools:

- [ruff](https://docs.astral.sh/ruff/): an extremely fast Python linter and formatter,
  written in Rust. Compatible with `black` formatting style, implement for
  linting `pylint`, `bandit`, `isort`, `pyupgrade`, `eradicate`, and
  `flake8` with dozens of its plugins. Check the configuration
  in our `pyproject.toml`.
- [mypy](https://mypy.readthedocs.io): static type checker.

These tools are run with:

```bash
make lint
```

You can use `lint-watch` to run these tool on file change in `src/`. This
is really useful as it gives you instantaneous feedback on your code.

> Note: All of these are also run for each commit, failing the commit
> if at least one error is found.

##### Tests

We shall always aim for the highest code coverage in our tests, and our
development environment should use tools that will help us ensure it.

The test frameworks used are unittest and pytest, run with tox. Thanks
to pytest-cov, code coverage is evaluated.

Run the tests with:

```bash
make test
```

##### Security

We use [pip-audit](https://pypi.org/project/pip-audit/) in our CI to check
our Python dependencies for potential security vulnerabilities.

#### Release

You can create a release with `make release`, the `CHANGELOG.md` file
will be automatically generated.

Don't forget to push the tags to your origin repo!

```bash
git push --tags
```

### Git

#### Hooks

We use [Pre-commit](https://pre-commit.com/) to run tools at specific
moments of the Git workflow, with [Git Hooks](https://git-scm.com/docs/githooks).
It will mostly run linting and formatting tools on the source code in our case.
Some tools will also run for yaml, json, or markdown files etc... The commitizen
tool will also enforce conventional commit usage.

Our hooks needs the following dependencies:

- Python (≥3.12)
- pre-commit (≥4.0)

#### Pull

It is good practice to pull with rebase over a normal pull.

```bash
git switch <your-branch>

# classic
git pull

# much better
git pull --rebase
```

But do keep in mind that to be able to rebase, you'll need to have a
clean state of your repository, with no changes to commit. If that's not
the case, you can use `stash` in addition:

```bash
git switch <your-branch>
git stash
git pull --rebase
git stash pop
```

If you don't want to specify `--rebase` each time you pull, configure it:

```bash
git config --local pull.rebase true
```

And if you don't want to manually `stash` at each rebase, you can also
configure it:

```bash
git config --local rebase.autostash true
```

Now each `git pull` will use `--rebase` and automatically `stash`!
