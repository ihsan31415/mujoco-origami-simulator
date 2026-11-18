"""Save creases to JSON and load them back for reproducible inputs."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from origami_engine import (
    evaluate_individual,
    load_creases_from_json,
    reference_miura_legacy_creases,
    save_creases_to_json,
)


def main():
    creases = reference_miura_legacy_creases()

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "reference_creases.json"
        save_creases_to_json(creases, out, angle_unit="degree")
        print(f"wrote {out.name} ({out.stat().st_size} bytes)")

        loaded = load_creases_from_json(out)

    print(f"loaded {len(loaded)} creases; first angle: {loaded[0].angle:.6f} rad")
    score = evaluate_individual(loaded, duration=0.5, trajectory=(1.0, 0.0, 0.0))
    print(f"forward displacement: {score:.6f}")


if __name__ == "__main__":
    main()
