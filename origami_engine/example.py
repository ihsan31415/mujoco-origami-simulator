from __future__ import annotations

import sys
from pathlib import Path

# Allow running this file directly (`python origami_engine/example.py`) as well as
# via `python -m origami_engine.example` from the project root.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from origami_engine.evaluation import evaluate_individual, evaluate_population
from origami_engine.patterns import DEFAULT_PATTERN_JSON, reference_miura_legacy_creases
from origami_engine.simulation import load_creases_from_json

DEFAULT_CREASE_JSON = DEFAULT_PATTERN_JSON


if __name__ == "__main__":
    if DEFAULT_CREASE_JSON.exists():
        creases = load_creases_from_json(DEFAULT_CREASE_JSON)
        print(f"loaded crease pattern from {DEFAULT_CREASE_JSON}")
    else:
        creases = reference_miura_legacy_creases()
        print("loaded embedded legacy reference crease pattern")

    displacement = evaluate_individual(creases, duration=0.5, trajectory=(1.0, 0.0, 0.0))
    print(f"single-individual displacement: {displacement:.6f}")
    print(evaluate_population([creases, creases], duration=0.5, trajectory=(1.0, 0.0, 0.0), workers=1))
