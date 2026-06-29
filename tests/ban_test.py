"""Test ban functionality."""


import pytest

from access import AccessControl

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
        self.admin = self.access.is_admin(self.user)


@pytest.fixture
def fixture_ban():
    """Fixture to test ban user."""
    from commands import ban

    message = Message()
    kwargs = dict(user="jan", channel=message.channel, message=message)
    result = ban.ban_user(**kwargs)
    return kwargs, result


@pytest.fixture
def fixture_unban():
    """Fixture to test unban user."""
    from commands import ban

    message = Message()
    kwargs = dict(user="fred", channel=message.channel, message=message)
    result = ban.unban_user(**kwargs)
    return kwargs, result


@pytest.fixture
def fixture_unbanall():
    """Fixture to test unbanning all users."""
    from commands import ban

    message = Message()
    kwargs = dict(user="jan", channel=message.channel, message=message)
    result = ban.unban_all(**kwargs)
    return kwargs, result, banned


@pytest.fixture
def fixture_notadmin():
    """Fixture to test non-admin command run."""
    from commands import ban

    message = Message(admins=[])
    kwargs = dict(user="jan", channel=message.channel, message=message)
    ban_result = ban.ban_user(**kwargs)
    unban_result = ban.unban_user(**kwargs)
    unbanall_result = ban.unban_all(**kwargs)
    return ban_result, unban_result, unbanall_result


def test_alias():
    """Test alias in commands.ban."""
    from commands import ban

    commands = ban.alias()
    assert "ban" in commands
    assert "unban" in commands
    assert "unbanall" in commands


def test_unbanall(fixture_unbanall):
    """Test unbanall functionality."""
    kwargs, unbanall, unbanned = fixture_unbanall
    assert unbanned == {}
    assert unbanall == "Cleared the ban list"


def test_ban(fixture_ban):
    """Test ban functionality."""
    kwargs, result = fixture_ban
    assert kwargs["message"].access.is_banned("jan")
    assert result == "User <@jan> is banned.\n"


def test_unban(fixture_unban):
    """Test unban functionality."""
    kwargs, result = fixture_unban
    assert not kwargs["message"].access.is_banned("fred")
    assert result == "User <@fred> is unbanned.\n"


def test_notadmin(fixture_notadmin):
    """Test non-admin filtering functionality."""
    ban_result, unban_result, unbanall_result = fixture_notadmin
    message = "<@bob>, you are not an admin"
    assert ban_result == message
    assert unban_result == message
    assert unbanall_result == message
