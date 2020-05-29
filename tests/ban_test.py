"""Test ban functionality."""


import pytest


banned = {'fred': True}


class Message(object):
    """Test class for command test."""

    def __init__(self):
        """Initialize testing object."""
        self._text = 'ban @<jan>'
        self._kwargs = dict(banned=banned)
        self.channel = '#general'
        self.user = 'bob'
        self.admin = True


@pytest.fixture
def fixture_ban():
    """Fixture to test ban user."""
    from commands import ban
    message = Message()
    kwargs = dict(user='jan',
                  channel=message.channel,
                  message=message)
    ban = ban.ban_user(**kwargs)
    return kwargs, ban


@pytest.fixture
def fixture_unban():
    """Fixture to test unban user."""
    from commands import ban
    message = Message()
    kwargs = dict(user='fred',
                  channel=message.channel,
                  message=message)
    unban = ban.unban_user(**kwargs)
    return kwargs, unban


@pytest.fixture
def fixture_unbanall():
    """Fixture to test unbanning all users."""
    from commands import ban
    message = Message()
    kwargs = dict(user='jan',
                  channel=message.channel,
                  message=message)
    unbanall = ban.unban_all(**kwargs)
    unbanned = message._kwargs.get('banned')
    return kwargs, unbanall, unbanned


@pytest.fixture
def fixture_notadmin():
    """Fixture to test non-admin command run."""
    from commands import ban
    message = Message()
    message.admin = False
    kwargs = dict(user='jan',
                  channel=message.channel,
                  message=message)
    _ban = ban.ban_user(**kwargs)
    unban = ban.unban_user(**kwargs)
    unbanall = ban.unban_all(**kwargs)
    return _ban, unban, unbanall


def test_alias():
    """Test alias in commands.ban."""
    from commands import ban
    commands = ban.alias()
    assert 'ban' in commands
    assert 'unban' in commands
    assert 'unbanall' in commands


def test_unbanall(fixture_unbanall):
    """Test unbanall functionality."""
    kwargs, unbanall, unbanned = fixture_unbanall
    assert unbanned == {}
    assert unbanall == 'Cleared the ban list'


def test_ban(fixture_ban):
    """Test ban functionality."""
    kwargs, ban = fixture_ban
    banned = kwargs.get('message')._kwargs.get('banned')
    assert banned.get('jan')
    assert ban == 'User <@jan> is banned.\n'


def test_unban(fixture_unban):
    """Test unban functionality."""
    kwargs, unban = fixture_unban
    banned = kwargs.get('message')._kwargs.get('banned')
    assert 'fred' not in banned
    assert unban == 'User <@fred> is unbanned.\n'


def test_notadmin(fixture_notadmin):
    """Test non-admin filtering functionality."""
    ban, unban, unbanall = fixture_notadmin
    message = '<@bob>, you are not an admin'
    assert ban == message
    assert unban == message
    assert unbanall == message
