# Architecture

The MuJoCo Origami Simulator is structured as an engineering pipeline rather
than a pure toy example. Crease patterns are normalized into a canonical
format, polygon faces are built from the sheet layout, MuJoCo XML is
generated from the resulting pattern, and the net displacement of the paper
centroid is measured as a forward-folding fitness signal.

## Module overview

All runtime code lives under [`origami_engine/`](origami_engine/). Each module
has a single responsibility:

| Module | Responsibility |
|---|---|
| `types.py` | Core domain types: `Crease`, `Pattern`, `SimulationResult` |
| `constants.py` | Physical and solver constants shared across the engine |
| `backend.py` | Optional MuJoCo import guard (lets modules be imported/tested without MuJoCo) |
| `geometry.py` | Reconstruct polygonal faces and the spanning-tree hinge graph from creases |
| `model.py` | Assemble MuJoCo XML model from a validated `Pattern` |
| `dynamics.py` | Run MuJoCo simulation, drive table vibration, compute centroid displacement |
| `simulation.py` | Facade: high-level `run_simulation()` wrapping geometry → model → dynamics |
| `evaluation.py` | Fitness API: `evaluate_individual()`, `evaluate_population()` |
| `serialization.py` | Crease JSON I/O, schema validation, `Crease` normalization |
| `patterns.py` | Reusable reference crease patterns (Miura-ori etc.) |
| `plotting.py` | `plot_pattern()` — reference-style crease pattern visualization |
| `render_individual.py` | Render a single simulation to video (MP4 / GIF fallback) |
| `example.py` | Minimal end-to-end example |

## Data flow

```
crease JSON / crease list
        │
        ▼
serialization.normalize_creases()   → list[Crease]
        │
        ▼
geometry.build_pattern()            → Pattern (faces, edges, tree, loops)
        │
        ├─► plotting.plot_pattern() → figure (visual inspection)
        │
        ▼
model.generate_xml()                → MuJoCo XML string + info dict
        │
        ▼
dynamics.run_simulation()           → SimulationResult (model, data, centroids)
        │
        ▼
evaluation.*                        → fitness score / population scores
```

## Key design decisions

- **Optional MuJoCo import**: `backend.py` isolates the `mujoco` import so
  geometry, serialization, and plotting modules can be imported and unit-tested
  without MuJoCo installed. `require_mujoco()` raises a helpful error if a
  MuJoCo-dependent operation is attempted when it is unavailable.
- **Signed fold angles**: Mountain folds carry negative angles, Valley folds
  positive angles. `constants.M` and `constants.V` are the canonical ±45°
  references.
- **Pattern validation**: `build_pattern()` checks for sliver faces, correct
  tiling area, and connected face graphs before producing a valid `Pattern`.
- **Facade layer**: `simulation.py` re-exports the most-used symbols so
  consumers can `from origami_engine import run_simulation` without importing
  every submodule directly.

## Public API

The package's public surface is curated in `origami_engine/__init__.py`.
Consumers should import from the package root, not from submodules directly:

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
