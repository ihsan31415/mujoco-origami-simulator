# Prototyping & Development Timeline

This directory contains the historical evolutionary path of the MuJoCo Origami Simulator prior to its modular refactoring into the core engine. These Jupyter notebooks document the rapid prototyping phases used to isolate physics constraints, manage collision boundaries, tune structural dynamics, and resolve critical mesh deformations (tearing).

## 📅 Evolutionary Timeline

### 🔷 Phase 1: Base Mechanics Exploration
* **Notebook:** `GEN_1_creasing_and_vibrations_simulation_.ipynb`
* **Objective:** Establish baseline crease generation parameters from 2D coordinates.
* **Focus Areas:** 
  * Parsing 2D point arrays into primitive hinges.
  * Validating basic torque actuators for programmatic angle folding.
  * Injecting stochastic noise parameters to evaluate support-table vibration.

### 🔷 Phase 2: Contact Layer Optimization
* **Notebook:** `GEN_2_improving_sim_collision.ipynb`
* **Objective:** Prevent self-intersection artifacts during high-angle folding configurations.
* **Focus Areas:**
  * Tuning MuJoCo collision geometry primitives (`geom` margins and gaps).
  * Overriding global contact solvers to properly isolate adjacent non-rigid paper faces.
  * Eliminating geometry clipping on complex overlay folds.

### 🔷 Phase 3: Viscoelastic Dynamics Tuning
* **Notebook:** `GEN_3_improving_sim_physics_spring,_damp_and_collision_test.ipynb`
* **Objective:** Refine paper structural stiffness and damping behaviors to emulate realistic physical sheets.
* **Focus Areas:**
  * Implementing linear spring coefficients (`stiffness`) across folding hinges.
  * Tuning joint dampening factors (`damping`) to eliminate extreme kinematic oscillations.
  * Co-testing collision robustness against heightened viscoelastic forces.

### 🔷 Phase 4: Production Stabilization & Tear Fixes
* **Notebook:** `GEN_4_optimizing_W_close_successed_to_fix_the_tear.ipynb`
* **Objective:** Rectify catastrophic mesh tearing caused by numerical divergence during extreme close-angle constraints.
* **Focus Areas:**
  * Adjusting constraint solver parameters (`solref` and `solimp`) for high-tension areas.
  * Optimizing localized closure proximity boundaries to seamlessly snap joints without mesh distortion.
  * Formulating the exact mathematical baseline deployed in the production `origami_engine/simulation.py`.

---

## 🛠️ Usage for Archive Inspection
To spin up these historical milestones locally, launch your Jupyter environment within your virtual environment:

```bash
. .venv/bin/activate
pip install jupyter
jupyter notebook
```
