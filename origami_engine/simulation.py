from __future__ import annotations

"""Stable public facade for the simulation core.

The implementation is split across focused modules:

- :mod:`origami_engine.constants` — physical and solver constants
- :mod:`origami_engine.types` — ``Crease``, ``Pattern``, ``SimulationResult``
- :mod:`origami_engine.geometry` — crease graph and face reconstruction
- :mod:`origami_engine.model` — MuJoCo XML generation
- :mod:`origami_engine.serialization` — crease normalization and JSON I/O
- :mod:`origami_engine.dynamics` — simulation loop, table vibration, centroids

Importing from this module keeps existing code working; new code may import
from the focused modules or from the package root (``origami_engine``).
"""

from .constants import (
    COLL_THICK,
    D_PANEL,
    DAMPING,
    EQ_SOLIMP,
    EQ_SOLREF,
    FORCE_MAX,
    K_PANEL,
    KP,
    KV,
    MAX_FOLD,
    MAX_STRAIN,
    MIN_FACE_AREA,
    MU_PAPER,
    MU_TABLE,
    PAPER_MASS,
    STRETCH_DAMP,
    STRETCH_K,
    STRETCH_MAX,
    THICK,
    VIB_AMP_X,
    VIB_AMP_Z,
    VIB_FREQ,
    Z0,
    M,
    S,
    V,
)
from .dynamics import drive_table, paper_centroid, run_simulation
from .geometry import build_pattern
from .model import generate_xml
from .serialization import load_creases_from_json, normalize_creases, save_creases_to_json
from .types import Crease, Pattern, SimulationResult

__all__ = [
    "COLL_THICK",
    "DAMPING",
    "D_PANEL",
    "EQ_SOLIMP",
    "EQ_SOLREF",
    "FORCE_MAX",
    "KP",
    "KV",
    "K_PANEL",
    "MAX_FOLD",
    "MAX_STRAIN",
    "MIN_FACE_AREA",
    "MU_PAPER",
    "MU_TABLE",
    "PAPER_MASS",
    "STRETCH_DAMP",
    "STRETCH_K",
    "STRETCH_MAX",
    "THICK",
    "VIB_AMP_X",
    "VIB_AMP_Z",
    "VIB_FREQ",
    "Z0",
    "Crease",
    "M",
    "Pattern",
    "S",
    "SimulationResult",
    "V",
    "build_pattern",
    "drive_table",
    "generate_xml",
    "load_creases_from_json",
    "normalize_creases",
    "paper_centroid",
    "run_simulation",
    "save_creases_to_json",
]
