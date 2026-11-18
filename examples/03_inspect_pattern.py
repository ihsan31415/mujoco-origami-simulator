"""Inspect the reconstructed face graph of a crease pattern."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from origami_engine import (
    DEFAULT_PATTERN_JSON,
    build_pattern,
    load_creases_from_json,
    reference_miura_legacy_creases,
)


def main():
    if DEFAULT_PATTERN_JSON.exists():
        creases = load_creases_from_json(DEFAULT_PATTERN_JSON)
        print(f"pattern source: {DEFAULT_PATTERN_JSON.name}")
    else:
        creases = reference_miura_legacy_creases()
        print("pattern source: embedded reference (JSON file not found)")

    pat = build_pattern(creases)
    if not pat.valid:
        print(f"invalid pattern: {pat.reason}")
        return

    hinge_edges = sum(1 for v in pat.tree_edge.values() if v is not None)
    print(f"valid: {pat.valid}")
    print(f"faces: {pat.n_faces}  hinge (tree) edges: {hinge_edges}  loop edges: {pat.n_loops}")
    print(f"root face: {pat.root}  max depth: {max(pat.depth.values())}")


if __name__ == "__main__":
    main()
