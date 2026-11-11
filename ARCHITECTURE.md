# Architecture Overview

## Module layout

- `origami_engine/simulation.py`
  - Core domain + simulation mechanics.
  - Defines `Crease`, `Pattern`, `SimulationResult`.
  - Reconstructs crease graphs/faces, builds MuJoCo XML, drives table vibration, runs simulation.
  - Owns shared physical/config constants and JSON crease I/O.

- `origami_engine/evaluation.py`
  - Fitness-oriented APIs:
    - `evaluate_individual(...)`
    - `evaluate_population(...)`
  - Keeps trajectory projection and batch orchestration separate from simulation internals.

- `origami_engine/patterns.py`
  - Reusable reference crease providers and default JSON path.
  - Prevents duplication across scripts/tests.

- `origami_engine/__init__.py`
  - Public package exports for library-style imports.

## Entry points

- `render_individual.py`
  - Visual validation workflow.
  - Loads crease JSON (default `crease_patterns/reference_miura_4x4.json`) and renders MP4.

- `example.py`
  - Minimal evaluation workflow for single and population runs.

## Compatibility layer

- `origami_simulation.py` and `evaluation.py` are compatibility wrappers.
- Existing imports continue working, but implementation now lives under `origami_engine/`.

## Input format

Crease patterns can be supplied as:
1. A list of `Crease` objects.
2. A list of dictionaries with `p1`, `p2`, `angle`.
3. A JSON file path accepted by `normalize_creases(...)`.

JSON schema:

```json
{
  "angle_unit": "degree",
  "creases": [
    {"p1": [0.2, 0.0], "p2": [0.45, 0.25], "angle": -180.0}
  ]
}
```

## Validation commands

- Tests: `./.venv/bin/python -m pytest tests/test_evaluation.py -q`
- Example run: `./.venv/bin/python example.py`
- Render run: `./.venv/bin/python render_individual.py`
