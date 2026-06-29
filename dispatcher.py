"""Route parsed messages to command handlers."""

from __future__ import annotations

from audit import record
from bot_state import BotState
from context import CommandContext
from fake_points import FakeInternetPoints
from message_parser import ParsedMessage
from response import BotResponse


class CommandDispatcher:
    def __init__(self, state: BotState):
        self.state = state

    def dispatch(self, parsed: ParsedMessage) -> BotResponse:
        if parsed.ignored or (not parsed.command and not parsed.fip_change):
            return BotResponse("", parsed.channel_id)

        ctx = CommandContext(
            actor_id=parsed.actor_id,
            channel_id=parsed.channel_id,
            text=parsed.text,
            target_users=parsed.target_users,
            access=self.state.access,
            score=self.state.score,
            workdir=self.state.workdir,
            commands=self.state.commands,
            reply_channel=parsed.channel_id,
            fip_change=parsed.fip_change,
        )

        blocked = self.state.access.block_if_banned(ctx)
        if blocked:
            return BotResponse(
                blocked,
                ctx.channel_id,
                ephemeral=True,
                user=ctx.actor_id,
            )

        if parsed.fip_change:
            text = self._run_fake_points(ctx)
            return BotResponse(
                text,
                ctx.reply_channel,
                ephemeral=ctx.ephemeral,
                user=ctx.actor_id if ctx.ephemeral else None,
            )

        if len(parsed.target_users) > 1:
            assert parsed.command is not None
            text = self._run_multi(ctx, parsed.command)
        else:
            assert parsed.command is not None
            target = parsed.target_users[0] if len(parsed.target_users) == 1 else None
            text = parsed.command(user=target, context=ctx, message=_MessageShim(ctx))

        return BotResponse(
            text or "",
            ctx.reply_channel,
            ephemeral=ctx.ephemeral,
            user=ctx.actor_id if ctx.ephemeral else None,
        )

    def _run_multi(self, ctx: CommandContext, command) -> str:
        parts = []
        for target_user in ctx.target_users:
            parts.append(
                command(user=target_user, context=ctx, message=_MessageShim(ctx))
            )
        return "".join(parts)

    def _run_fake_points(self, ctx: CommandContext) -> str:
        if len(ctx.target_users) > 1:
            return ""
        target = ctx.target_users[0] if ctx.target_users else None
        fip = FakeInternetPoints(user=target, context=ctx, message=_MessageShim(ctx))
        if fip.change and target:
            record(ctx.workdir, ctx.actor_id, "fip_change", target=target, details=str(fip.change))
        return fip.msg


class _MessageShim:
    """Backward-compatible view for legacy command/tests interfaces."""

    def __init__(self, ctx: CommandContext):
        self.context = ctx
        self.user = ctx.actor_id
        self.channel = ctx.reply_channel
        self._text = ctx.text
        self.target_users = ctx.target_users
        self._fipchange = ctx.fip_change
        self._list_commands = ctx.commands
        self.access = ctx.access
        self._kwargs = {
            "score": ctx.score,
            "banned": ctx.access.banned,
            "myworkdir": ctx.workdir,
            "commands": ctx.commands,
            "access": ctx.access,
        }

    @property
    def admin(self) -> bool:
        return self.context.admin
