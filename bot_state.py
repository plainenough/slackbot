"""Shared runtime state for the bot."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional


@dataclass
class BotState:
    workdir: str
    commands: Dict[str, Callable[..., str]]
    access: Any
    score: dict
    banned: dict
    botid: str = ""
    botuserid: str = ""

    @classmethod
    def from_kwargs(cls, kwargs: dict) -> "BotState":
        access = kwargs.get("access")
        if access is None:
            from access import AccessControl

            access = AccessControl(kwargs.get("admins", []), kwargs.get("banned", {}))
        return cls(
            workdir=kwargs.get("myworkdir", ""),
            commands=kwargs.get("commands", {}),
            access=access,
            score=kwargs.get("score", {}),
            banned=kwargs.get("banned", {}),
            botid=kwargs.get("botid", ""),
            botuserid=kwargs.get("botuserid", ""),
        )

    def to_kwargs(self) -> dict:
        return {
            "myworkdir": self.workdir,
            "commands": self.commands,
            "access": self.access,
            "score": self.score,
            "banned": self.banned,
            "botid": self.botid,
            "botuserid": self.botuserid,
            "admins": list(self.access.admins),
        }
