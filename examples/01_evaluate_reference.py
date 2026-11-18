"""Evaluate the reference Miura pattern and print its fitness score."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from origami_engine import evaluate_individual, reference_miura_legacy_creases


def main():
    creases = reference_miura_legacy_creases()
    score = evaluate_individual(
        creases,
        duration=1.0,
        trajectory=(1.0, 0.0, 0.0),
        fold_duration=0.5,
    )
    print(f"forward displacement: {score:.6f}")


if __name__ == "__main__":
    main()
