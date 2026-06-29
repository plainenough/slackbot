"""Test tools around fake internet points."""

import pytest

from access import AccessControl
from context import CommandContext
from commands import fake_internet_points


def _ctx(user="bob", score=None, admins=None):
    score = score or {"fred": 1, "bob": 2}
    admin_list = ["bob"] if admins is None else admins
    return CommandContext(
        actor_id=user,
        channel_id="C1",
        text="scoreboard",
        target_users=[],
        access=AccessControl(admin_list, {}),
        score=score,
        workdir="/tmp",
        commands=fake_internet_points.alias(),
        reply_channel="C1",
    )


def test_alias():
    commands = fake_internet_points.alias()
    assert "mypoints" in commands
    assert "scoreboard" in commands
    assert "resetScores" in commands


def test_fipmypoints():
    ctx = _ctx()
    result = fake_internet_points.my_points(context=ctx)
    assert result == "<@bob> has 2 points"


def test_fipallpoints(tmp_path):
    ctx = _ctx()
    ctx.workdir = str(tmp_path)
    result = fake_internet_points.all_points(context=ctx)
    assert "🥇" in result
    assert "<@bob>" in result


def test_fipdelpoints():
    ctx = _ctx()
    result = fake_internet_points.del_points(user="fred", context=ctx)
    assert result == "<@fred> has been removed from the scoreboard"
    assert ctx.score == {"bob": 2}
