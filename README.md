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

<!-- Image left + description right referencing JSON -->
<table>
  <tr>
    <td style="vertical-align: top; padding-right: 20px;">
      <p align="center">
        <img src="docs/crease_pattern_plot.png" alt="Reference crease pattern" width="300" style="border:1px solid #d0d0d0; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.08);" />
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

<!-- Video table (eyecatching) -->
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

*This repository is structured as a **library** for crease pattern simulation and analysis. For full documentation, see the dedicated files below.*

## 📖 Documentation

For in-depth information, see the dedicated documentation files:

- **[GETTING_STARTED.md](GETTING_STARTED.md)** — installation, quick start tutorials, example crease input
- **[API_REFERENCE.md](API_REFERENCE.md)** — full public API exports, domain types, and constants
- **[ARCHITECTURE.md](ARCHITECTURE.md)** — module overview, data flow, and design decisions

*The README provides a brief overview and the simulation output (the eyecatching feature). All technical content is available in the dedicated documentation files.*

## Core modules (brief)

- `origami_engine/constants.py` — shared physical/solver constants
- `origami_engine/types.py` — `Crease`, `Pattern`, `SimulationResult` domain types
- `origami_engine/geometry.py` — crease graph / face reconstruction (`build_pattern`)
- `origami_engine/model.py` — MuJoCo XML generation (`generate_xml`)
- `origami_engine/dynamics.py` — simulation loop, table vibration, centroids
- `origami_engine/evaluation.py` — fitness APIs (`evaluate_individual`, `evaluate_population`)
- `origami_engine/patterns.py` — reusable reference crease patterns
- `origami_engine/render_individual.py` — render to MP4/video report
- `origami_engine/example.py` — minimal evaluation workflow

## Quick start

Install from PyPI with `pip` or `uv`:

### Using pip
```bash
python -m venv .venv
. .venv/bin/activate
pip install origami-engine[dev]
```

### Using uv (recommended, faster)
```bash
uv pip install origami-engine[dev]
```

### Without creating a venv (quick test)
```bash
pip install origami-engine
```

### After installation, run the validation suite:
```bash
python -m pytest -q tests
python origami_engine/render_individual.py
```

*For detailed installation steps, environment management, and usage tutorials, see [GETTING_STARTED.md](GETTING_STARTED.md).*

## Library API (brief)

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

*For the complete API reference, see [API_REFERENCE.md](API_REFERENCE.md).*
