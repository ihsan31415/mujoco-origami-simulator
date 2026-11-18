"""Score a small population of crease patterns, sequentially or in parallel."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from origami_engine import evaluate_population, reference_miura_legacy_creases


def main():
    # Same pattern repeated so the example is deterministic; swap in distinct
    # individuals (e.g. genomes decoded into creases) for a real search.
    population = [reference_miura_legacy_creases() for _ in range(3)]

    scores = evaluate_population(
        population,
        duration=0.5,
        trajectory=(1.0, 0.0, 0.0),
        workers=1,  # set >1 to use a process pool
        error_policy="nan",
    )
    for i, score in enumerate(scores):
        print(f"individual {i}: {score}")


if __name__ == "__main__":
    main()
