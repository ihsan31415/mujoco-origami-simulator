# MuJoCo Origami Engine

<p align="center">
  <a href="https://github.com/ihsan31415/origami-engine/releases">
    <img src="https://img.shields.io/github/v/release/ihsan31415/origami-engine?display_name=tag&logo=github" alt="Latest Release">
  </a>
  <a href="https://github.com/ihsan31415/origami-engine/actions/workflows/ci.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/ihsan31415/origami-engine/ci.yml/badge.svg" alt="CI">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11-blue?logo=python&logoColor=white" alt="Python">
  </a>
  <a href="https://mujoco.org/">
    <img src="https://img.shields.io/badge/Physics-MuJoCo-blue" alt="MuJoCo">
  </a>
  <a href="https://numpy.org/">
    <img src="https://img.shields.io/badge/NumPy-Scientific%20Computing-013243?logo=numpy&logoColor=white" alt="NumPy">
  </a>
  <a href="https://shapely.readthedocs.io/">
    <img src="https://img.shields.io/badge/Geometry-Shapely-3776AB" alt="Shapely">
  </a>
  <br>
  <a href="https://github.com/python/mypy">
    <img src="https://img.shields.io/badge/Type%20Checking-mypy-blue?logo=python&logoColor=white" alt="mypy">
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/badge/Code%20Style-Ruff-D7FF64?logo=ruff&logoColor=black" alt="Ruff">
  </a>
  <a href="https://docs.pytest.org/">
    <img src="https://img.shields.io/badge/Tests-pytest-0A9EDC?logo=pytest&logoColor=white" alt="pytest">
  </a>
  <a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white" alt="pre-commit">
  </a>
  <a href="https://github.com/ihsan31415/origami-engine/commits/main">
    <img src="https://img.shields.io/github/last-commit/ihsan31415/origami-engine" alt="Last Commit">
  </a>
  <a href="https://github.com/ihsan31415/origami-engine/issues">
    <img src="https://img.shields.io/github/issues/ihsan31415/origami-engine" alt="Issues">
  </a>
  <a href="https://github.com/ihsan31415/origami-engine/stargazers">
    <img src="https://img.shields.io/github/stars/ihsan31415/origami-engine" alt="Stars">
  </a>
  <a href="https://github.com/ihsan31415/origami-engine/LICENSE">
    <img src="https://img.shields.io/github/license/ihsan31415/origami-engine" alt="License">
  </a>
</p>

## 🚀 Getting Started

### Installation

```bash
git clone https://github.com/ihsan31415/origami-engine.git
cd origami-engine
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
```

### Quick start

```python
from origami_engine import load_default_creases, build_pattern, plot_pattern

creases = load_default_creases()
pat = build_pattern(creases)
plot_pattern(creases, pat)
```

See the [Examples](##examples) section for more usage snippets.

---

## 📦 As a Library

This project is structured as a **library** for crease pattern simulation and analysis. Core modules live under `origami_engine/`:

| Module | What it does |
|---|---|
| `origami_engine/types.py` | Domain types: `Crease`, `Pattern`, `SimulationResult` |
| `origami_engine/geometry.py` | Reconstruct faces and hinge graph from creases (`build_pattern`) |
| `origami_engine/model.py` | Generate MuJoCo XML from a validated `Pattern` |
| `origami_engine/dynamics.py` | Run simulation, table vibration, compute centroids |
| `origami_engine/evaluation.py` | Fitness APIs: `evaluate_individual()`, `evaluate_population()` |
| `origami_engine/plotting.py` | `plot_pattern()` — reference-style crease pattern visualization |
| `origami_engine/simulation.py` | Facade: high-level `run_simulation()` |
| `origami_engine/serialization.py` | Crease JSON I/O, schema validation, normalization |

### Core usage

```python
from origami_engine import (
    Crease,
    Pattern,
    build_pattern,
    generate_xml,
    run_simulation,
    evaluate_individual,
    evaluate_population,
    plot_pattern,
    load_default_creases,
    load_creases_from_json,
    save_creases_to_json,
)
```

---

## 📦 Installation

```bash
pip install -e ".[dev]"
```

Also installable from PyPI:

```bash
pip install origami-engine
```

---

## 📦 Latest Release

See the [GitHub Releases](https://github.com/ihsan31415/origami-engine/releases/latest) page for the most recent version, changelog, and assets.

---

## 📚 Documentation

- [Architecture](ARCHITECTURE.md) — module overview, data flow, design decisions
- [Changelog](CHANGELOG.md) — version history
- [Experimental history](experiments/TIMELINE.md) — archived Jupyter notebooks
- [Crease pattern visualization](##-crease-pattern-visualization) — `plot_pattern` reference

---

## 🔍 Examples

Runnable usage snippets live in the [`examples/`](examples/README.md) folder:

```bash
python examples/01_evaluate_reference.py
python examples/02_json_input.py
python examples/03_inspect_pattern.py
python examples/04_evaluate_population.py
python examples/05_plot_pattern.py
```

---

## 🔍 Crease pattern visualization

View any crease pattern at a glance with `plot_pattern`:

```python
from origami_engine import build_pattern, load_default_creases, plot_pattern

creases = load_default_creases()  # default reference pattern
pat = build_pattern(creases)  # validate faces / edges
plot_pattern(creases, pat)  # Mountain=red dashed, Valley=blue dash-dot
```

`plot_pattern` draws the sheet between `0.0` and `1.0` on both axes, colours
Mountain folds red dashed and Valley folds blue dash-dot, labels every
crease with its fold angle in degrees, places a gray face index at each
polygon's representative point, marks loop edges with a black `x`, and prints a
title like `"24 creases | 16 faces | 9 loop edges (x)"`.

Run the example script to open the figure interactively:

```bash
python examples/05_plot_pattern.py
```

A pre-rendered version of the default reference pattern is included in the
repository at [`docs/crease_pattern_plot.png`](docs/crease_pattern_plot.png):

<p align="center">
  <img src="docs/crease_pattern_plot.png" alt="Crease pattern plot" width="480" style="border:1px solid #d0d0d0; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.08);" />
</p>

<p align="center"><sub>Default reference crease pattern — 24 creases | 16 faces | 9 loop edges</sub></p>

---

## 🔍 Example crease input

Crease data is represented as a list of line segments with a start point, end point, and target fold angle. Target angles dictate whether a joint behaves as a **Mountain fold** (negative radians) or a **Valley fold** (positive radians).

```python
from origami_engine.simulation import Crease

creases = [
    Crease((0.2, 0.0), (0.45, 0.25), -0.7853981633974483),
    Crease((0.45, 0.25), (0.2, 0.5), -0.7853981633974483),
]
```

### Explicit Mountain-Valley Fold Pairing

Here is an explicit example of a 90-degree Mountain-Valley fold sequence along a shared crease node to create a standard V-shape:

```python
import numpy as np
from origami_engine.simulation import Crease

crease_sequence = [
    # Crease 1: Mountain Fold (-90 degrees in radians)
    Crease(p1=(0.0, 0.5), p2=(0.5, 0.5), angle=-np.pi / 2),
    # Crease 2: Valley Fold (+90 degrees in radians)
    Crease(p1=(0.5, 0.5), p2=(1.0, 0.5), angle=np.pi / 2),
]
```

The project also supports JSON input with the following schema:

```json
{
  "angle_unit": "degree",
  "creases": [
    { "p1": [0.0, 0.5], "p2": [0.5, 0.5], "angle": -90.0 },
    { "p1": [0.5, 0.5], "p2": [1.0, 0.5], "angle": 90.0 }
  ]
}
```

---

## 📊 Evaluation workflow

The project exposes a small evaluation API over the MuJoCo simulation:

```python
from origami_engine.evaluation import evaluate_individual

score = evaluate_individual(
    creases,
    duration=8.0,
    trajectory=(1.0, 0.0, 0.0),
    fold_duration=3.0,
)
print(score)
```

This returns the forward displacement of the paper centroid relative to the requested trajectory direction, measured after the simulated folding run.

---

## 📦 Package data

- `schemas/*.json` — JSON Schema for crease input validation
- `docs/crease_pattern_plot.png` — pre-rendered reference plot
- `examples/` — runnable usage snippets
- `experiments/` — archived prototyping notebooks (`TIMELINE.md` + `prototype_notebooks.zip`)

---

## 👥 Experimental history

This repository also preserves the **experimental stage** of the simulator before it was modularized into `origami_engine/`. These are the historical Jupyter notebooks (not part of the runtime package) that were used to develop the fold physics:

- [`experiments/TIMELINE.md`](experiments/TIMELINE.md) — phase-by-phase prototyping history (contact optimization, viscoelastic tuning, tear fixes, etc.)
- [`experiments/prototype_notebooks.zip`](experiments/prototype_notebooks.zip) — the archived notebook bundle (`GEN_1` … `GEN_4`)

Unzip the archive and run the notebooks locally:

```bash
unzip experiments/prototype_notebooks.zip -d experiments/notebooks
. .venv/bin/activate
pip install jupyter
jupyter notebook experiments/notebooks
```

---

## 📄 License

Distributed under the [Apache License 2.0](LICENSE).

---

## 🤝 Citation

If you use this work in research, please cite:

```
MuJoCo Origami Engine (origami-engine). 
GitHub repository: https://github.com/ihsan31415/origami-engine
```

---

## 📬 Contact

- GitHub: [https://github.com/ihsan31415/origami-engine](https://github.com/ihsan31415/origami-engine)
- Author: ihsan <ihsanmuhammadkhoirul@students.unnes.ac.id>