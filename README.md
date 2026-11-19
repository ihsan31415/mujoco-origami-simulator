<h1 align="center">MuJoCo Origami Engine</h1>

<div align="center">
  <a href="https://github.com/ihsan31415/origami-engine/releases"><img src="https://img.shields.io/github/v/release/ihsan31415/origami-engine?display_name=tag&logo=github" alt="Latest Release"></a>
  <a href="https://github.com/ihsan31415/origami-engine/actions/workflows/ci.yml"><img src="https://github.com/ihsan31415/origami-engine/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11-blue?logo=python&logoColor=white" alt="Python"></a>
  <a href="https://mujoco.org/"><img src="https://img.shields.io/badge/Physics-MuJoCo-blue" alt="MuJoCo"></a>
  <a href="https://numpy.org/"><img src="https://img.shields.io/badge/NumPy-Scientific%20Computing-013243?logo=numpy&logoColor=white" alt="NumPy"></a>
  <a href="https://shapely.readthedocs.io/"><img src="https://img.shields.io/badge/Geometry-Shapely-3776AB" alt="Shapely"></a>
  <br>
  <a href="https://github.com/python/mypy"><img src="https://img.shields.io/badge/Type%20Checking-mypy-blue?logo=python&logoColor=white" alt="mypy"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/badge/Code%20Style-Ruff-D7FF64?logo=ruff&logoColor=black" alt="Ruff"></a>
  <a href="https://docs.pytest.org/"><img src="https://img.shields.io/badge/Tests-pytest-0A9EDC?logo=pytest&logoColor=white" alt="pytest"></a>
  <a href="origami_engine/schemas/crease_pattern.schema.json"><img src="https://img.shields.io/badge/Validation-JSON%20Schema-green" alt="JSON Schema"></a>
  <a href="https://github.com/pre-commit/pre-commit"><img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white" alt="pre-commit"></a>
  <br>
  <a href="https://github.com/ihsan31415/origami-engine/commits/main"><img src="https://img.shields.io/github/last-commit/ihsan31415/origami-engine" alt="Last Commit"></a>
  <a href="https://github.com/ihsan31415/origami-engine/issues"><img src="https://img.shields.io/github/issues/ihsan31415/origami-engine" alt="Issues"></a>
  <a href="https://github.com/ihsan31415/origami-engine/stargazers"><img src="https://img.shields.io/github/stars/ihsan31415/origami-engine" alt="Stars"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/ihsan31415/origami-engine" alt="License"></a>
</div>

This project is a Python-based origami folding simulator built around MuJoCo. It reconstructs a crease pattern from 2D line segments, validates the paper topology, generates a MuJoCo model for the folded sheet, applies fold-angle targets, and optionally vibrates the support table to simulate a realistic folding environment. The code is structured as an **engineering library** rather than a pure toy example.

## Simulation Output
Below is the physical rendering of the simulation output, demonstrating how the paper layout reacts to active hinge joint torques and support table vibrations:

<!-- Image on top of the table -->
<p align="center">
  <img src="docs/crease_pattern_plot.png" alt="Reference crease pattern" width="300" style="border:1px solid #d0d0d0; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.08);" />
</p>
<p align="center"><sub>Default reference crease pattern — 24 creases | 16 faces | 9 loop edges</sub></p>

<table>
  <tr>
    <th>Vibrating Table: Amplitude & Frequency</th>
    <th>Fold Crease</th>
    <th>Video Preview</th>
  </tr>
  <tr>
    <td><strong>Lower</strong> amplitude & frequency</td>
    <td>Partial / standard</td>
    <td>
      <video src="https://github.com/user-attachments/assets/15ff98b3-7a72-46c2-9303-e106c88bc71a"
             width="280" controls muted playsinline></video>
    </td>
  </tr>
  <tr>
    <td><strong>High</strong> amplitude & frequency</td>
    <td>Full</td>
    <td>
      <video src="https://github.com/user-attachments/assets/ef7d9808-d0a5-4c6b-b33c-2c6a81e11003"
             width="280" controls muted playsinline></video>
    </td>
  </tr>
  <tr>
    <td><strong>Higher</strong> amplitude & frequency</td>
    <td>Full</td>
    <td>
      <video src="https://github.com/user-attachments/assets/438714c1-f831-43cb-a729-027816fb3ea5"
             width="280" controls muted playsinline></video>
    </td>
  </tr>
</table>

<!-- Another table: image left, description right, referencing JSON -->
<table>
  <tr>
    <td style="vertical-align: top; padding-right: 20px;">
      <p align="center">
        <img src="docs/crease_pattern_plot.png" alt="Reference crease pattern" width="250" style="border:1px solid #d0d0d0; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.08);" />
      </p>
      <p align="center"><sub>24 creases | 16 faces | 9 loop edges</sub></p>
    </td>
    <td>
      <strong>Reference Crease Pattern</strong><br>
      This table shows the default Miura-ori crease pattern used in simulations. The pattern consists of 24 creases that tile a square sheet, forming 16 polygonal faces with 9 loop edges. <br><br>
      <a href="origami_engine/schemas/crease_pattern.schema.json"><strong>Crease Pattern JSON Schema</strong></a> — validates the structure of crease input files (angle units, point coordinates, mountain/valley signs).<br>
      <a href="crease_patterns/reference_miura_4x4.json"><strong>reference_miura_4x4.json</strong></a> — the actual crease pattern data in JSON format, containing the p1, p2, and angle values for each of the 24 creases.<br><br>
      <em>Mountain folds are negative angles (creasing "up"), Valley folds are positive angles (creasing "down").</em>
    </td>
  </tr>
</table>

This project is a Python-based origami folding simulator built around MuJoCo. It reconstructs a crease pattern from 2D line segments, validates the paper topology, generates a MuJoCo model for the folded sheet, applies fold-angle targets, and optionally vibrates the support table to simulate a realistic folding environment. The code is structured as an **engineering library** rather than a pure toy example.

## Core modules
- `origami_engine/constants.py` — shared physical/solver constants
- `origami_engine/types.py` — `Crease`, `Pattern`, `SimulationResult` domain types
- `origami_engine/geometry.py` — crease graph / face reconstruction (`build_pattern`)
- `origami_engine/model.py` — MuJoCo XML generation (`generate_xml`)
- `origami_engine/dynamics.py` — simulation loop, table vibration, centroids (`run_simulation`, `drive_table`, `paper_centroid`)
- `origami_engine/serialization.py` — crease normalization and JSON I/O (validated against the packaged JSON Schema via `jsonschema`)
- `origami_engine/evaluation.py` — fitness-oriented APIs (`evaluate_individual`, `evaluate_population`)
- `origami_engine/patterns.py` — reusable reference crease patterns
- `origami_engine/simulation.py` — backward-compatible facade
- `origami_engine/render_individual.py` — script for rendering a single pattern to an MP4/video report
- `origami_engine/example.py` — minimal evaluation workflow
- `tests/test_evaluation.py` — regression checks for evaluation, input validation, and JSON I/O

## Project layout
```text
.
├── origami_engine/
│   ├── __init__.py
│   ├── backend.py
│   ├── constants.py
│   ├── types.py
│   ├── geometry.py
│   ├── model.py
│   ├── dynamics.py
│   ├── serialization.py
│   ├── schemas/
│   │   └── crease_pattern.schema.json
│   ├── evaluation.py
│   ├── patterns.py
│   ├── simulation.py       # facade for backward-compatible imports
│   ├── render_individual.py
│   └── example.py
├── examples/
│   ├── README.md
│   ├── 01_evaluate_reference.py
│   ├── 02_json_input.py
│   ├── 03_inspect_pattern.py
│   └── 04_evaluate_population.py
├── crease_patterns/
│   └── reference_miura_4x4.json
├── experiments/
│   ├── TIMELINE.md
│   └── prototype_notebooks.zip
├── tests/
│   └── test_evaluation.py
├── .github/workflows/ci.yml
├── ARCHITECTURE.md
├── individual_simulation.mp4
├── pyproject.toml
└── README.md
```

## Requirements
Runtime dependencies are declared in `pyproject.toml` (MuJoCo, NumPy, Shapely, imageio, jsonschema) and installed with:
```bash
pip install -e ".[dev]"
```
which also adds `pytest` for running the test suite. The package is importable as `origami_engine` after installation.

## Quick start
Create a virtual environment and install the package with development dependencies, then run the validation or rendering scripts.
```bash
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
python -m pytest -q tests
python origami_engine/render_individual.py
```

## Library API

```bash
pip install -e ".[dev]"

python -c "
from origami_engine import (
    CREASE_SCHEMA,
    Crease,
    build_pattern,
    evaluate_individual,
    evaluate_population,
    load_creases_from_json,
    normalize_creases,
    reference_miura_legacy_creases,
    save_creases_to_json,
    run_simulation,
    paper_centroid,
)
"
```

A machine‑readable JSON Schema describing the crease input format is included at
`origami_engine/schemas/crease_pattern.schema.json`. It is used by
`load_creases_from_json` to validate files at load time (invalid files raise
`ValueError`), and is also exposed as `origami_engine.CREASE_SCHEMA` for
validation in your own tools before calling the library.

## API Reference

### Domain types

| Export | Description |
|---|---|
| `Crease` | A single crease segment with `p1`, `p2` (2D points) and `angle` (radians). Negative = Mountain, positive = Valley. |
| `Pattern` | Validated face/edge graph from `build_pattern()`. Contains `faces`, `edges`, `loop_edges`, `valid`, `reason`, `n_faces`, `n_loops`. |
| `SimulationResult` | Result of `run_simulation()`: `model`, `data`, `pattern`, `info`, centroids. |
| `CREASE_SCHEMA` | JSON Schema for validating crease input files. |

### Pattern construction

| Export | Description |
|---|---|
| `build_pattern(creases)` | Reconstruct polygonal faces and the spanning-tree hinge graph from a crease list. Returns a `Pattern`. |
| `load_default_creases()` | Load the default reference crease pattern from JSON, with fallback to the built-in Miura-ori. |
| `load_creases_from_json(path)` | Load and validate creases from a JSON file. |
| `save_creases_to_json(creases, path)` | Save creases to a JSON file. |
| `normalize_creases(creases)` | Normalize raw crease inputs (dicts or `Crease` objects) into `Crease` instances. |
| `reference_miura_legacy_creases()` | Legacy Miura-ori crease list. |
| `reference_miura_render_creases()` | Render-tuned Miura-ori crease list. |

### Simulation

| Export | Description |
|---|---|
| `run_simulation(creases, ...)` | Run a MuJoCo simulation from creases and return a `SimulationResult`. |
| `generate_xml(pattern)` | Generate MuJoCo XML from a validated `Pattern`. |
| `drive_table(...)` | Apply support-table vibration during simulation. |
| `paper_centroid(data)` | Compute the paper centroid from MuJoCo data. |

### Evaluation

| Export | Description |
|---|---|
| `evaluate_individual(creases, ...)` | Score a single crease pattern via forward displacement. |
| `evaluate_population(creases_list, ...)` | Score a population of crease patterns, optionally in parallel. |
| `compute_forward_displacement(...)` | Compute forward displacement from simulation data. |

### Visualization

| Export | Description |
|---|---|
| `plot_pattern(creases, pat=None)` | Plot a crease pattern: Mountain=crimson dashed, Valley=blue dash-dot, degree labels, face indices, loop-edge markers, legend. |

### Constants

| Export | Description |
|---|---|
| `S` | Sheet size (1.0). |
| `M`, `V` | Canonical Mountain (negative) and Valley (positive) fold angles (±45°). |
| `MAX_FOLD`, `MIN_FACE_AREA`, `KP`, `KV`, ... | Physical and solver constants. |

### Example: complete workflow

```python
from origami_engine import load_default_creases, build_pattern, plot_pattern, run_simulation

creases = load_default_creases()
pat = build_pattern(creases)

# Visualize
plot_pattern(creases, pat)

# Simulate
result = run_simulation(creases, duration=8.0)
print(result.info["n_faces"], "faces simulated")
```

## Examples

Runnable usage snippets live in the [`examples/`](examples/README.md) folder:

```bash
python examples/01_evaluate_reference.py
python examples/02_json_input.py
python examples/03_inspect_pattern.py
python examples/04_evaluate_population.py
python examples/05_plot_pattern.py
```


## Crease pattern visualization

View any crease pattern at a glance with `plot_pattern`:

```python
from origami_engine import build_pattern, load_default_creases, plot_pattern

creases = load_default_creates()  # default reference pattern
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

## Experimental history

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

## Example crease input
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

## Evaluation workflow
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

## Notes
The simulator is built around real paper topology and MuJoCo dynamics. It is not just a geometric crease renderer; it creates a physical model that can be evaluated and visualized under controlled fold and vibration conditions. For implementation details and module responsibilities, see [ARCHITECTURE.md](ARCHITECTURE.md).