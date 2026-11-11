# MuJoCo Origami Simulator

This project is a Python-based origami folding simulator built around MuJoCo. It reconstructs a crease pattern from 2D line segments, validates the paper topology, generates a MuJoCo model for the folded sheet, applies fold-angle targets, and optionally vibrates the support table to simulate a realistic folding environment.

The code is structured as an engineering pipeline rather than a pure toy example: crease patterns are normalized into a canonical format, polygon faces are built from the sheet layout, MuJoCo XML is generated from the resulting pattern, and the net displacement of the paper is measured as a forward-folding fitness signal.

## What this project does

- Builds a crease network from `p1`, `p2`, and `angle` data
- Verifies that the crease graph tiles the square sheet without invalid sliver faces
- Creates a MuJoCo model from the pattern geometry and hinge constraints
- Drives fold actuators toward target fold angles during simulation
- Applies a small support-table vibration for dynamic motion
- Measures the forward displacement of the paper centroid
- Exports the rendered motion to video for inspection

## Core modules

- `origami_engine/simulation.py` — authoritative simulation logic, crease model, MuJoCo XML generation, and stepping code
- `origami_engine/evaluation.py` — single-individual and batch evaluation entry points
- `origami_engine/patterns.py` — reusable reference crease patterns and JSON defaults
- `origami_engine/render_individual.py` — script for rendering a single pattern to an MP4/video report
- `tests/test_evaluation.py` — regression checks for evaluation, input validation, and JSON I/O

## Project layout

```text
.
├── origami_engine/
│   ├── __init__.py
│   ├── simulation.py
│   ├── evaluation.py
│   ├── patterns.py
│   ├── render_individual.py
│   └── example.py
├── crease_patterns/
│   └── reference_miura_4x4.json
├── tests/
│   └── test_evaluation.py
├── ARCHITECTURE.md
├── individual_simulation.mp4
├── render_report.json
├── render_report.md
├── README.md
└── schema/
```

## Requirements

This project depends on:

- Python
- MuJoCo
- NumPy
- Shapely
- imageio
- pytest

A local virtual environment is used in the repo (`.venv`), and the project is designed to run as a package-friendly Python workspace rather than a packaged pip install.

## Quick start

Create a virtual environment and install the runtime dependencies you need, then run the validation or rendering scripts.

```bash
python -m venv .venv
. .venv/bin/activate
pip install numpy shapely imageio mujoco pytest

python -m pytest -q tests
python origami_engine/render_individual.py
```

## Example crease input

Crease data is represented as a list of line segments with a start point, end point, and target fold angle:

```python
from origami_engine.simulation import Crease

creases = [
    Crease((0.2, 0.0), (0.45, 0.25), -0.7853981633974483),
    Crease((0.45, 0.25), (0.2, 0.5), -0.7853981633974483),
]
```

The project also supports JSON input with the following schema:

```json
{
  "angle_unit": "degree",
  "creases": [
    {"p1": [0.2, 0.0], "p2": [0.45, 0.25], "angle": -45.0}
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

The simulator is built around real paper topology and MuJoCo dynamics. It is not just a geometric crease renderer; it creates a physical model that can be evaluated and visualized under controlled fold and vibration conditions.

For implementation details and module responsibilities, see [ARCHITECTURE.md](ARCHITECTURE.md).
