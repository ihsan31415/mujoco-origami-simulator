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

## 🚀 Getting Started

### As a Library
```bash
pip install -e ".[dev]"
```

```python
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
```

### As a Script / Quick Start
```bash
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
python -m pytest -q tests
python origami_engine/render_individual.py
```

*This repository is structured as a **library** for crease pattern simulation and analysis. See the documentation below for more details.*

## 📖 Documentation

For in-depth information, see the dedicated documentation files:

- **[ARCHITECTURE.md](ARCHITECTURE.md)** — module overview, data flow, and design decisions
- **[API Reference](API_REFERENCE.md)** — full public API exports, domain types, and constants
- **[Getting Started Guide](GETTING_STARTED.md)** — detailed installation and usage tutorials
- **[Changelog](CHANGELOG.md)** — version history
- **[Experimental history](experiments/TIMELINE.md)** — archived Jupyter notebooks

*The full API, module details, and advanced usage are available in the dedicated documentation files above. The README provides a brief overview and getting started path.*

## 📦 Core concepts (brief)

- **Crease patterns**: Defined by `p1`, `p2` (2D points) and `angle` (radians). Negative = Mountain, positive = Valley.
- **Simulation**: MuJoCo-based physics with support table vibration and centroid tracking.
- **Evaluation**: Forward displacement measurement as fitness signal.
- **Visualization**: `plot_pattern()` for reference-style crease pattern plots.

*For the complete list of modules, requirements, and API exports, refer to the dedicated documentation files.*