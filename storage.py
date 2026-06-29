"""Persist score and ban data as JSON."""

import json
import logging
import os
import pickle
import threading

logger = logging.getLogger(__name__)


def _json_path(workdir, name):
    return os.path.join(workdir, "data", f"{name}.json")


def _pickle_path(workdir, name):
    return os.path.join(workdir, "data", name)


def _load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_pickle(path):
    with open(path, "rb") as handle:
        return pickle.load(handle)


def load_data(workdir, name):
    json_path = _json_path(workdir, name)
    pickle_path = _pickle_path(workdir, name)

    if os.path.isfile(json_path):
        try:
            data = _load_json(json_path)
            return data if isinstance(data, dict) else {}
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Failed to load %s: %s", json_path, exc)

    if os.path.isfile(pickle_path):
        try:
            data = _load_pickle(pickle_path)
            if isinstance(data, dict):
                save_data(workdir, name, data)
                logger.info("Migrated %s from pickle to JSON", name)
                return data
        except (pickle.UnpicklingError, OSError) as exc:
            logger.warning("Failed to migrate %s: %s", pickle_path, exc)

    return {}


def save_data(workdir, name, data):
    os.makedirs(os.path.join(workdir, "data"), exist_ok=True)
    path = _json_path(workdir, name)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)


def load_state(workdir):
    return load_data(workdir, "score"), load_data(workdir, "banned")


def save_state(workdir, score, banned):
    save_data(workdir, "score", score)
    save_data(workdir, "banned", banned)


def start_save_worker(workdir, score, banned, stop_event, interval=30):
    def worker():
        while not stop_event.wait(interval):
            save_state(workdir, score, banned)

    thread = threading.Thread(target=worker, daemon=True, name="state-save")
    thread.start()
    return thread
