"""Test for help message generation."""

from access import AccessControl
from context import CommandContext
from commands import help as help_command


def mycmd():
    """Return true."""
    return True


def test_alias():
    commands = help_command.alias()
    assert "help" in commands


def test_printout():
    ctx = CommandContext(
        actor_id="bob",
        channel_id="C1",
        text="help",
        target_users=[],
        access=AccessControl([], {}),
        score={},
        workdir="/tmp",
        commands={"mycmd": mycmd},
        reply_channel="C1",
    )
    result = help_command.generate_help(context=ctx)
    assert "mycmd" in result
    assert "Return true." in result
    assert "Slash commands" in result
    assert ctx.reply_channel == "bob"

