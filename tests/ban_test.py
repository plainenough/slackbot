"""Test ban functionality."""

import pytest

from access import AccessControl
from context import CommandContext
from commands import ban as ban_command

banned = {"fred": True}


class Message(object):
    """Test stub with shared AccessControl state."""

    def __init__(self, admins=None):
        self._text = "ban @<jan>"
        self.channel = "#general"
        self.user = "bob"
        admin_list = ["bob"] if admins is None else admins
        self._kwargs = dict(banned=banned)
        self.access = AccessControl(admin_list, banned)
        self.context = CommandContext(
            actor_id=self.user,
            channel_id=self.channel,
            text=self._text,
            target_users=[],
            access=self.access,
            score={},
            workdir="/tmp",
            commands={},
            reply_channel=self.channel,
        )
        self.admin = self.access.is_admin(self.user)


@pytest.fixture
def fixture_ban():
    message = Message()
    kwargs = dict(user="jan", channel=message.channel, message=message, context=message.context)
    result = ban_command.ban_user(**kwargs)
    return kwargs, result


@pytest.fixture
def fixture_unban():
    message = Message()
    kwargs = dict(user="fred", channel=message.channel, message=message, context=message.context)
    result = ban_command.unban_user(**kwargs)
    return kwargs, result


@pytest.fixture
def fixture_unbanall():
    message = Message()
    kwargs = dict(user="jan", channel=message.channel, message=message, context=message.context)
    result = ban_command.unban_all(**kwargs)
    return kwargs, result, banned


@pytest.fixture
def fixture_notadmin():
    message = Message(admins=[])
    message.context = CommandContext(
        actor_id=message.user,
        channel_id=message.channel,
        text=message._text,
        target_users=[],
        access=message.access,
        score={},
        workdir="/tmp",
        commands={},
        reply_channel=message.channel,
    )
    kwargs = dict(user="jan", channel=message.channel, message=message, context=message.context)
    return (
        ban_command.ban_user(**kwargs),
        ban_command.unban_user(**kwargs),
        ban_command.unban_all(**kwargs),
    )


def test_alias():
    commands = ban_command.alias()
    assert "ban" in commands
    assert "unban" in commands
    assert "unbanall" in commands


def test_unbanall(fixture_unbanall):
    kwargs, result, unbanned = fixture_unbanall
    assert unbanned == {}
    assert result == "Cleared the ban list"


def test_ban(fixture_ban):
    kwargs, result = fixture_ban
    assert kwargs["message"].access.is_banned("jan")
    assert result == "User <@jan> is banned.\n"


def test_unban(fixture_unban):
    kwargs, result = fixture_unban
    assert not kwargs["message"].access.is_banned("fred")
    assert result == "User <@fred> is unbanned.\n"


def test_notadmin(fixture_notadmin):
    ban_result, unban_result, unbanall_result = fixture_notadmin
    message = "<@bob>, you are not an admin"
    assert ban_result == message
    assert unban_result == message
    assert unbanall_result == message
