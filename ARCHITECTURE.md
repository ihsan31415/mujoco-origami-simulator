# Architecture Overview

## Module layout

- `origami_engine/constants.py` — shared physical/solver constants.
- `origami_engine/types.py` — `Crease`, `Pattern`, `SimulationResult` domain types.
- `origami_engine/backend.py` — optional MuJoCo import guard (private).
- `origami_engine/geometry.py` — crease graph / face reconstruction (`build_pattern`).
- `origami_engine/model.py` — MuJoCo XML generation (`generate_xml`).
- `origami_engine/dynamics.py` — simulation loop, table vibration, centroids (`run_simulation`, `drive_table`, `paper_centroid`).
- `origami_engine/serialization.py` — crease normalization and JSON I/O (`normalize_creases`, `load_creases_from_json`, `save_creases_to_json`), validated against the packaged schema in `origami_engine/schemas/` via `jsonschema`.
- `origami_engine/evaluation.py` — fitness-oriented APIs (`evaluate_individual`, `evaluate_population`, `compute_forward_displacement`).
- `origami_engine/patterns.py` — reusable reference crease patterns and default JSON path.
- `origami_engine/simulation.py` — backward-compatible facade re-exporting the core surface.
- `origami_engine/__init__.py` — curated public package exports (library-style imports).
- `origami_engine/render_individual.py` — visual validation entry point.
- `origami_engine/example.py` — minimal evaluation workflow for single and population runs.

Entry points unchanged:
- `render_individual.py` — visual validation workflow.
- `example.py` — minimal evaluation workflow.

## Compatibility layer

- `origami_simulation.py` and root `evaluation.py` were removed in the modularization; import from `origami_engine` instead. The `origami_engine.simulation` facade re-exports every name they previously provided.

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

- Tests: `. .venv/bin/activate && python -m pytest tests -q`
- Example run: `. .venv/bin/activate && python origami_engine/example.py`
- Render run: `. .venv/bin/activate && python origami_engine/render_individual.py`
- Usage examples: `. .venv/bin/activate && python examples/01_evaluate_reference.py`
