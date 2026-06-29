"""Test JSON storage helpers."""

import json
import pickle

from storage import load_data, load_state, save_data, save_state


def test_save_and_load_json(tmp_path):
    save_data(str(tmp_path), "score", {"U123": 5})
    loaded = load_data(str(tmp_path), "score")
    assert loaded == {"U123": 5}


def test_migrate_pickle_to_json(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    with open(data_dir / "score", "wb") as handle:
        pickle.dump({"U999": 3}, handle)

    loaded = load_data(str(tmp_path), "score")
    assert loaded == {"U999": 3}
    assert (data_dir / "score.json").is_file()


def test_load_state(tmp_path):
    save_state(str(tmp_path), {"a": 1}, {"b": True})
    score, banned = load_state(str(tmp_path))
    assert score == {"a": 1}
    assert banned == {"b": True}
