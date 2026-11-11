"""Backward-compatible import shim for the legacy top-level evaluation entry point."""

from origami_engine.evaluation import (
    _as_trajectory_vector,
    compute_forward_displacement,
    evaluate_individual,
    evaluate_population,
)

__all__ = [
    "_as_trajectory_vector",
    "compute_forward_displacement",
    "evaluate_individual",
    "evaluate_population",
]
