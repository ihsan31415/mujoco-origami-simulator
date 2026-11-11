from __future__ import annotations

from pathlib import Path

from origami_engine.evaluation import evaluate_individual, evaluate_population
from origami_engine.patterns import reference_miura_legacy_creases
from origami_engine.simulation import load_creases_from_json


DEFAULT_CREASE_JSON = Path(__file__).with_name("crease_patterns") / "reference_miura_4x4.json"


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
