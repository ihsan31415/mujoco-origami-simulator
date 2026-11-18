from __future__ import annotations

"""Simulation execution: build the model, step MuJoCo, track the paper."""

import numpy as np

from .backend import require_mujoco
from .constants import VIB_AMP_X, VIB_AMP_Z, VIB_FREQ
from .geometry import build_pattern
from .model import generate_xml
from .serialization import normalize_creases
from .types import SimulationResult


def drive_table(model, data, t, amp_x=VIB_AMP_X, amp_z=VIB_AMP_Z, freq_hz=VIB_FREQ):
    """Kinemetically drive the support table with a sinusoidal vibration."""
    w = 2 * np.pi * freq_hz
    jx, jz = model.joint("table_x"), model.joint("table_z")
    data.qpos[jx.qposadr[0]] = amp_x * np.sin(w * t)
    data.qvel[jx.dofadr[0]] = amp_x * w * np.cos(w * t)
    data.qpos[jz.qposadr[0]] = amp_z * np.sin(w * t)
    data.qvel[jz.dofadr[0]] = amp_z * w * np.cos(w * t)


def paper_centroid(model, data):
    """Mean XY position of all non-table geoms (the paper sheet)."""
    table_id = model.body("table").id
    ids = [g for g in range(model.ngeom) if model.geom_bodyid[g] != table_id]
    if not ids:
        raise ValueError("No paper geoms were found in the MuJoCo model.")
    points = np.asarray(data.geom_xpos[ids, :3], dtype=float)
    if points.size == 0:
        raise ValueError("Simulation geometry is empty.")
    return points[:, :2].mean(axis=0)


# Backward-compatible private alias.
_paper_centroid = paper_centroid


def run_simulation(
    creases,
    duration=8.0,
    fold_duration=3.0,
    vibrate=True,
    amp_x=VIB_AMP_X,
    amp_z=VIB_AMP_Z,
    freq_hz=VIB_FREQ,
):
    """Run the fold simulation and return final MuJoCo state plus centroid data."""
    mujoco = require_mujoco("MuJoCo is required to run the simulation.")
    if duration <= 0:
        raise ValueError("duration must be positive.")

    normalized = normalize_creases(creases)
    pat = build_pattern(normalized)
    if not pat.valid:
        raise ValueError(f"invalid crease pattern: {pat.reason}")

    xml, info = generate_xml(pat, normalized)
    model = mujoco.MjModel.from_xml_string(xml)
    data = mujoco.MjData(model)

    initial_centroid = paper_centroid(model, data)
    target_angles = np.asarray(info["targets"], dtype=float)
    hinge_adr = np.array([model.joint(h["name"]).qposadr[0] for h in info["hinges"]], dtype=int)
    if len(hinge_adr):
        data.qpos[hinge_adr] = 0.0

    while data.time < duration:
        t = min(data.time / fold_duration, 1.0)
        s = t * t * (3 - 2 * t)
        data.ctrl[:] = s * target_angles
        if vibrate:
            drive_table(model, data, data.time, amp_x=amp_x, amp_z=amp_z, freq_hz=freq_hz)
        mujoco.mj_step(model, data)

    if not np.isfinite(data.qpos).all():
        raise FloatingPointError("unstable simulation: non-finite joint coordinates produced.")

    final_centroid = paper_centroid(model, data)
    return SimulationResult(
        model=model,
        data=data,
        pattern=pat,
        info=info,
        initial_centroid=initial_centroid,
        final_centroid=final_centroid,
    )


__all__ = ["drive_table", "paper_centroid", "run_simulation"]
