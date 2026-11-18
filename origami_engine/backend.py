from __future__ import annotations

"""MuJoCo import guard.

Keeping the optional import in one place lets geometry and I/O modules be
imported (and unit-tested) without MuJoCo installed.
"""

try:
    import mujoco
except Exception as exc:  # pragma: no cover - import-time guard for clarity
    mujoco = None
    MUJOCO_IMPORT_ERROR = exc
else:
    MUJOCO_IMPORT_ERROR = None


def require_mujoco(message: str = "MuJoCo is required for this operation."):
    """Return the imported ``mujoco`` module or raise a helpful RuntimeError."""
    if mujoco is None:
        raise RuntimeError(message) from MUJOCO_IMPORT_ERROR
    return mujoco


__all__ = ["MUJOCO_IMPORT_ERROR", "mujoco", "require_mujoco"]
