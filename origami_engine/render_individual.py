from __future__ import annotations

import json
import sys
from pathlib import Path

# Allow running this file directly (`python render_individual.py`) as well as
# via `python -m origami_engine.render_individual` from the project root.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import imageio
import numpy as np
import mujoco

from origami_engine.evaluation import evaluate_individual
from origami_engine.patterns import DEFAULT_PATTERN_JSON, reference_miura_render_creases
from origami_engine.simulation import VIB_AMP_X, VIB_AMP_Z, VIB_FREQ, build_pattern, drive_table, generate_xml, load_creases_from_json, normalize_creases


OUTPUT_VIDEO = PROJECT_ROOT / "individual_simulation.mp4"
OUTPUT_REPORT = PROJECT_ROOT / "render_report.json"



def paper_centroid(model, data):
    table_id = model.body("table").id
    ids = [g for g in range(model.ngeom) if model.geom_bodyid[g] != table_id]
    if not ids:
        raise ValueError("No paper geoms available for centroid tracking.")
    points = np.asarray(data.geom_xpos[ids, :3], dtype=float)
    return points[:, :2].mean(axis=0)


def trace_simulation(creases, duration=2.0, fold_duration=3.0, fps=24, trajectory=(1.0, 0.0, 0.0), vibrate=True, amp_x=VIB_AMP_X, amp_z=VIB_AMP_Z, freq_hz=VIB_FREQ):
    creases = normalize_creases(creases)
    pat = build_pattern(creases)
    if not pat.valid:
        raise ValueError(f"invalid crease pattern: {pat.reason}")

    xml, info = generate_xml(pat, creases)
    model = mujoco.MjModel.from_xml_string(xml)
    data = mujoco.MjData(model)

    initial_centroid = paper_centroid(model, data)
    target_angles = np.asarray(info["targets"], dtype=float)
    hinge_adr = np.array([model.joint(h["name"]).qposadr[0] for h in info["hinges"]], dtype=int)
    if len(hinge_adr):
        data.qpos[hinge_adr] = 0.0

    renderer = mujoco.Renderer(model, width=720, height=720)
    cam = mujoco.MjvCamera()
    cam.lookat[:] = [0.5, 0.5, 0.05]
    cam.distance, cam.azimuth, cam.elevation = 2.5, 90, -30

    frames = []
    frame_dt = 1.0 / float(fps)
    next_frame_time = 0.0

    renderer.update_scene(data, camera=cam)
    frames.append(renderer.render())
    next_frame_time += frame_dt

    while data.time < duration:
        t = min(data.time / fold_duration, 1.0)
        s = t * t * (3 - 2 * t)
        data.ctrl[:] = s * target_angles
        if vibrate:
            drive_table(model, data, data.time, amp_x=amp_x, amp_z=amp_z, freq_hz=freq_hz)
        mujoco.mj_step(model, data)

        while data.time >= next_frame_time and next_frame_time <= duration + 1e-9:
            renderer.update_scene(data, camera=cam)
            frames.append(renderer.render())
            next_frame_time += frame_dt

    final_centroid = paper_centroid(model, data)
    direction = np.asarray(trajectory, dtype=float)
    direction = direction / np.linalg.norm(direction)
    displacement = float(np.dot(final_centroid - initial_centroid, direction[:2]))

    return {
        "initial_centroid": initial_centroid,
        "final_centroid": final_centroid,
        "forward_displacement": displacement,
        "frames": frames,
        "model": model,
        "data": data,
        "info": info,
        "pattern": pat,
    }


def export_video(frames, output_path: Path, fps: int = 24):
    if not frames:
        raise ValueError("No frames were captured during the simulation.")
    try:
        writer = imageio.get_writer(output_path, fps=fps, codec="libx264", format="FFMPEG", output_params=["-pix_fmt", "yuv420p"])
        for frame in frames:
            writer.append_data(frame)
        writer.close()
        return True
    except Exception:
        fallback = output_path.with_suffix(".gif")
        writer = imageio.get_writer(fallback, fps=fps)
        for frame in frames:
            writer.append_data(frame)
        writer.close()
        return False


def main():
    if DEFAULT_PATTERN_JSON.exists():
        creases = load_creases_from_json(DEFAULT_PATTERN_JSON)
        crease_source = str(DEFAULT_PATTERN_JSON)
    else:
        creases = reference_miura_render_creases()
        crease_source = "embedded_reference_render_pattern"

    trajectory = (1.0, 0.0, 0.0)
    duration = 20.0
    fold_duration = 0.000001

    trace = trace_simulation(creases, duration=duration, fold_duration=fold_duration, trajectory=trajectory, vibrate=True)
    displacement = evaluate_individual(creases, duration=duration, trajectory=trajectory, fold_duration=fold_duration, vibrate=True)

    is_mp4 = export_video(trace["frames"], OUTPUT_VIDEO, fps=24)
    report = {
        "crease_configuration": crease_source,
        "duration": duration,
        "fold_duration": fold_duration,
        "trajectory": list(np.asarray(trajectory, dtype=float)),
        "initial_centroid": trace["initial_centroid"].tolist(),
        "final_centroid": trace["final_centroid"].tolist(),
        "rendered_forward_displacement": trace["forward_displacement"],
        "evaluator_forward_displacement": float(displacement),
        "difference": float(trace["forward_displacement"] - displacement),
        "video_path": str(OUTPUT_VIDEO),
        "video_written": is_mp4,
    }
    OUTPUT_REPORT.write_text(json.dumps(report, indent=2))

    print(json.dumps(report, indent=2))
    print(f"video_exists={OUTPUT_VIDEO.exists()} path={OUTPUT_VIDEO}")


if __name__ == "__main__":
    main()
