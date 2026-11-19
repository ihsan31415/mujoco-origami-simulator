# Changelog

All notable changes to the MuJoCo Origami Simulator are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `origami_engine/plotting.py` with `plot_pattern(creases, pat=None)` for
  reference-style crease pattern visualization
- `examples/05_plot_pattern.py` runnable plotting snippet
- `docs/crease_pattern_plot.png` committed reference plot image
- README "Crease pattern visualization" section
- `matplotlib` runtime dependency
- `.github/workflows/ci.yml` continuous integration workflow
- `ARCHITECTURE.md` module layout and data flow documentation
- `CHANGELOG.md` release history
- `MANIFEST.in` source distribution manifest
- `conftest.py` shared pytest fixtures
- Coverage reporting via `pytest-cov`

### Changed
- `pyproject.toml` packaging metadata: classifiers, project URLs, authors,
  keywords, license file reference, and `pytest-cov` dev dependency
- README: added Installation, Quick Start, and API Reference sections;
  added coverage badge; centered and shrank the crease pattern plot image

## [0.1.0] - 2026-11-19

### Added
- Initial modularized `origami_engine` package:
  `constants.py`, `types.py`, `backend.py`, `geometry.py`, `model.py`,
  `serialization.py`, `dynamics.py`, `simulation.py`, `evaluation.py`,
  `patterns.py`, `render_individual.py`, `example.py`
- `Makefile`, `.pre-commit-config.yaml`, `CONTRIBUTING.md`
- `pyproject.toml` with dev extras (`pytest`, `ruff`, `mypy`, `pre-commit`)
- `examples/` with 4 runnable snippets + README
- `experiments/` archive: `TIMELINE.md` + `prototype_notebooks.zip`
- Badge row in README (CI, Python 3.10+, Apache-2.0, ruff, pre-commit, MuJoCo)
