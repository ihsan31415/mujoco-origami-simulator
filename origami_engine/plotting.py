"""Crease-pattern plotting utilities.

Reference-style line plot of a crease pattern:

- Background sheet rectangle (0,0)-(S,S), light gray fill, black edge
- Mountain folds (angle < 0): crimson dashed lines
- Valley folds (angle > 0): royal blue dash-dot lines
- Each crease labelled with its fold angle in degrees at its midpoint
- Face indices drawn in gray at each polygon's representative point
- Loop edges marked with black "x" at their midpoints
- Legend at lower centre; axes limited to [-0.05S, 1.05S] with equal aspect
- Title: "{N} creases | {M} faces | {K} loop edges (x)"

Supports two calling conventions:

1. ``plot_pattern(creases)`` — plot from a raw crease list.
2. ``plot_pattern(creases, pat)`` — plot from a validated :class:`Pattern`.
"""

from __future__ import annotations

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from .constants import S
from .types import Crease, Pattern


def plot_pattern(creases: list[Crease], pat: Pattern | None = None) -> None:
    """Plot a crease pattern.

    Parameters
    ----------
    creases:
        List of :class:`~origami_engine.types.Crease` objects describing the
        crease segments.
    pat:
        Optional :class:`~origami_engine.types.Pattern` object returned by
        :func:`~origami_engine.geometry.build_pattern`.  When provided and
        valid, face indices and loop-edge markers are added to the axes and
        the title includes the face/loop-edge counts.

    Returns
    -------
    None
        The figure is displayed with :func:`matplotlib.pyplot.show`.  Under a
        non-interactive backend (e.g. Agg) ``show()`` does not block, so
        callers can still grab the current figure via
        :func:`matplotlib.pyplot.gcf` and save it to PNG.

    Notes
    -----
    The visual style matches the reference plot:

    - **Mountain** folds → crimson dashed lines
    - **Valley** folds → royal blue dash-dot lines
    - Crease labels → actual fold angle in degrees at each midpoint
    - Face numbers → gray at each polygon's representative point
    - Loop edges → black "x" at each edge midpoint
    - Axes → limits [-0.05S, 1.05S] × [-0.05S, 1.05S], equal aspect
    - Legend → Mountain / Valley at lower centre
    - Title → ``"{N} creases | {M} faces | {K} loop edges (x)"`` when *pat*
      is valid, otherwise ``"{N} creases [ | INVALID: reason]"``
    """
    _fig, ax = plt.subplots(figsize=(6, 6))
    ax.add_patch(Rectangle((0, 0), S, S, fc="#f4f4f4", ec="k", lw=2))

    for c in creases:
        valley = c.angle > 0
        ax.plot(
            [c.p1[0], c.p2[0]],
            [c.p1[1], c.p2[1]],
            color="royalblue" if valley else "crimson",
            ls="-." if valley else "--",
            lw=2.5,
        )
        m = ((c.p1[0] + c.p2[0]) / 2, (c.p1[1] + c.p2[1]) / 2)
        ax.text(
            m[0],
            m[1],
            f"{np.degrees(abs(c.angle)):.0f}°",
            fontsize=8,
            ha="center",
            bbox={"fc": "white", "ec": "none", "alpha": 0.7, "pad": 1},
        )

    title = f"{len(creases)} creases"
    if pat is not None and pat.valid:
        faces = pat.faces or []
        edges = pat.edges or []
        loop_edges = pat.loop_edges or []
        for i, f in enumerate(faces):
            p = f.representative_point()
            ax.text(p.x, p.y, str(i), color="gray", ha="center", fontsize=9)
        for k in loop_edges:
            e = edges[k]
            ax.plot(
                (e["p"][0] + e["q"][0]) / 2,
                (e["p"][1] + e["q"][1]) / 2,
                "kx",
                ms=9,
            )
        title += f" | {len(faces)} faces | {len(loop_edges)} loop edges (x)"
    elif pat is not None:
        title += f" | INVALID: {pat.reason}"

    ax.legend(
        handles=[
            Line2D([], [], color="crimson", ls="--", label="Mountain"),
            Line2D([], [], color="royalblue", ls="-.", label="Valley"),
        ],
        loc="lower center",
        ncol=2,
        bbox_to_anchor=(0.5, -0.12),
    )
    ax.set_xlim(-0.05 * S, 1.05 * S)
    ax.set_ylim(-0.05 * S, 1.05 * S)
    ax.set_aspect("equal")
    ax.set_title(title, fontsize=10)
    plt.show()
