from pathlib import Path

import pytest

from origami_engine import Crease, build_pattern, load_default_creases


@pytest.fixture
def simple_creases():
    """A minimal valid crease set: two mountain folds forming a V."""
    return [
        Crease((0.2, 0.0), (0.5, 0.5), -0.7853981633974483),
        Crease((0.5, 0.5), (0.8, 0.0), -0.7853981633974483),
    ]


@pytest.fixture
def default_creases():
    """The default reference crease pattern (24 creases)."""
    return load_default_creases()


@pytest.fixture
def default_pattern(default_creases):
    """The validated default pattern (16 faces, 9 loop edges)."""
    pat = build_pattern(default_creases)
    assert pat.valid
    return pat


@pytest.fixture
def tmp_json(tmp_path: Path):
    """A temporary JSON crease file path."""
    return tmp_path / "test_creases.json"
