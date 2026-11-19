# Getting Started — MuJoCo Origami Engine

## Installation

### As a Library (recommended)
```bash
# Clone the repository
git clone https://github.com/ihsan31415/origami-engine.git
cd origami-engine

# Create and activate a virtual environment
python -m venv .venv
. .venv/bin/activate

# Install with development dependencies (pytest, ruff, mypy, pre-commit)
pip install -e ".[dev]"
```

### As a Script-Only Usage
```bash
# Minimal install without dev tools
pip install origami-engine
```

## Quick Start — Library Usage

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

### Load a reference pattern
```python
creases = load_default_creases()  # or load_creases_from_json("path/to/file.json")
```

### Build and validate the pattern
```python
pat = build_pattern(creases)
# pat.valid == True if the crease graph tiles the sheet correctly
```

### Run a simulation
```python
result = run_simulation(creases, duration=8.0)
print(f"{result.info['n_faces']} faces simulated in {result.info['duration']}s")
```

### Evaluate fitness (forward displacement)
```python
score = evaluate_individual(
    creases,
    duration=8.0,
    trajectory=(1.0, 0.0, 0.0),
    fold_duration=3.0,
)
print(f"Forward displacement: {score}")
```

### Plot the crease pattern
```python
from origami_engine import plot_pattern

plot_pattern(creases, pat)
```

## Quick Start — Script Usage

```bash
# 1. Create venv and install
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"

# 2. Run the validation suite
python -m pytest -q tests

# 3. Render a single pattern to MP4
python origami_engine/render_individual.py

# 4. Or run an example script
python examples/01_evaluate_reference.py
python examples/02_json_input.py
python examples/03_inspect_pattern.py
python examples/04_evaluate_population.py
python examples/05_plot_pattern.py
```

## Example Crease Input

Crease data is represented as a list of line segments:

```python
from origami_engine.simulation import Crease

creases = [
    Crease((0.2, 0.0), (0.45, 0.25), -0.7853981633974483),  # Mountain fold
    Crease((0.45, 0.25), (0.2, 0.5), -0.7853981633974483),  # Mountain fold
]
```

### Mountain-Valley Pairing Example
```python
import numpy as np
from origami_engine.simulation import Crease

crease_sequence = [
    # Crease 1: Mountain Fold (-90 degrees)
    Crease(p1=(0.0, 0.5), p2=(0.5, 0.5), angle=-np.pi / 2),
    # Crease 2: Valley Fold (+90 degrees)
    Crease(p1=(0.5, 0.5), p2=(1.0, 0.5), angle=np.pi / 2),
]
```

## JSON Input Schema

Creases can be loaded from JSON following this schema:
```json
{
  "angle_unit": "degree",
  "creases": [
    { "p1": [0.0, 0.5], "p2": [0.5, 0.5], "angle": -90.0 },
    { "p1": [0.5, 0.5], "p2": [1.0, 0.5], "angle": 90.0 }
  ]
}
```

## What's Next?

- Browse the [examples/](examples/) folder for runnable snippets
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for module details
- See [API_REFERENCE.md](API_REFERENCE.md) for the full public API
- View the [experimental history](experiments/TIMELINE.md) for prototyping notes