"""Test dice roll functionality."""

import pytest

from access import AccessControl
from context import CommandContext
from commands import dice


def _ctx(text):
    return CommandContext(
        actor_id="bob",
        channel_id="#general",
        text=text,
        target_users=[],
        access=AccessControl([], {}),
        score={},
        workdir="/tmp",
        commands=dice.alias(),
        reply_channel="#general",
    )


def test_alias():
    commands = dice.alias()
    assert "roll" in commands


def test_roll():
    result = dice.roll(context=_ctx("roll d10"))
    value = int(result.split("is")[1])
    assert 0 <= value <= 10


def test_bad_roll():
    assert dice.roll(context=_ctx("roll d20+1")) == ""


def test_d0_roll():
    assert dice.roll(context=_ctx("roll d0")) == ""


def test_d1_roll():
    result = dice.roll(context=_ctx("roll d1"))
    assert int(result.split("is")[1]) == 1
