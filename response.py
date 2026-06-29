"""Bot response payload."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class BotResponse:
    text: str
    channel: str
    ephemeral: bool = False
    user: Optional[str] = None

    @property
    def empty(self) -> bool:
        return not self.text
