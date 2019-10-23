#!/usr/bin/env python3
import pytest

@pytest.fixture
def fixture_message():
    from message import Message
    import os
    _mypath = os.path.abspath(__file__)
    myworkdir = os.path.dirname(_mypath)
    kwargs = dict(myworkdir = '{0}'.format(myworkdir),
                  commands = ['ban'],
                  admins = ['UEMN5QPLM'])
    #  Just a message I captured from my bot.
    _message = {'client_msg_id': 'just-a-message-id',
                'suppress_notification': False,
                'text': 'ban <@FRED>',
                'user': 'UEMN5QPLM',
                'team': 'TEMBBDTK6',
                'user_team': 'TEMBBDTK6',
                'source_team': 'TEMBBDTK6',
                'channel': 'CETRYVBDW',
                'event_ts': '1570120295.029800',
                'ts': '1570120295.029800'}
    msg = Message(_message, **kwargs)
    return msg


@pytest.fixture
def fixture_message_not_admin():
    from message import Message
    import os
    _mypath = os.path.abspath(__file__)
    myworkdir = os.path.dirname(_mypath)
    #  Just a message I captured from my bot.
    kwargs = dict(myworkdir = '{0}'.format(myworkdir),
                  commands = ['ban'],
                  admins = ['UEMN5QPLM'])
    _message = {'client_msg_id': 'just-a-message-id',
                'suppress_notification': False,
                'text': '<@FRED> ++ for good work homie',
                'user': 'NOADMIN',
                'team': 'TEMBBDTK6',
                'user_team': 'TEMBBDTK6',
                'source_team': 'TEMBBDTK6',
                'channel': 'CETRYVBDW',
                'event_ts': '1570120295.029800',
                'ts': '1570120295.029800'}
    msg = Message(_message, **kwargs)
    return msg


def test_message_user(fixture_message):
    message = fixture_message
    assert message.user == 'UEMN5QPLM'


def test_message_channel(fixture_message):
    message = fixture_message
    assert message.channel == 'CETRYVBDW'


def test_user_is_admin(fixture_message):
    message = fixture_message
    assert message.admin is True


def test_user_not_banned(fixture_message):
    message = fixture_message
    assert message.banned is False


def test_message_command(fixture_message):
    message = fixture_message
    assert message.command == 'ban'


def test_user_not_admin(fixture_message_not_admin):
    message = fixture_message_not_admin
    assert message.admin is False


def test_user_is_banned(fixture_message_not_admin):
    message = fixture_message_not_admin
    assert message.banned is True
