"""Tests for AccessControl."""

import pytest

from access import AccessControl


class StubMessage:
    def __init__(self, user, channel="C1"):
        self.user = user
        self.channel = channel
        self.msg = ""
        self.banned = False


@pytest.fixture
def access():
    return AccessControl(["ADMIN1"], {"BANNED1": True})


def test_is_admin(access):
    assert access.is_admin("ADMIN1") is True
    assert access.is_admin("USER1") is False


def test_is_banned(access):
    assert access.is_banned("BANNED1") is True
    assert access.is_banned("USER1") is False


def test_block_if_banned(access):
    message = StubMessage("BANNED1")
    assert access.block_if_banned(message) is True
    assert message.banned is True
    assert "banned" in message.msg.lower()
    assert message.channel == "BANNED1"


def test_block_if_not_banned(access):
    message = StubMessage("USER1")
    assert access.block_if_banned(message) is False
    assert message.msg == ""


def test_require_admin(access):
    message = StubMessage("ADMIN1")
    assert access.require_admin(message) is None


def test_require_admin_denied(access):
    message = StubMessage("USER1", channel="CPUBLIC")
    denied = access.require_admin(message)
    assert denied == "<@USER1>, you are not an admin"
    assert message.channel == "USER1"


def test_ban_mutations(access):
    access.ban_user("USER9")
    assert access.is_banned("USER9")
    access.unban_user("USER9")
    assert not access.is_banned("USER9")
    access.ban_user("A")
    access.ban_user("B")
    access.unban_all()
    assert access.banned == {}
