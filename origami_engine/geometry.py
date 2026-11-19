from __future__ import annotations

"""Geometry reconstruction: turn crease segments into a validated face graph."""

import numpy as np
from shapely.geometry import LineString, Point, box
from shapely.ops import linemerge, polygonize, unary_union

from .constants import MIN_FACE_AREA, S
from .types import Pattern


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
            (c[i], c[i + 1]) for i in range(len(c) - 1) if np.hypot(c[i + 1][0] - c[i][0], c[i + 1][1] - c[i][1]) > 1e-6
        ]
    return out


def build_pattern(creases):
    """Reconstruct polygonal faces and the spanning-tree hinge graph.

    Returns a :class:`~origami_engine.types.Pattern` whose ``valid`` flag
    reports whether the creases tile the square sheet without sliver faces or
    disconnected panels.
    """
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
    return Pattern(
        True,
        "",
        faces,
        edges,
        root,
        parent,
        depth,
        tree_edge,
        loop_edges,
        n_faces=len(faces),
        n_loops=len(loop_edges),
    )


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

            tris = [
                np.array(t.exterior.coords)[:3] for t in triangulate(poly) if poly.contains(t.representative_point())
            ]
    return [np.asarray(t) for t in tris if _tri_area(t) > 1e-7]


__all__ = ["build_pattern"]
