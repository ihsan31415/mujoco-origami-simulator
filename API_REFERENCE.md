# API Reference — MuJoCo Origami Engine

## Domain types

| Export | Description |
|---|---|
| `Crease` | A single crease segment with `p1`, `p2` (2D points) and `angle` (radians). Negative = Mountain, positive = Valley. |
| `Pattern` | Validated face/edge graph from `build_pattern()`. Contains `faces`, `edges`, `loop_edges`, `valid`, `reason`, `n_faces`, `n_loops`. |
| `SimulationResult` | Result of `run_simulation()`: `model`, `data`, `pattern`, `info`, centroids. |
| `CREASE_SCHEMA` | JSON Schema for validating crease input files. |

## Pattern construction

| Export | Description |
|---|---|
| `build_pattern(creases)` | Reconstruct polygonal faces and the spanning-tree hinge graph from a crease list. Returns a `Pattern`. |
| `load_default_creases()` | Load the default reference crease pattern from JSON, with fallback to the built-in Miura-ori. |
| `load_creases_from_json(path)` | Load and validate creases from a JSON file. |
| `save_creases_to_json(creases, path)` | Save creases to a JSON file. |
| `normalize_creases(creases)` | Normalize raw crease inputs (dicts or `Crease` objects) into `Crease` instances. |
| `reference_miura_legacy_creases()` | Legacy Miura-ori crease list. |
| `reference_miura_render_creases()` | Render-tuned Miura-ori crease list. |

## Simulation

| Export | Description |
|---|---|
| `run_simulation(creases, ...)` | Run a MuJoCo simulation from creases and return a `SimulationResult`. |
| `generate_xml(pattern)` | Generate MuJoCo XML from a validated `Pattern`. |
| `drive_table(...)` | Apply support-table vibration during simulation. |
| `paper_centroid(data)` | Compute the paper centroid from MuJoCo data. |

## Evaluation

| Export | Description |
|---|---|
| `evaluate_individual(creases, ...)` | Score a single crease pattern via forward displacement. |
| `evaluate_population(creases_list, ...)` | Score a population of crease patterns, optionally in parallel. |
| `compute_forward_displacement(...)` | Compute forward displacement from simulation data. |

## Visualization

| Export | Description |
|---|---|
| `plot_pattern(creases, pat=None)` | Plot a crease pattern: Mountain=crimson dashed, Valley=blue dash-dot, degree labels, face indices, loop-edge markers, legend. |

## Constants

| Export | Description |
|---|---|
| `S` | Sheet size (1.0). |
| `M`, `V` | Canonical Mountain (negative) and Valley (positive) fold angles (±45°). |
| `MAX_FOLD`, `MIN_FACE_AREA`, `KP`, `KV`, ... | Physical and solver constants. |

## Example: complete workflow

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