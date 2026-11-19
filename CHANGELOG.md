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
  keywords, license-file reference, and `pytest-cov` dev dependency
- README: added Installation, Quick Start, and API Reference sections;
  badges (latest release, PyPI version, CI status, license, Python, mypy,
  ruff, pre-commit); release link and API Reference table
- Renamed package from `origami-simulator` to `origami-engine`
- `MANIFEST.in` — include schemas, docs image, examples, experiments, LICENSE

### Fixed
- `ruff format` issues in README.md, plotting.py, example.py
- `mypy` error in `render_individual.py` — `imageio` format arg type

## [0.1.0] - 2026-11-20

### Added
- `plot_pattern(creases, pat=None)` — reference-style crease pattern plot
  (Mountain=crimson dashed, Valley=royalblue dash-dot, degree labels,
  face indices, loop-edge markers, legend at lower center)
- `examples/05_plot_pattern.py` — runnable plotting snippet
- `docs/crease_pattern_plot.png` — committed reference image
- README "Crease pattern visualization" section with centered embedded image
- `pyproject.toml` — packaging metadata upgrade (classifiers, authors,
  keywords, license-files)
- `.github/workflows/ci.yml` — CI pipeline (ruff + mypy + pytest on
  Python 3.10/3.11, + publish-to-pypi job via OIDC)
- `ARCHITECTURE.md` — module overview, data flow, design decisions,
  public API table
- `CHANGELOG.md` — Keep a Changelog format
- `MANIFEST.in` — ensure source distribution includes all assets
- `tests/conftest.py` — shared pytest fixtures
- Coverage reporting via `pytest-cov`

### Changed
- Package renamed from `origami-simulator` to `origami-engine`
- `pyproject.toml` — classifiers, authors, keywords, license-files,
  `pytest-cov` dev dependency
- README — Installation, Quick Start, API Reference sections added;
  badges reorganized; release link and API Reference table added
- `render_individual.py` — removed `format="FFMPEG"` arg (imageio inference)
- `pyproject.toml` — updated dev deps (`pytest-cov` added)

### Fixed
- `ruff format` issues in README.md, plotting.py, example.py
- `mypy` error in `render_individual.py` — `imageio` format arg type

## [0.1.0-alpha] - 2026-11-19

### Added
- Initial modularized `origami_engine` package:
  `constants.py`, `types.py`, `backend.py`, `geometry.py`, `model.py`,
  `serialization.py`, `dynamics.py`, `simulation.py`, `evaluation.py`,
  `patterns.py`, `render_individual.py`, `example.py`
- `Makefile`, `.pre-commit-config.yaml`, `CONTRIBRIBUTING.md`
- `pyproject.toml` with dev extras (`pytest`, `ruff`, `mypy`, `pre-commit`)
- `examples/` with 4 runnable snippets + README
- `experiments/` archive: `TIMELINE.md` + `prototype_notebooks.zip`
- Badge row in README (CI, Python 3.10+, Apache-2.0, ruff, pre-commit, MuJoCo)

### Changed
- N/A

### Fixed
- N/A