"""Scoreboard helpers and snapshot tracking."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Tuple


MEDALS = ("🥇", "🥈", "🥉")


def _meta_path(workdir: str) -> str:
    return os.path.join(workdir, "data", "score_meta.json")


def load_snapshot(workdir: str) -> Dict[str, int]:
    path = _meta_path(workdir)
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
        snapshot = payload.get("snapshot", {})
        return snapshot if isinstance(snapshot, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def save_snapshot(workdir: str, score: dict) -> None:
    os.makedirs(os.path.join(workdir, "data"), exist_ok=True)
    payload = {
        "snapshot": dict(score),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(_meta_path(workdir), "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def format_leaderboard(score: dict, previous: Dict[str, int]) -> str:
    if not score:
        return "No one on your team has gained or lost any fake internet points"
    ranked: List[Tuple[str, int]] = sorted(score.items(), key=lambda item: item[1], reverse=True)
    lines = []
    for index, (user_id, value) in enumerate(ranked):
        prefix = MEDALS[index] if index < len(MEDALS) else "  "
        delta = value - previous.get(user_id, value)
        delta_text = ""
        if previous and delta != 0:
            sign = "+" if delta > 0 else ""
            delta_text = " ({0}{1} since last scoreboard)".format(sign, delta)
        lines.append(
            "{0} <@{1}> has a score of {2}{3}".format(prefix, user_id, value, delta_text)
        )
    return "\n".join(lines) + "\n"
