from __future__ import annotations

"""MuJoCo XML generation from a validated crease pattern."""

import numpy as np

from .backend import require_mujoco
from .constants import (
    DAMPING,
    EQ_SOLIMP,
    EQ_SOLREF,
    FORCE_MAX,
    KP,
    KV,
    MAX_FOLD,
    MU_PAPER,
    MU_TABLE,
    PAPER_MASS,
    S,
    STRETCH_DAMP,
    STRETCH_K,
    STRETCH_MAX,
    THICK,
    Z0,
)
from .geometry import _triangles
from shapely.geometry import Point


def _prism(tri, O, thick=None):
    """Triangular prism vertex list."""
    t = THICK if thick is None else thick
    v = []
    for x, y in np.asarray(tri)[:, :2]:
        v += [x - O[0], y - O[1], -t, x - O[0], y - O[1], t]
    return " ".join(f"{a:.6f}" for a in v)


def generate_xml(pat, creases, name="origami_free", coll_thick=None):
    """Build a MuJoCo XML string for a pattern.

    Parameters
    ----------
    pat : Pattern
        Validated pattern produced by :func:`origami_engine.geometry.build_pattern`.
    creases : list[Crease]
        Normalized creases, used to look up target fold angles.
    coll_thick : float | None
        ``None`` keeps the baseline single-geom behavior. A value enables thin
        collision mode with separate visual and collision geoms.
    """
    require_mujoco("MuJoCo is required to build the simulation model.")

    faces, edges = pat.faces, pat.edges
    n = len(faces)
    density = PAPER_MASS / (S * S * 2 * THICK)
    mats = ["paper_A", "paper_B"]

    children = {i: [] for i in range(n)}
    for v, u in pat.parent.items():
        if u is not None:
            children[u].append(v)

    origin = {}
    for v in range(n):
        if v == pat.root:
            c = faces[v].centroid
            origin[v] = (c.x, c.y)
        else:
            origin[v] = edges[pat.tree_edge[v]]["p"]

    mesh_lines, body_lines, hinges = [], [], []

    def emit(i, depth):
        ind = "    " * (depth + 2)
        if i == pat.root:
            pos = (origin[i][0] - S / 2, origin[i][1] - S / 2, Z0)
        else:
            po = origin[pat.parent[i]]
            pos = (origin[i][0] - po[0], origin[i][1] - po[1], 0.0)
        body_lines.append(f'{ind}<body name="face_{i}" pos="{pos[0]:.6f} {pos[1]:.6f} {pos[2]:.6f}">')

        if i == pat.root:
            body_lines.append(f'{ind}    <freejoint name="root"/>')
        else:
            e = edges[pat.tree_edge[i]]
            p, q = np.array(e["p"]), np.array(e["q"])
            a = (q - p) / np.linalg.norm(q - p)
            nl = np.array([-a[1], a[0]])
            left = faces[i].intersects(Point(*((p + q) / 2 + 1e-4 * nl)))
            sgn = 1.0 if left else -1.0
            ang = creases[e["crease"]].angle if e["crease"] >= 0 else 0.0
            h = len(hinges)
            hinges.append(
                dict(
                    name=f"crease_{h}",
                    face=i,
                    edge=pat.tree_edge[i],
                    target=float(np.clip(sgn * ang, -MAX_FOLD, MAX_FOLD)),
                )
            )
            for tag, ax_ in (("a", a), ("n", nl)):
                body_lines.append(
                    f'{ind}    <joint name="stretch_{tag}_{h}" type="slide" '
                    f'axis="{ax_[0]:.6f} {ax_[1]:.6f} 0" stiffness="{STRETCH_K}" '
                    f'damping="{STRETCH_DAMP}" armature="0.001" '
                    f'range="{-STRETCH_MAX} {STRETCH_MAX}" '
                    f'solreflimit="0.002 1" solimplimit="0.99 0.999 0.0001"/>'
                )
            body_lines.append(
                f'{ind}    <joint name="crease_{h}" type="hinge" pos="0 0 0" '
                f'axis="{a[0]:.6f} {a[1]:.6f} 0" range="{-np.pi:.4f} {np.pi:.4f}" '
                f'damping="{DAMPING}" armature="0.001"/>'
            )

        for j, tri in enumerate(_triangles(faces[i])):
            if coll_thick is None:
                mname = f"m{i}_{j}"
                mesh_lines.append(f'        <mesh name="{mname}" vertex="{_prism(tri, origin[i])}"/>')
                body_lines.append(
                    f'{ind}    <geom type="mesh" mesh="{mname}" '
                    f'material="{mats[pat.depth[i] % 2]}" density="{density:.3f}" '
                    f'contype="1" conaffinity="1" condim="3" '
                    f'friction="{MU_PAPER} 0.005 0.0001"/>'
                )
            else:
                vname = f"mv{i}_{j}"
                mesh_lines.append(f'        <mesh name="{vname}" vertex="{_prism(tri, origin[i])}"/>')
                body_lines.append(
                    f'{ind}    <geom type="mesh" mesh="{vname}" '
                    f'material="{mats[pat.depth[i] % 2]}" density="{density:.3f}" '
                    f'contype="0" conaffinity="0" condim="3"/>'
                )
                cname = f"mc{i}_{j}"
                mesh_lines.append(f'        <mesh name="{cname}" vertex="{_prism(tri, origin[i], coll_thick)}"/>')
                body_lines.append(
                    f'{ind}    <geom type="mesh" mesh="{cname}" rgba="0 0 0 0" '
                    f'density="0" contype="1" conaffinity="1" condim="3" '
                    f'friction="{MU_PAPER} 0.005 0.0001"/>'
                )

        for c in children[i]:
            emit(c, depth + 1)
        body_lines.append(f'{ind}</body>')

    emit(pat.root, 0)

    eq_lines = []
    for k in pat.loop_edges:
        e = edges[k]
        oi = origin[e["i"]]
        for pt in (e["p"], e["q"]):
            eq_lines.append(
                f'        <connect body1="face_{e["i"]}" body2="face_{e["j"]}" '
                f'anchor="{pt[0] - oi[0]:.6f} {pt[1] - oi[1]:.6f} 0" solref="{EQ_SOLREF}" solimp="{EQ_SOLIMP}"/>'
            )

    act_lines = [
        f'        <position name="fold_{h}" joint="{hi["name"]}" kp="{KP}" kv="{KV}" '
        f'ctrlrange="{-np.pi:.4f} {np.pi:.4f}" forcerange="-{FORCE_MAX} {FORCE_MAX}"/>'
        for h, hi in enumerate(hinges)
    ]

    xml = f'''<mujoco model="{name}">
    <compiler angle="radian"/>
    <option timestep="0.001" gravity="0 0 -9.81" integrator="implicitfast"/>
    <visual><global offwidth="1280" offheight="720"/></visual>
    <default><geom solref="0.004 1" solimp="0.9 0.95 0.001"/></default>

    <asset>
        <material name="paper_A" rgba="0.85 0.90 1.0 1" specular="0.1"/>
        <material name="paper_B" rgba="1.0 0.85 0.85 1" specular="0.1"/>
        <texture name="checker" type="2d" builtin="checker" width="512" height="512"
                 rgb1="0.1 0.1 0.1" rgb2="0.8 0.8 0.8"/>
        <material name="floor" texture="checker" texrepeat="8 8" reflectance="0.1" specular="0.2"/>
 {chr(10).join(mesh_lines)}
    </asset>

    <worldbody>
        <body name="table" pos="0 0 -0.05">
            <joint name="table_x" type="slide" axis="1 0 0" damping="0"/>
            <joint name="table_z" type="slide" axis="0 0 1" damping="0"/>
            <geom name="ground" type="box" size="5 5 0.05" material="floor"
                  contype="1" conaffinity="1" condim="3"
                  friction="{MU_TABLE} 0.005 0.0001" mass="1000"/>
        </body>
 {chr(10).join(body_lines)}
    </worldbody>

    <equality>
 {chr(10).join(eq_lines)}
    </equality>

    <actuator>
 {chr(10).join(act_lines)}
    </actuator>
</mujoco>'''

    info = dict(
        hinges=hinges,
        targets=np.array([h["target"] for h in hinges]),
        n_faces=n,
        n_hinges=len(hinges),
        n_loops=len(pat.loop_edges),
    )
    return xml, info


__all__ = ["generate_xml"]
