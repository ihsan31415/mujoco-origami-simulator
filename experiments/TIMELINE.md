# Experimental Timeline

This folder preserves the **prototyping stage** of the MuJoCo Origami Simulator,
before the code was modularized into `origami_engine/`. The four Jupyter
notebooks document how the physics was discovered and tuned: crease generation,
collision handling, spring/damping behavior, and the fixes that stopped the paper
mesh from tearing.

The notebooks are **archived, not executed**. They are not required to run the
simulator and are not imported by the package.

## Contents

| File | What it is |
|---|---|
| [`prototype_notebooks.zip`](prototype_notebooks.zip) | The four original prototyping notebooks (`GEN_1` … `GEN_4`), zipped to keep the repository light |
| `TIMELINE.md` | This document — the phase-by-phase history |

## Timeline

### Phase 1 — Base mechanics exploration
**Notebook:** `GEN_1_creasing_and_vibrations_simulation_.ipynb`

- Parse 2D point arrays into primitive hinges.
- Validate basic torque actuators for programmatic angle folding.
- Inject stochastic noise parameters to evaluate support-table vibration.

### Phase 2 — Contact layer optimization
**Notebook:** `GEN_2_improving_sim_collision.ipynb`

- Prevent self-intersection artifacts during high-angle folds.
- Tune MuJoCo collision primitives (`geom` margins and gaps).
- Override global contact solvers to isolate adjacent non-rigid paper faces.

### Phase 3 — Viscoelastic dynamics tuning
**Notebook:** `GEN_3_improving_sim_physics_spring,_damp_and_collision_test.ipynb`

- Add linear spring coefficients (`stiffness`) across folding hinges.
- Tune joint damping to remove extreme kinematic oscillations.
- Stress-test collision robustness against heightened viscoelastic forces.

### Phase 4 — Production stabilization and tear fixes
**Notebook:** `GEN_4_optimizing_W_close_successed_to_fix_the_tear.ipynb`

- Fix mesh tearing caused by numerical divergence at extreme close angles.
- Adjust constraint solver parameters (`solref`, `solimp`) for high-tension areas.
- Snap joints closed without distorting the mesh.

Phase 4 is the baseline that became the current engine. The tuned values now live
in [`origami_engine/constants.py`](../origami_engine/constants.py) and the model
assembly in [`origami_engine/model.py`](../origami_engine/model.py).

## Inspecting the notebooks

Unzip the archive locally (the extracted folder is git-ignored):

```bash
unzip experiments/prototype_notebooks.zip -d experiments/notebooks
. .venv/bin/activate
pip install jupyter
jupyter notebook experiments/notebooks
```

## See also

- [`README.md`](../README.md) — project overview and quick start
- [`ARCHITECTURE.md`](../ARCHITECTURE.md) — current module layout and data flow
