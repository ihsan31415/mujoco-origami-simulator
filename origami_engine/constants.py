from __future__ import annotations

"""Physical and solver constants shared across the engine."""

import numpy as np

# Sheet geometry and mass
S = 1.0
THICK = 0.0001
PAPER_MASS = 0.2
Z0 = THICK + 0.001

# Pattern validation
MIN_FACE_AREA = 1e-4 * S * S
MAX_FOLD = np.pi * 0.98

# Hinge actuation and panels
KP, KV, DAMPING, FORCE_MAX = 2.0, 0.15, 0.003, 2.0
MU_PAPER = 0.3
MU_TABLE = 0.5

# Table vibration
VIB_FREQ = 75.0
VIB_AMP_X = 0.0
VIB_AMP_Z = 0.0013

# Constraint solver tuning
EQ_SOLREF = "0.005 1"
EQ_SOLIMP = "0.95 0.99 0.001"
STRETCH_K = 5.0e4
STRETCH_DAMP = 50.0
STRETCH_MAX = 1.0e-4
K_PANEL = 1e5
D_PANEL = 50.0
MAX_STRAIN = 0.005
COLL_THICK = THICK * 0.1

# Canonical mountain/valley angles
V = np.deg2rad(-45)
M = np.deg2rad(45)

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
    "M",
    "S",
    "V",
]
