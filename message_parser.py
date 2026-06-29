"""Parse Slack message and slash command payloads."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable, List, Optional

from bot_state import BotState


@dataclass
class ParsedMessage:
    actor_id: str
    channel_id: str
    text: str
    target_users: List[str]
    command: Optional[Callable[..., str]] = None
    fip_change: Optional[str] = None
    ignored: bool = False


class MessageParser:
    MENTION = re.compile(r"<@([A-Z0-9]+)>")

    @classmethod
    def parse_event(cls, data: dict, state: BotState) -> ParsedMessage:
        actor_id = data.get("user", "")
        channel_id = data.get("channel", "")
        text = data.get("text") or " "
        parsed = ParsedMessage(
            actor_id=actor_id,
            channel_id=channel_id,
            text=text,
            target_users=cls.parse_targets(text, state.botid),
        )
        if cls._should_ignore(data, state, actor_id):
            parsed.ignored = True
            return parsed
        cls._resolve_command(parsed, state)
        return parsed

    @classmethod
    def parse_slash(cls, payload: dict, state: BotState) -> ParsedMessage:
        command_name = payload.get("command", "")
        text = (payload.get("text") or "").strip()
        actor_id = payload.get("user_id", "")
        channel_id = payload.get("channel_id", "")
        synthetic = cls._slash_to_text(command_name, text)
        parsed = ParsedMessage(
            actor_id=actor_id,
            channel_id=channel_id,
            text=synthetic,
            target_users=cls.parse_targets(synthetic, state.botid),
        )
        cls._resolve_command(parsed, state)
        return parsed

    @classmethod
    def parse_targets(cls, text: str, botid: str) -> List[str]:
        targets: List[str] = []
        for match in cls.MENTION.finditer(text):
            user_id = match.group(1)
            if user_id == botid or user_id in targets:
                continue
            targets.append(user_id)
        return targets

    @classmethod
    def _slash_to_text(cls, command_name: str, text: str) -> str:
        mapping = {
            "/help": "help",
            "/roll": "roll {0}".format(text or "d20").strip(),
            "/ban": "ban {0}".format(text).strip(),
            "/unban": "unban {0}".format(text).strip(),
            "/unbanall": "unbanall",
            "/mypoints": "mypoints",
            "/scoreboard": "scoreboard",
            "/wtf": "wtf_is {0}".format(text).strip(),
        }
        return mapping.get(command_name, text)

    @classmethod
    def _should_ignore(cls, data: dict, state: BotState, actor_id: str) -> bool:
        if data.get("bot_id") and data.get("bot_id") == state.botid:
            return True
        if actor_id and actor_id == state.botuserid:
            return True
        if actor_id and actor_id == state.botid:
            return True
        ignore_types = ["message_changed", "bot_message", "message_deleted"]
        return data.get("subtype") in ignore_types

    @classmethod
    def _resolve_command(cls, parsed: ParsedMessage, state: BotState) -> None:
        for token in parsed.text.split():
            if token in state.commands:
                parsed.command = state.commands[token]
                return
            if token.startswith("+") or token.startswith("-"):
                parsed.fip_change = token
                parsed.command = None
                return
