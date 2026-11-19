"""Crease-pattern plotting utilities.

Produces reference-style line plots of crease patterns with:
- Red dashed lines for Mountain folds (negative angles)
- Blue dash-dot lines for Valley folds (positive angles)
- Face numbers centered in each polygon
- 180° labels on every crease
- Legend, axis 0.0–1.0
- Title with crease/face/loop counts

Supports two calling conventions:

1. ``plot_pattern(creases)`` — plot from a raw crease list.
2. ``plot_pattern(creases, pat)`` — plot from a :class:`~origami_engine.types.Pattern`
   object (recommended, enables face indices and loop-edge counts in the title).
"""
from __future__ import annotations

from matplotlib import pyplot as plt

from .types import Pattern


def _is_mountain(angle: float) -> bool:
    """Mountain folds have a negative signed angle in this package."""
    return angle < 0


def _is_valley(angle: float) -> bool:
    """Valley folds have a positive signed angle in this package."""
    return angle > 0


def _plot_creases(ax, creases) -> None:
    """Draw every crease on *ax*, coloured by fold type.

    Mountain folds → red dashed, Valley folds → blue dash-dot, others → grey solid.
    """
    for cr in creases:
        x0, y0 = cr.p1
        x1, y1 = cr.p2
        if _is_mountain(cr.angle):
            ax.plot([x0, x1], [y0, y1], linestyle="--", color="red", linewidth=2)
        elif _is_valley(cr.angle):
            ax.plot([x0, x1], [y0, y1], linestyle="-.", color="blue", linewidth=2)
        else:
            ax.plot([x0, x1], [y0, y1], color="gray", linewidth=1)


def _plot_face_numbers(ax, faces) -> None:
    """Print the face index at the centroid of each polygon."""
    for i, face in enumerate(faces):
        cx, cy = face.centroid.xy
        ax.text(cx[0], cy[0], str(i), ha="center", va="center", fontsize=10, color="black", weight="bold")


def _plot_angle_labels(ax, creases) -> None:
    """Print a fixed 180° label at the midpoint of every crease."""
    for cr in creases:
        x0, y0 = cr.p1
        x1, y1 = cr.p2
        mx, my = (x0 + x1) / 2.0, (y0 + y1) / 2.0
        ax.text(mx, my, "180°", fontsize=7, ha="center", va="center", color="black")


def _add_manual_legend(ax) -> None:
    """Add a legend showing the Mountain / Valley line styles."""
    from matplotlib.lines import Line2D

    legend_handles = [
        Line2D([0], [0], color="red", linestyle="--", linewidth=2, label="Mountain"),
        Line2D([0], [0], color="blue", linestyle="-.", linewidth=2, label="Valley"),
    ]
    ax.legend(handles=legend_handles, loc="upper right", fontsize=9)


def plot_pattern(creases, pat: Pattern | None = None) -> None:
    """Plot a crease pattern.

    Parameters
    ----------
    creases:
        List of :class:`~origami_engine.types.Crease` objects describing the
        crease segments.
    pat:
        Optional :class:`~origami_engine.types.Pattern` object returned by
        :func:`~origami_engine.geometry.build_pattern`.  If provided, the
        plot title will include the face count, loop-edge count, and the
        valid/invalid status, and face indices are drawn in each polygon.

    Returns
    -------
    None
        The function displays the plot via ``plt.show()``.  To save the
        figure, call ``plt.savefig`` before ``plt.show`` or close the
        figure with ``plt.close``.

    Notes
    -----
    The visual style matches the reference plot:

    - **Mountain** folds → red dashed lines
    - **Valley** folds → blue dash-dot lines
    - Face numbers → centered in each polygon, rendered in bold black
    - Crease labels → a fixed ``180°`` at each crease midpoint
    - Axes → limits ``[0, 1]`` × ``[0, 1]``, equal aspect, axes hidden
    - Legend → distinguishes Mountain vs. Valley
    - Title → ``"{N} creases | {M} faces | {K} loop edges ({status})"`` when
      *pat* is given, otherwise ``"{N} creases"``

    Example
    -------
    >>> from origami_engine import load_default_creases, build_pattern, plot_pattern
    >>> creases = load_default_creases()
    >>> pat = build_pattern(creases)
    >>> plot_pattern(creases, pat)  # doctest: +SKIP
    """
    _fig, ax = plt.subplots(figsize=(8, 8))

    # Draw crease lines and their 180° labels
    _plot_creases(ax, creases)
    _plot_angle_labels(ax, creases)

    # Draw face numbers and build a title with counts if we have a Pattern
    if pat is not None and pat.faces is not None:
        _plot_face_numbers(ax, pat.faces)

        n_creases = len(creases)
        n_faces = pat.n_faces if pat.n_faces else len(pat.faces)
        n_loops = pat.n_loops if pat.n_loops else (len(pat.loop_edges) if pat.loop_edges else 0)
        status = "valid" if pat.valid else "invalid"
        ax.set_title(f"{n_creases} creases | {n_faces} faces | {n_loops} loop edges ({status})", fontsize=13)
    else:
        ax.set_title(f"{len(creases)} creases", fontsize=13)

    # Axis formatting to match the reference 0.0–1.0 view
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")

    # Add legend
    _add_manual_legend(ax)

    plt.tight_layout()
    plt.show()