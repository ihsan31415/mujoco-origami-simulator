# MuJoCo Origami Simulator

This project is a Python-based origami folding simulator built around MuJoCo. It reconstructs a crease pattern from 2D line segments, validates the paper topology, generates a MuJoCo model for the folded sheet, applies fold-angle targets, and optionally vibrates the support table to simulate a realistic folding environment. The code is structured as an engineering pipeline rather than a pure toy example: crease patterns are normalized into a canonical format, polygon faces are built from the sheet layout, MuJoCo XML is generated from the resulting pattern, and the net displacement of the paper is measured as a forward-folding fitness signal.

## What this project does
- Builds a crease network from `p1`, `p2`, and `angle` data
- Verifies that the crease graph tiles the square sheet without invalid sliver faces
- Creates a MuJoCo model from the pattern geometry and hinge constraints
- Drives fold actuators toward target fold angles during simulation
- Applies a small support-table vibration for dynamic motion
- Measures the forward displacement of the paper centroid
- Exports the rendered motion to video for inspection

## Simulation Output
Below is the physical rendering of the simulation output, demonstrating how the paper layout reacts to active hinge joint torques and support table vibrations:

<video src="individual_simulation.mp4" width="100%" controls title="MuJoCo Origami Simulation Loop"></video>

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
├── schema/
│   ├── SCHEMA.md
│   └── GEN_EXPERIMENTS.zip
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

## Examples

Runnable usage snippets live in the [`examples/`](examples/README.md) folder:

```bash
python examples/01_evaluate_reference.py
python examples/02_json_input.py
python examples/03_inspect_pattern.py
python examples/04_evaluate_population.py
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
    Crease(p1=(0.5, 0.5), p2=(1.0, 0.5), angle=np.pi / 2)
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
