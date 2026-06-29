"""Append-only audit log for admin actions."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Optional


def _audit_path(workdir: str) -> str:
    return os.path.join(workdir, "data", "audit.jsonl")


def record(workdir: str, actor_id: str, action: str, target: Optional[str] = None, details: Optional[str] = None) -> None:
    os.makedirs(os.path.join(workdir, "data"), exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "actor": actor_id,
        "action": action,
        "target": target,
        "details": details,
    }
    with open(_audit_path(workdir), "a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")
