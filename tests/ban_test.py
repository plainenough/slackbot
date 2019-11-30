#!/usr/bin/env python3
import pytest


class Message(object):
    ''' Test class for command test '''

    def __init__(self):
        self._text = 'ban @<jan>'
        self.channel = '#general'
        self.user = 'bob'
        self.admin = True

banned = {'fred': True}

@pytest.fixture
def fixture_ban():
    from commands import ban
    message = Message()
    kwargs = dict(user='jan',
                  channel=message.channel,
                  message=message,
                  banned=banned)
    ban = ban.ban_user(**kwargs)
    return kwargs, ban


@pytest.fixture
def fixture_unban():
    from commands import ban
    message = Message()
    kwargs = dict(user='fred',
                  channel=message.channel,
                  message=message,
                  banned=banned)
    unban = ban.unban_user(**kwargs)
    return kwargs, unban


@pytest.fixture
def fixture_unbanall():
    from commands import ban
    message = Message()
    kwargs = dict(user='jan',
                  channel=message.channel,
                  message=message,
                  banned=banned)
    unbanall = ban.unban_all(**kwargs)
    unbanned = kwargs.get('banned')
    return kwargs, unbanall, unbanned


@pytest.fixture
def fixture_notadmin():
    from commands import ban
    message = Message()
    message.admin = False
    kwargs = dict(user='jan',
                  channel=message.channel,
                  message=message,
                  banned=banned)
    _ban = ban.ban_user(**kwargs)
    unban = ban.unban_user(**kwargs)
    unbanall = ban.unban_all(**kwargs)
    return _ban, unban, unbanall


def test_unbanall(fixture_unbanall):
    kwargs, unbanall, unbanned  = fixture_unbanall
    assert unbanned == {}
    assert unbanall == 'Cleared the ban list'


def test_ban(fixture_ban):
    kwargs, ban  = fixture_ban
    banned = kwargs.get('banned')
    assert banned.get('jan') == True
    assert ban == 'User <@jan> is banned.\n'


def test_unban(fixture_unban):
    kwargs, unban  = fixture_unban
    banned = kwargs.get('banned')
    assert 'fred' not in banned
    assert unban == 'User <@fred> is unbanned.\n'


def test_notadmin(fixture_notadmin):
    ban, unban, unbanall = fixture_notadmin
    message = '<@bob>, you are not an admin'
    assert ban == message
    assert unban == message
    assert unbanall == message
