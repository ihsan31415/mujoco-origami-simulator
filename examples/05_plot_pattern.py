"""Plot the default crease pattern and save a PNG for the docs.

Run from the repository root:

    python examples/05_plot_pattern.py
"""
from __future__ import annotations

from pathlib import Path

from origami_engine import build_pattern, load_default_creases, plot_pattern


def main() -> None:
    creases = load_default_creases()
    pat = build_pattern(creases)

    # Save a PNG next to this script for quick viewing, then show the plot.
    out = Path(__file__).with_suffix(".png")
    import matplotlib.pyplot as plt

    plot_pattern(creases, pat)
    if plt.get_fignums():
        plt.savefig(out, dpi=150, bbox_inches="tight")
        plt.close("all")
        print(f"Saved plot to {out}")


if __name__ == "__main__":
    main()