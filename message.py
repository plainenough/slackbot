"""Simple message facade for Slack events."""

from __future__ import annotations

from bot_state import BotState
from context import CommandContext
from dispatcher import CommandDispatcher
from message_parser import MessageParser


class Message:
    """Parse a Slack event and dispatch the first matching command."""

    def __init__(self, data, **kwargs):
        self._kwargs = kwargs
        self._data = data
        state = BotState.from_kwargs(kwargs)
        parsed = MessageParser.parse_event(data, state)
        response = CommandDispatcher(state).dispatch(parsed)
        self.user = parsed.actor_id
        self.channel = response.channel
        self.msg = response.text
        self.banned = state.access.is_banned(parsed.actor_id) and bool(response.text)
        self.target_users = parsed.target_users
        self._text = parsed.text
        self.command = parsed.command or parsed.fip_change
        self.ephemeral = response.ephemeral
        self.context = CommandContext(
            actor_id=parsed.actor_id,
            channel_id=parsed.channel_id,
            text=parsed.text,
            target_users=parsed.target_users,
            access=state.access,
            score=state.score,
            workdir=state.workdir,
            commands=state.commands,
            reply_channel=response.channel,
            fip_change=parsed.fip_change,
            ephemeral=response.ephemeral,
        )
        self.access = state.access

    @property
    def admin(self) -> bool:
        return self.access.is_admin(self.user)

    def __str__(self) -> str:
        return (
            "\nUSER:{0}\nTARGETS:{1}\nCOMMAND:{2}\nORIGINAL_TEXT:{3}\n"
            "MSG:{4}\nADMIN:{5}\nBANNED:{6}"
        ).format(
            self.user,
            self.target_users,
            self.command,
            self._text,
            self.msg,
            self.admin,
            self.banned,
        )
