from __future__ import annotations

"""Core origami simulation domain and MuJoCo execution pipeline.

This module contains the authoritative simulation mechanics extracted from the
notebook implementation. It intentionally keeps geometry reconstruction,
MuJoCo model generation, and stepping logic together to preserve behavior while
providing a single reusable interface for evaluation and rendering.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from shapely.geometry import LineString, Point, box
from shapely.ops import linemerge, nearest_points, polygonize, unary_union

try:
    import mujoco
except Exception as exc:  # pragma: no cover - import-time guard for clarity
    mujoco = None
    _MUJOCO_IMPORT_ERROR = exc
else:
    _MUJOCO_IMPORT_ERROR = None

# ---------------------------------------------------------------------------
# Notebook constants recovered from the fold simulation.
# ---------------------------------------------------------------------------
S = 1.0
THICK = 0.0001
PAPER_MASS = 0.2
Z0 = THICK + 0.001

N_MAX = 8
GENES = 6
GENOME_LEN = N_MAX * GENES
GENE_LOW = np.tile([0, 0, 0, 0, -np.pi, 0], N_MAX)
GENE_HIGH = np.tile([S, S, S, S, np.pi, 1], N_MAX)

EXTEND_MODE = "chord"
SNAP_TOL = 0.02
GRID = 1e-4
MIN_FACE_AREA = 1e-4 * S * S
MAX_FOLD = np.pi * 0.98

KP, KV, DAMPING, FORCE_MAX = 2.0, 0.15, 0.003, 2.0
MU_PAPER = 0.3
MU_TABLE = 0.5
VIB_FREQ = 75.0
VIB_AMP_X = 0.0
VIB_AMP_Z = 0.0013
EQ_SOLREF = "0.005 1"
EQ_SOLIMP = "0.95 0.99 0.001"
STRETCH_K = 5.0e4
STRETCH_DAMP = 50.0
STRETCH_MAX = 1.0e-4
K_PANEL = 1e5
D_PANEL = 50.0
MAX_STRAIN = 0.005
COLL_THICK = THICK * 0.1

V = np.deg2rad(-45)
M = np.deg2rad(45)


@dataclass(frozen=True)
class Crease:
    p1: tuple[float, float]
    p2: tuple[float, float]
    angle: float


@dataclass
class Pattern:
    valid: bool
    reason: str = ""
    faces: list | None = None
    edges: list | None = None
    root: int = 0
    parent: dict | None = None
    depth: dict | None = None
    tree_edge: dict | None = None
    loop_edges: list | None = None


@dataclass
class SimulationResult:
    model: Any
    data: Any
    pattern: Pattern
    info: dict[str, Any]
    initial_centroid: np.ndarray
    final_centroid: np.ndarray


def clip_to_square(p, d, t0, t1):
    """Clip p + t*d (t in [t0, t1]) to the square [0, S]^2."""
    for k in range(2):
        if abs(d[k]) < 1e-12:
            if p[k] < 0 or p[k] > S:
                return None
        else:
            ta, tb = (0 - p[k]) / d[k], (S - p[k]) / d[k]
            if ta > tb:
                ta, tb = tb, ta
            t0, t1 = max(t0, ta), min(t1, tb)
            if t0 > t1:
                return None
    return p + t0 * d, p + t1 * d


def snap_endpoints(segs, tol):
    boundary = box(0, 0, S, S).exterior
    out = []
    for i, (a, b, ang) in enumerate(segs):
        others = [LineString([s[0], s[1]]) for j, s in enumerate(segs) if j != i]
        targets = unary_union([boundary] + others)
        new = []
        for p in (a, b):
            pt = Point(p)
            if targets.distance(pt) < tol:
                q = nearest_points(targets, pt)[0]
                new.append((q.x, q.y))
            else:
                new.append(tuple(p))
        out.append((new[0], new[1], ang))
    return out


def decode_genome(genome, mode=None):
    mode = mode or EXTEND_MODE
    g = np.asarray(genome, float).reshape(N_MAX, GENES)
    segs = []
    for x1, y1, x2, y2, ang, act in g:
        if act <= 0.5:
            continue
        p = np.array([x1, y1])
        d = np.array([x2 - x1, y2 - y1])
        if np.linalg.norm(d) < 1e-3:
            continue
        res = clip_to_square(p, d, -1e3, 1e3) if mode == "chord" else clip_to_square(p, d, 0.0, 1.0)
        if res is None:
            continue
        a, b = (np.round(r / GRID) * GRID for r in res)
        if np.linalg.norm(b - a) < 1e-3:
            continue
        segs.append((tuple(a), tuple(b), float(ang)))

    if mode == "segment" and SNAP_TOL > 0:
        segs = snap_endpoints(segs, SNAP_TOL)

    return [
        Crease(a, b, ang)
        for a, b, ang in segs
        if np.hypot(b[0] - a[0], b[1] - a[1]) > 1e-3
    ]


def _parts(g):
    return list(g.geoms) if hasattr(g, "geoms") else [g]


def _straight_pieces(g):
    lines = [x for x in _parts(g) if x.geom_type == "LineString"]
    if not lines:
        return []
    out = []
    for part in _parts(linemerge(lines)):
        c = list(part.simplify(1e-9).coords)
        out += [
            (c[i], c[i + 1])
            for i in range(len(c) - 1)
            if np.hypot(c[i + 1][0] - c[i][0], c[i + 1][1] - c[i][1]) > 1e-6
        ]
    return out


def build_pattern(creases):
    lines = [LineString([c.p1, c.p2]) for c in creases]
    noded = unary_union([box(0, 0, S, S).exterior] + lines)
    faces = list(polygonize(_parts(noded)))
    if not faces:
        return Pattern(False, "no faces")

    areas = np.array([f.area for f in faces])
    if areas.min() < MIN_FACE_AREA:
        return Pattern(False, f"sliver face (area {areas.min():.2e})")
    if abs(areas.sum() - S * S) > 1e-6:
        return Pattern(False, "faces do not tile the sheet")

    bnd = [f.boundary for f in faces]
    edges = []
    for i in range(len(faces)):
        for j in range(i + 1, len(faces)):
            if not faces[i].intersects(faces[j]):
                continue
            for p, q in _straight_pieces(bnd[i].intersection(bnd[j])):
                mid = Point((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
                dist = [ln.distance(mid) for ln in lines]
                k = int(np.argmin(dist)) if dist else -1
                if k >= 0 and dist[k] > 1e-6:
                    k = -1
                edges.append({"i": i, "j": j, "p": p, "q": q, "crease": k})

    adj = {i: [] for i in range(len(faces))}
    for k, e in enumerate(edges):
        adj[e["i"]].append((e["j"], k))
        adj[e["j"]].append((e["i"], k))

    root = int(np.argmax(areas))
    parent, depth, tree_edge = {root: None}, {root: 0}, {}
    queue = [root]
    while queue:
        u = queue.pop(0)
        for v, k in adj[u]:
            if v not in parent:
                parent[v], depth[v], tree_edge[v] = u, depth[u] + 1, k
                queue.append(v)

    if len(parent) < len(faces):
        return Pattern(False, "disconnected faces")

    used = set(tree_edge.values())
    loop_edges = [k for k in range(len(edges)) if k not in used]
    pat = Pattern(True, "", faces, edges, root, parent, depth, tree_edge, loop_edges)
    pat.n_faces = len(faces)
    pat.n_loops = len(loop_edges)
    return pat


def _tri_area(t):
    return 0.5 * abs((t[1][0] - t[0][0]) * (t[2][1] - t[0][1]) - (t[2][0] - t[0][0]) * (t[1][1] - t[0][1]))


def _triangles(poly):
    if poly.convex_hull.area - poly.area < 1e-12 and not list(poly.interiors):
        c = np.array(poly.exterior.coords)[:-1]
        tris = [(c[0], c[k], c[k + 1]) for k in range(1, len(c) - 1)]
    else:
        try:
            import shapely

            tris = [np.array(t.exterior.coords)[:3] for t in shapely.constrained_delaunay_triangles(poly).geoms]
        except Exception:
            from shapely.ops import triangulate

            tris = [np.array(t.exterior.coords)[:3] for t in triangulate(poly) if poly.contains(t.representative_point())]
    return [np.asarray(t) for t in tris if _tri_area(t) > 1e-7]


def _prism(tri, O, thick=None):
    """Triangular prism vertex list."""
    t = THICK if thick is None else thick
    v = []
    for x, y in np.asarray(tri)[:, :2]:
        v += [x - O[0], y - O[1], -t, x - O[0], y - O[1], t]
    return " ".join(f"{a:.6f}" for a in v)


def generate_xml(pat, creases, name="origami_free", coll_thick=None):
    """
    coll_thick : None -> original single-geom behavior (baseline)
                 value -> thin-collision mode: separate visual + collision geoms
    """
    if mujoco is None:
        raise RuntimeError("MuJoCo is required to build the simulation model.") from _MUJOCO_IMPORT_ERROR

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


def drive_table(model, data, t, amp_x=VIB_AMP_X, amp_z=VIB_AMP_Z, freq_hz=VIB_FREQ):
    w = 2 * np.pi * freq_hz
    jx, jz = model.joint("table_x"), model.joint("table_z")
    data.qpos[jx.qposadr[0]] = amp_x * np.sin(w * t)
    data.qvel[jx.dofadr[0]] = amp_x * w * np.cos(w * t)
    data.qpos[jz.qposadr[0]] = amp_z * np.sin(w * t)
    data.qvel[jz.dofadr[0]] = amp_z * w * np.cos(w * t)


def _paper_centroid(model, data):
    table_id = model.body("table").id
    ids = [g for g in range(model.ngeom) if model.geom_bodyid[g] != table_id]
    if not ids:
        raise ValueError("No paper geoms were found in the MuJoCo model.")
    points = np.asarray(data.geom_xpos[ids, :3], dtype=float)
    if points.size == 0:
        raise ValueError("Simulation geometry is empty.")
    return points[:, :2].mean(axis=0)


def run_simulation(creases, duration=8.0, fold_duration=3.0, vibrate=True, amp_x=VIB_AMP_X, amp_z=VIB_AMP_Z, freq_hz=VIB_FREQ):
    """Run the fold simulation and return final MuJoCo state plus centroid data."""
    if mujoco is None:
        raise RuntimeError("MuJoCo is required to run the simulation.") from _MUJOCO_IMPORT_ERROR
    if duration <= 0:
        raise ValueError("duration must be positive.")

    normalized = normalize_creases(creases)
    pat = build_pattern(normalized)
    if not pat.valid:
        raise ValueError(f"invalid crease pattern: {pat.reason}")

    xml, info = generate_xml(pat, normalized)
    model = mujoco.MjModel.from_xml_string(xml)
    data = mujoco.MjData(model)

    initial_centroid = _paper_centroid(model, data)
    target_angles = np.asarray(info["targets"], dtype=float)
    hinge_adr = np.array([model.joint(h["name"]).qposadr[0] for h in info["hinges"]], dtype=int)
    if len(hinge_adr):
        data.qpos[hinge_adr] = 0.0

    while data.time < duration:
        t = min(data.time / fold_duration, 1.0)
        s = t * t * (3 - 2 * t)
        data.ctrl[:] = s * target_angles
        if vibrate:
            drive_table(model, data, data.time, amp_x=amp_x, amp_z=amp_z, freq_hz=freq_hz)
        mujoco.mj_step(model, data)

    if not np.isfinite(data.qpos).all():
        raise FloatingPointError("unstable simulation: non-finite joint coordinates produced.")

    final_centroid = _paper_centroid(model, data)
    return SimulationResult(
        model=model,
        data=data,
        pattern=pat,
        info=info,
        initial_centroid=initial_centroid,
        final_centroid=final_centroid,
    )


def load_creases_from_json(path):
    """Load crease pattern from JSON object or list schema."""
    path_obj = Path(path)
    payload = json.loads(path_obj.read_text())

    if isinstance(payload, list):
        crease_items = payload
        angle_unit = "radian"
    elif isinstance(payload, dict):
        if "creases" not in payload:
            raise ValueError("JSON crease file must contain a 'creases' key.")
        crease_items = payload["creases"]
        angle_unit = str(payload.get("angle_unit", "radian")).strip().lower()
    else:
        raise ValueError("JSON crease file must be an object or list.")

    if angle_unit not in {"radian", "radians", "rad", "degree", "degrees", "deg"}:
        raise ValueError("angle_unit must be one of: radian, degree.")

    use_degrees = angle_unit in {"degree", "degrees", "deg"}
    creases = []
    for idx, item in enumerate(crease_items):
        if not isinstance(item, dict):
            raise ValueError(f"crease entry at index {idx} must be an object.")
        try:
            p1 = tuple(float(v) for v in item["p1"])
            p2 = tuple(float(v) for v in item["p2"])
            angle = float(item["angle"])
        except KeyError as exc:
            raise ValueError(f"crease entry at index {idx} missing key: {exc}") from exc

        if len(p1) != 2 or len(p2) != 2:
            raise ValueError(f"crease entry at index {idx} must have 2D p1/p2 coordinates.")

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
    if creases is None:
        raise ValueError("creases must not be None.")
    if isinstance(creases, (str, Path)):
        return load_creases_from_json(creases)
    if not isinstance(creases, (list, tuple)):
        raise ValueError("creases must be a list or tuple of Crease objects.")
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


__all__ = [
    "COLL_THICK",
    "Crease",
    "D_PANEL",
    "DAMPING",
    "EQ_SOLIMP",
    "EQ_SOLREF",
    "EXTEND_MODE",
    "FORCE_MAX",
    "GENE_HIGH",
    "GENE_LOW",
    "GENES",
    "GENOME_LEN",
    "GRID",
    "K_PANEL",
    "KP",
    "KV",
    "M",
    "MAX_FOLD",
    "MAX_STRAIN",
    "MIN_FACE_AREA",
    "MU_PAPER",
    "MU_TABLE",
    "N_MAX",
    "PAPER_MASS",
    "Pattern",
    "S",
    "SNAP_TOL",
    "STRETCH_DAMP",
    "STRETCH_K",
    "STRETCH_MAX",
    "SimulationResult",
    "THICK",
    "V",
    "VIB_AMP_X",
    "VIB_AMP_Z",
    "VIB_FREQ",
    "Z0",
    "build_pattern",
    "decode_genome",
    "drive_table",
    "generate_xml",
    "load_creases_from_json",
    "normalize_creases",
    "run_simulation",
    "save_creases_to_json",
]
