"""Ban command utilities."""

from audit import record
from context import get_context


def alias():
    """Define separate commands and map them to functions."""
    return {
        "ban": ban_user,
        "unban": unban_user,
        "unbanall": unban_all,
    }


def ban_user(**kwargs):
    """Ban a user from using commands."""
    ctx = get_context(kwargs)
    user = kwargs.get("user")
    denied = ctx.access.require_admin(ctx)
    if denied:
        return denied
    if user == "none":
        return ""
    ctx.access.ban_user(user)
    record(ctx.workdir, ctx.actor_id, "ban", target=user)
    return "User <@{0}> is banned.\n".format(user)


def unban_all(**kwargs):
    """Unban all users."""
    ctx = get_context(kwargs)
    denied = ctx.access.require_admin(ctx)
    if denied:
        return denied
    ctx.access.unban_all()
    record(ctx.workdir, ctx.actor_id, "unbanall")
    return "Cleared the ban list"


def unban_user(**kwargs):
    """Unban an existing user ban."""
    ctx = get_context(kwargs)
    user = kwargs.get("user")
    denied = ctx.access.require_admin(ctx)
    if denied:
        return denied
    ctx.access.unban_user(user)
    record(ctx.workdir, ctx.actor_id, "unban", target=user)
    return "User <@{0}> is unbanned.\n".format(user)
