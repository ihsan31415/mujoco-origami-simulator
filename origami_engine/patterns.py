from __future__ import annotations

"""Reusable crease-pattern providers for examples, tests, and rendering."""

from pathlib import Path

import numpy as np

from .simulation import Crease, M, V, load_creases_from_json

DEFAULT_PATTERN_JSON = Path(__file__).resolve().parent.parent / "crease_patterns" / "reference_miura_4x4.json"


def reference_miura_legacy_creases():
    """Reference pattern used by legacy evaluation tests and examples."""
    return [
        Crease((0.25, 0.0), (0.3125, 0.25), V),
        Crease((0.3125, 0.25), (0.25, 0.5), V),
        Crease((0.25, 0.5), (0.3125, 0.75), V),
        Crease((0.3125, 0.75), (0.25, 1.0), V),
        Crease((0.5, 0.0), (0.5625, 0.25), M),
        Crease((0.5625, 0.25), (0.5, 0.5), M),
        Crease((0.5, 0.5), (0.5625, 0.75), M),
        Crease((0.5625, 0.75), (0.5, 1.0), M),
        Crease((0.75, 0.0), (0.8125, 0.25), V),
        Crease((0.8125, 0.25), (0.75, 0.5), V),
        Crease((0.75, 0.5), (0.8125, 0.75), V),
        Crease((0.8125, 0.75), (0.75, 1.0), V),
        Crease((0.0, 0.25), (0.3125, 0.25), V),
        Crease((0.3125, 0.25), (0.5625, 0.25), M),
        Crease((0.5625, 0.25), (0.8125, 0.25), V),
        Crease((0.8125, 0.25), (1.0, 0.25), M),
        Crease((0.0, 0.5), (0.25, 0.5), M),
        Crease((0.25, 0.5), (0.5, 0.5), V),
        Crease((0.5, 0.5), (0.75, 0.5), M),
        Crease((0.75, 0.5), (1.0, 0.5), V),
        Crease((0.0, 0.75), (0.3125, 0.75), V),
        Crease((0.3125, 0.75), (0.5625, 0.75), M),
        Crease((0.5625, 0.75), (0.8125, 0.75), V),
        Crease((0.8125, 0.75), (1.0, 0.75), M),
    ]


def reference_miura_render_creases():
    """Reference pattern tuned for current rendering workflow."""
    return [
        Crease((0.2, 0.0), (0.45, 0.25), V),
        Crease((0.45, 0.25), (0.2, 0.5), V),
        Crease((0.2, 0.5), (0.45, 0.75), V),
        Crease((0.45, 0.75), (0.2, 1.0), V),
        Crease((0.45, 0.0), (0.7, 0.25), M),
        Crease((0.7, 0.25), (0.45, 0.5), M),
        Crease((0.45, 0.5), (0.7, 0.75), M),
        Crease((0.7, 0.75), (0.45, 1.0), M),
        Crease((0.7, 0.0), (0.95, 0.25), V),
        Crease((0.95, 0.25), (0.7, 0.5), V),
        Crease((0.7, 0.5), (0.95, 0.75), V),
        Crease((0.95, 0.75), (0.7, 1.0), V),
        Crease((0.0, 0.25), (0.45, 0.25), V),
        Crease((0.45, 0.25), (0.7, 0.25), M),
        Crease((0.7, 0.25), (0.95, 0.25), V),
        Crease((0.95, 0.25), (1.0, 0.25), M),
        Crease((0.0, 0.5), (0.2, 0.5), M),
        Crease((0.2, 0.5), (0.45, 0.5), V),
        Crease((0.45, 0.5), (0.7, 0.5), M),
        Crease((0.7, 0.5), (1.0, 0.5), V),
        Crease((0.0, 0.75), (0.45, 0.75), V),
        Crease((0.45, 0.75), (0.7, 0.75), M),
        Crease((0.7, 0.75), (0.95, 0.75), V),
        Crease((0.95, 0.75), (1.0, 0.75), M),
    ]


def load_default_creases():
    """Load default crease pattern from JSON when available, else fallback."""
    if DEFAULT_PATTERN_JSON.exists():
        return load_creases_from_json(DEFAULT_PATTERN_JSON)
    return reference_miura_render_creases()


__all__ = [
    "DEFAULT_PATTERN_JSON",
    "load_default_creases",
    "reference_miura_legacy_creases",
    "reference_miura_render_creases",
]
