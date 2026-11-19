# Architecture — MuJoCo Origami Engine

## Module Overview

The library is organized into focused modules under `origami_engine/`, each with a single responsibility:

| Module | Purpose |
|---|---|
| `constants.py` | Shared physical/solver constants (`S`, `M`, `V`, `MAX_FOLD`, `MIN_FACE_AREA`, `KP`, `KV`, etc.) |
| `types.py` | Domain types: `Crease`, `Pattern`, `SimulationResult` |
| `geometry.py` | Crease graph / face reconstruction (`build_pattern`) — validates tiling, builds polygon faces, identifies loop edges |
| `model.py` | Generate MuJoCo XML from a validated `Pattern` (`generate_xml`) |
| `dynamics.py` | Simulation loop, table vibration, centroid computation (`run_simulation`, `drive_table`, `paper_centroid`) |
| `serialization.py` | Crease normalization and JSON I/O, validated against `crease_pattern.schema.json` |
| `evaluation.py` | Fitness-oriented APIs: `evaluate_individual()`, `evaluate_population()`, `compute_forward_displacement()` |
| `patterns.py` | Reusable reference crease patterns (Miura-ori, etc.) |
| `simulation.py` | Backward-compatible facade for imports |
| `render_individual.py` | Script for rendering a single pattern to MP4/video report |
| `example.py` | Minimal evaluation workflow demo |
| `plotting.py` | `plot_pattern()` — reference-style crease pattern visualization |

## Data Flow

1. **Input** → `creases` list of `Crease` objects (or dicts)
2. **Validate** → `load_creases_from_json()` / `normalize_creases()` — schema validation
3. **Reconstruct** → `build_pattern(creases)` → `Pattern` with faces, edges, loop_edges, `valid` flag
4. **XML Generation** → `generate_xml(pattern)` → MuJoCo XML string
5. **Simulation** → `run_simulation(creases, ...)` → `SimulationResult` (model, data, pattern, info)
6. **Fitness** → `evaluate_individual()` / `evaluate_population()` — forward displacement
7. **Visualization** → `plot_pattern(creases, pat)` — Matplotlib figure with Mountain/Valley colors, face indices, loop-edge markers

## Design Decisions

- **Library-first**: The code is structured as an importable package (`origami_engine`), not a standalone script.
- **Schema-driven**: Crease input is validated against a JSON Schema at load time.
- **Modular simulation**: The dynamics module is decoupled from pattern construction, enabling population-based optimization.
- **Video output**: Simulation renders to MP4 via `imageio` for inspection and presentation.

## Public API Table (summary)

See [API_REFERENCE.md](API_REFERENCE.md) for the complete export table.