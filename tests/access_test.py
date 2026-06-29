"""Tests for AccessControl."""

import pytest

from access import AccessControl
from context import CommandContext


@pytest.fixture
def access():
    return AccessControl(["ADMIN1"], {"BANNED1": True})


def _ctx(user, channel="C1", access_obj=None):
    access_obj = access_obj or AccessControl(["ADMIN1"], {"BANNED1": True})
    return CommandContext(
        actor_id=user,
        channel_id=channel,
        text="help",
        target_users=[],
        access=access_obj,
        score={},
        workdir="/tmp",
        commands={},
        reply_channel=channel,
    )


def test_is_admin(access):
    assert access.is_admin("ADMIN1") is True
    assert access.is_admin("USER1") is False


def test_is_banned(access):
    assert access.is_banned("BANNED1") is True
    assert access.is_banned("USER1") is False


def test_block_if_banned(access):
    ctx = _ctx("BANNED1", access_obj=access)
    blocked = access.block_if_banned(ctx)
    assert blocked is not None
    assert "banned" in blocked.lower()
    assert ctx.reply_channel == "BANNED1"


def test_block_if_not_banned(access):
    ctx = _ctx("USER1", access_obj=access)
    assert access.block_if_banned(ctx) is None


def test_require_admin(access):
    ctx = _ctx("ADMIN1", access_obj=access)
    assert access.require_admin(ctx) is None


def test_require_admin_denied(access):
    ctx = _ctx("USER1", channel="CPUBLIC", access_obj=access)
    denied = access.require_admin(ctx)
    assert denied == "<@USER1>, you are not an admin"
    assert ctx.reply_channel == "USER1"


def test_ban_mutations(access):
    access.ban_user("USER9")
    assert access.is_banned("USER9")
    access.unban_user("USER9")
    assert not access.is_banned("USER9")
    access.ban_user("A")
    access.ban_user("B")
    access.unban_all()
    assert access.banned == {}
