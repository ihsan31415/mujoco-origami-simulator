"""Plot the default crease pattern and save a PNG for the docs.

Run from the repository root:

    python examples/05_plot_pattern.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt

from origami_engine import build_pattern, load_default_creases, plot_pattern


def main() -> None:
    creases = load_default_creases()
    pat = build_pattern(creases)

    # Draw the pattern (Agg backend: show() does not block).
    plot_pattern(creases, pat)

    # Save a PNG next to this script for quick viewing (gitignored).
    out = Path(__file__).resolve().parent / "05_plot_pattern.png"
    fig = plt.gcf()
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved plot to {out}")


if __name__ == "__main__":
    main()
