"""Command execution context passed to handlers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from access import AccessControl


@dataclass
class CommandContext:
    actor_id: str
    channel_id: str
    text: str
    target_users: List[str]
    access: "AccessControl"
    score: dict
    workdir: str
    commands: Dict[str, Callable[..., str]]
    reply_channel: str
    fip_change: Optional[str] = None
    ephemeral: bool = False

    @property
    def admin(self) -> bool:
        return self.access.is_admin(self.actor_id)

    def dm_actor(self, ephemeral: bool = True) -> None:
        self.reply_channel = self.actor_id
        self.ephemeral = ephemeral


def get_context(kwargs: dict) -> CommandContext:
    if "context" in kwargs:
        return kwargs["context"]
    message = kwargs.get("message")
    if message is not None and hasattr(message, "context"):
        return message.context
    raise ValueError("CommandContext not available in kwargs")
