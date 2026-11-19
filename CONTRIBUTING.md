# Contributing to MuJoCo Origami Simulator

Thanks for your interest in contributing! This guide covers how to set up a
development environment, run the test suite, and submit changes.

## Development setup

```bash
python -m venv .venv
. .venv/bin/activate
make install          # installs the package in editable mode with dev deps
# or, without make:
pip install -e ".[dev]"
```

## Running tests

```bash
make test            # pytest -q
# or:
python -m pytest -q tests
```

## Running the example workflows

```bash
make example         # minimal evaluation example
make render          # render the reference pattern to individual_simulation.mp4
make examples        # run every script under examples/
```

## Code style

- Linting/formatting: [ruff](https://docs.astral.sh/ruff/) (`make lint`, `make format`)
- Type checking: [mypy](https://mypy.readthedocs.io/) (`make typecheck`)
- Install the pre-commit hooks once: `pre-commit install`

Please run `make lint` and `make test` before opening a pull request.

## Submitting changes

1. Fork the repository and create a feature branch (e.g. `feat/...`, `fix/...`, `chore/...`).
2. Make your changes, keeping commits focused and reasonably sized.
3. Add or update tests for any new behavior.
4. Open a pull request against `main` with a clear description of the change.

## Project layout

See `ARCHITECTURE.md` for module responsibilities and the data flow through the
pipeline.
