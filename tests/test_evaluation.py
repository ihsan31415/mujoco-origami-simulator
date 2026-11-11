import math

import numpy as np
import pytest

from evaluation import evaluate_individual, evaluate_population
from origami_engine.patterns import reference_miura_legacy_creases
from origami_simulation import build_pattern, load_creases_from_json, save_creases_to_json


def make_reference_creases():
    return reference_miura_legacy_creases()


def test_input_compatibility_and_pattern_validity():
    creases = make_reference_creases()
    pat = build_pattern(creases)
    assert pat.valid is True
    assert pat.n_faces if hasattr(pat, "n_faces") else len(pat.faces) > 0


def test_basic_execution_returns_finite_displacement():
    creases = make_reference_creases()
    value = evaluate_individual(creases, duration=0.5, trajectory=(1.0, 0.0, 0.0))
    assert isinstance(value, float)
    assert math.isfinite(value)


def test_duration_handling_is_consistent():
    creases = make_reference_creases()
    short = evaluate_individual(creases, duration=0.25, trajectory=(1.0, 0.0, 0.0))
    long = evaluate_individual(creases, duration=0.75, trajectory=(1.0, 0.0, 0.0))
    assert math.isfinite(short)
    assert math.isfinite(long)


def test_repeatability():
    creases = make_reference_creases()
    a = evaluate_individual(creases, duration=0.5, trajectory=(1.0, 0.0, 0.0))
    b = evaluate_individual(creases, duration=0.5, trajectory=(1.0, 0.0, 0.0))
    assert a == pytest.approx(b)


def test_state_isolation_between_evaluations():
    creases = make_reference_creases()
    first = evaluate_individual(creases, duration=0.5, trajectory=(1.0, 0.0, 0.0))
    second = evaluate_individual(creases, duration=0.5, trajectory=(1.0, 0.0, 0.0))
    assert first == pytest.approx(second)


def test_invalid_duration_and_direction_raise():
    creases = make_reference_creases()
    with pytest.raises(ValueError):
        evaluate_individual(creases, duration=0.0, trajectory=(1.0, 0.0, 0.0))
    with pytest.raises(ValueError):
        evaluate_individual(creases, duration=0.5, trajectory=(0.0, 0.0, 0.0))


def test_population_evaluation_keeps_order_and_supports_sequential_fallback():
    creases = make_reference_creases()
    population = [creases, creases]
    result = evaluate_population(population, duration=0.5, trajectory=(1.0, 0.0, 0.0), workers=1)
    assert len(result) == 2
    assert all(math.isfinite(x) for x in result)
    assert result[0] == pytest.approx(result[1])


def test_invalid_crease_shape_is_rejected():
    with pytest.raises(ValueError):
        evaluate_individual([{'not': 'a crease'}], duration=0.5, trajectory=(1.0, 0.0, 0.0))


def test_json_loader_round_trip(tmp_path):
    creases = make_reference_creases()
    out = tmp_path / "creases.json"
    save_creases_to_json(creases, out, angle_unit="degree")
    loaded = load_creases_from_json(out)
    assert len(loaded) == len(creases)
    assert loaded[0].p1 == pytest.approx(creases[0].p1)
    assert loaded[0].p2 == pytest.approx(creases[0].p2)
    assert loaded[0].angle == pytest.approx(creases[0].angle)


def test_evaluate_individual_accepts_json_path(tmp_path):
    creases = make_reference_creases()
    out = tmp_path / "creases.json"
    save_creases_to_json(creases, out)
    value = evaluate_individual(out, duration=0.25, trajectory=(1.0, 0.0, 0.0))
    assert isinstance(value, float)
    assert math.isfinite(value)
