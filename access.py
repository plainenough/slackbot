"""Authorization helpers for admin and ban checks."""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from context import CommandContext


class AccessControl:
    """Centralized admin and ban policy for command execution."""

    def __init__(self, admins, banned):
        self.admins = set(admins or [])
        self.banned = banned if banned is not None else {}

    def is_admin(self, user_id: Optional[str]) -> bool:
        return user_id in self.admins

    def is_banned(self, user_id: Optional[str]) -> bool:
        return user_id in self.banned

    def ban_message(self) -> str:
        return "You are banned. Please contact an admin."

    def admin_denied_message(self, actor_id: str) -> str:
        return "<@{0}>, you are not an admin".format(actor_id)

    def block_if_banned(self, ctx: "CommandContext") -> Optional[str]:
        if not self.is_banned(ctx.actor_id):
            return None
        ctx.dm_actor()
        return self.ban_message()

    def require_admin(self, ctx: "CommandContext") -> Optional[str]:
        if self.is_admin(ctx.actor_id):
            return None
        ctx.dm_actor()
        return self.admin_denied_message(ctx.actor_id)

    def ban_user(self, user_id: Optional[str]) -> None:
        if user_id and user_id != "none":
            self.banned[user_id] = True

    def unban_user(self, user_id: Optional[str]) -> None:
        self.banned.pop(user_id, None)

    def unban_all(self) -> None:
        self.banned.clear()
