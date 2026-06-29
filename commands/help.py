"""Generate help message from docstrings."""

from context import get_context


def alias():
    """Load custom commands and the functions they map too."""
    return {"help": generate_help}


def generate_help(**kwargs):
    """Pull the doc string out of all of the commands."""
    ctx = get_context(kwargs)
    if len(ctx.text) > 25 and not ctx.text.startswith("/"):
        return ""
    ctx.dm_actor()
    lines = []
    for name, func in sorted(ctx.commands.items()):
        doc = (func.__doc__ or "").strip()
        lines.append("{0:<30}: {1}".format(name, doc))
    slash_lines = [
        "Slash commands:",
        "/help, /roll, /ban, /unban, /unbanall, /mypoints, /scoreboard, /wtf",
    ]
    return "```" + "\n".join(lines + [""] + slash_lines) + "```"
