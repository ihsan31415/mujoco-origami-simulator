from __future__ import annotations

"""Crease input normalization and JSON (de)serialization."""

import json
from importlib import resources
from pathlib import Path

import jsonschema
import numpy as np

from .types import Crease


def _load_schema():
    """Read the packaged JSON Schema for crease input."""
    schema_path = resources.files(__package__) / "schemas" / "crease_pattern.schema.json"
    with resources.as_file(schema_path) as path:
        return json.loads(path.read_text())


CREASE_SCHEMA = _load_schema()


def load_creases_from_json(path):
    """Load a crease pattern from JSON.

    The file may be either a bare list of crease objects or an object with a
    ``creases`` key and an optional ``angle_unit`` (``radian`` or ``degree``).
    Payloads are validated against the packaged JSON Schema; a
    :class:`ValueError` is raised when the structure is invalid.
    """
    path_obj = Path(path)
    payload = json.loads(path_obj.read_text())

    try:
        jsonschema.validate(instance=payload, schema=CREASE_SCHEMA)
    except jsonschema.ValidationError as exc:
        raise ValueError(f"invalid crease JSON: {exc.message}") from exc

    if isinstance(payload, list):
        crease_items = payload
        angle_unit = "radian"
    else:
        crease_items = payload["creases"]
        angle_unit = str(payload.get("angle_unit", "radian")).strip().lower()

    use_degrees = angle_unit in {"degree", "degrees", "deg"}
    creases = []
    for idx, item in enumerate(crease_items):
        try:
            p1 = tuple(float(v) for v in item["p1"])
            p2 = tuple(float(v) for v in item["p2"])
            angle = float(item["angle"])
        except KeyError as exc:
            raise ValueError(f"crease entry at index {idx} missing key: {exc}") from exc

        if use_degrees:
            angle = float(np.deg2rad(angle))
        creases.append(Crease(p1, p2, angle))
    return creases


def save_creases_to_json(creases, path, angle_unit="radian"):
    """Save a crease pattern to JSON for reproducible pipeline inputs."""
    unit = str(angle_unit).strip().lower()
    if unit not in {"radian", "degree"}:
        raise ValueError("angle_unit must be 'radian' or 'degree'.")

    normalized = normalize_creases(creases)
    payload = {
        "angle_unit": unit,
        "creases": [],
    }
    for c in normalized:
        angle = float(c.angle if unit == "radian" else np.rad2deg(c.angle))
        payload["creases"].append(
            {
                "p1": [float(c.p1[0]), float(c.p1[1])],
                "p2": [float(c.p2[0]), float(c.p2[1])],
                "angle": angle,
            }
        )

    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2))
    return out


def normalize_creases(creases):
    """Coerce supported crease inputs into a list of :class:`Crease` objects.

    Accepts a JSON file path, a list of ``Crease`` objects, or a list of dicts
    with ``p1``, ``p2`` and ``angle`` keys.
    """
    if creases is None:
        raise ValueError("creases must not be None.")
    if isinstance(creases, (str, Path)):
        return load_creases_from_json(creases)
    if not isinstance(creases, (list, tuple)):
        raise TypeError("creases must be a list or tuple of Crease objects.")
    if len(creases) == 0:
        raise ValueError("creases must contain at least one crease.")

    normalized = []
    for idx, crease in enumerate(creases):
        if isinstance(crease, Crease):
            normalized.append(crease)
            continue
        if isinstance(crease, dict):
            try:
                p1 = tuple(crease["p1"])
                p2 = tuple(crease["p2"])
                angle = float(crease["angle"])
            except KeyError as exc:
                raise ValueError(f"crease at index {idx} is missing required keys: {exc}") from exc
            normalized.append(Crease(p1, p2, angle))
            continue
        raise ValueError(f"crease at index {idx} is not a valid Crease object or dict.")
    return normalized


__all__ = ["CREASE_SCHEMA", "load_creases_from_json", "normalize_creases", "save_creases_to_json"]
