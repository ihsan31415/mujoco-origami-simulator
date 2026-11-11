from __future__ import annotations

"""Evaluation interfaces for single-individual and batch fitness runs."""

import math
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from .simulation import VIB_AMP_X, VIB_AMP_Z, VIB_FREQ, normalize_creases, run_simulation


def _as_trajectory_vector(trajectory):
    if trajectory is None:
        return np.asarray([1.0, 0.0, 0.0], dtype=float)

    arr = np.asarray(trajectory, dtype=float)
    if arr.ndim == 0:
        raise ValueError("trajectory must be a direction vector or a sequence of points.")
    if arr.ndim == 1:
        if arr.size not in (2, 3):
            raise ValueError("direction vectors must have length 2 or 3.")
        direction = arr.astype(float)
    elif arr.ndim == 2:
        if arr.shape[0] < 2:
            raise ValueError("trajectory waypoint arrays require at least two points.")
        direction = arr[-1] - arr[0]
    else:
        raise ValueError("trajectory must be a vector or 2D waypoint array.")

    norm = np.linalg.norm(direction)
    if not math.isfinite(norm) or norm <= 0.0:
        raise ValueError("trajectory direction must be non-zero and finite.")
    return direction / norm


def compute_forward_displacement(sim_result, trajectory=(1.0, 0.0, 0.0)):
    direction = _as_trajectory_vector(trajectory)
    initial = np.asarray(sim_result.initial_centroid, dtype=float)
    final = np.asarray(sim_result.final_centroid, dtype=float)
    delta = final - initial

    if direction.size == 2:
        delta_2d = np.asarray([delta[0], delta[1]], dtype=float)
        return float(np.dot(delta_2d, direction))

    delta_3d = np.zeros(3, dtype=float)
    delta_3d[:2] = delta
    return float(np.dot(delta_3d, direction))


def evaluate_individual(
    creases,
    duration=8.0,
    trajectory=(1.0, 0.0, 0.0),
    fold_duration=3.0,
    vibrate=True,
    amp_x=VIB_AMP_X,
    amp_z=VIB_AMP_Z,
    freq_hz=VIB_FREQ,
    return_details=False,
):
    """Evaluate one crease configuration and return net forward displacement."""
    if duration <= 0:
        raise ValueError("duration must be positive.")

    normalized = normalize_creases(creases)
    sim_result = run_simulation(
        normalized,
        duration=duration,
        fold_duration=fold_duration,
        vibrate=vibrate,
        amp_x=amp_x,
        amp_z=amp_z,
        freq_hz=freq_hz,
    )
    displacement = compute_forward_displacement(sim_result, trajectory=trajectory)

    if return_details:
        return {
            "displacement": float(displacement),
            "initial_centroid": np.asarray(sim_result.initial_centroid, dtype=float),
            "final_centroid": np.asarray(sim_result.final_centroid, dtype=float),
            "duration": float(duration),
            "trajectory": np.asarray(_as_trajectory_vector(trajectory), dtype=float),
            "n_faces": int(sim_result.pattern.n_faces),
            "n_loops": int(len(sim_result.pattern.loop_edges or [])),
        }
    return float(displacement)


def _evaluate_worker(item, duration, trajectory, fold_duration, vibrate, amp_x, amp_z, freq_hz):
    return evaluate_individual(
        item,
        duration=duration,
        trajectory=trajectory,
        fold_duration=fold_duration,
        vibrate=vibrate,
        amp_x=amp_x,
        amp_z=amp_z,
        freq_hz=freq_hz,
    )


def evaluate_population(
    individuals,
    duration=8.0,
    trajectory=(1.0, 0.0, 0.0),
    fold_duration=3.0,
    vibrate=True,
    amp_x=VIB_AMP_X,
    amp_z=VIB_AMP_Z,
    freq_hz=VIB_FREQ,
    workers=1,
    error_policy="raise",
):
    """Evaluate a list of GA individuals in sequence or parallel."""
    if workers is None or workers <= 1:
        results = []
        for i, item in enumerate(individuals):
            try:
                results.append(
                    evaluate_individual(
                        item,
                        duration=duration,
                        trajectory=trajectory,
                        fold_duration=fold_duration,
                        vibrate=vibrate,
                        amp_x=amp_x,
                        amp_z=amp_z,
                        freq_hz=freq_hz,
                    )
                )
            except Exception as exc:  # pragma: no cover - exercised by tests via explicit raise
                if error_policy == "raise":
                    raise RuntimeError(f"individual {i} failed during evaluation: {exc}") from exc
                results.append(float("nan"))
        return results

    max_workers = max(1, min(workers, len(individuals) if individuals else 1))
    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        futures = []
        for i, item in enumerate(individuals):
            futures.append(
                (
                    i,
                    pool.submit(
                        _evaluate_worker,
                        item,
                        duration,
                        trajectory,
                        fold_duration,
                        vibrate,
                        amp_x,
                        amp_z,
                        freq_hz,
                    ),
                )
            )

        results = [float("nan")] * len(individuals)
        for i, future in futures:
            try:
                results[i] = future.result()
            except Exception as exc:
                if error_policy == "raise":
                    raise RuntimeError(f"individual {i} failed during evaluation: {exc}") from exc
        return results


__all__ = [
    "_as_trajectory_vector",
    "compute_forward_displacement",
    "evaluate_individual",
    "evaluate_population",
]
