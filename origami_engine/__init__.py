"""Origami simulation package.

Public entry points are grouped into:

- simulation domain/model construction in `geometry`, `model`, `dynamics`
- fitness/evaluation interfaces in `evaluation`
- reusable reference inputs in `patterns`
- crease input normalization in `serialization`
"""

from .constants import (
    MAX_FOLD,
    PAPER_MASS,
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
from .evaluation import compute_forward_displacement, evaluate_individual, evaluate_population
from .geometry import build_pattern
from .model import generate_xml
from .patterns import (
    DEFAULT_PATTERN_JSON,
    load_default_creases,
    reference_miura_legacy_creases,
    reference_miura_render_creases,
)
from .serialization import CREASE_SCHEMA, load_creases_from_json, normalize_creases, save_creases_to_json
from .types import Crease, Pattern, SimulationResult

__version__ = "0.1.0"

__all__ = [
    "CREASE_SCHEMA",
    "DEFAULT_PATTERN_JSON",
    "MAX_FOLD",
    "PAPER_MASS",
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
    "compute_forward_displacement",
    "drive_table",
    "evaluate_individual",
    "evaluate_population",
    "generate_xml",
    "load_creases_from_json",
    "load_default_creases",
    "normalize_creases",
    "paper_centroid",
    "reference_miura_legacy_creases",
    "reference_miura_render_creases",
    "run_simulation",
    "save_creases_to_json",
]
