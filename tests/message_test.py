#!/usr/bin/env python3
import pytest


@pytest.fixture
def fixture_message():
    from main import Message
    import os
    _mypath = os.path.abspath(__file__)
    MYWORKDIR = os.path.dirname(_mypath)
    #  Writing a blank banned file for this fixture
    with open('data/BANNED', 'w') as _bannedfile:
        _bannedfile.write('')
    #  Just a message I captured from my bot.
    ADMINS = ['UEMN5QPLM']
    COMMAND = ['ban']
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
    message = Message(_message)
    return message


@pytest.fixture
def fixture_message_not_admin():
    import os
    _mypath = os.path.abspath(__file__)
    MYWORKDIR = os.path.dirname(_mypath)
    from main import Message
    #  Writing a banned user.
    with open('data/BANNED', 'w') as _bannedfile:
        _bannedfile.write('NOADMIN\n')
    #  Just a message I captured from my bot.
    ADMINS = [ ]
    COMMAND = ['ban']
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
    message = Message(_message)
    return message


def test_message_user(fixture_message):
    message = fixture_message
    assert message.user == 'UEMN5QPLM'


def test_message_channel(fixture_message):
    message = fixture_message
    assert message.channel == 'CETRYVBDW'


def test_user_is_admin(fixture_message):
    message = fixture_message
    assert message.admin == True


def test_user_not_banned(fixture_message):
    message = fixture_message
    assert message.banned == False


def test_message_command(fixture_message):
    message = fixture_message
    assert message.command == 'ban'


def test_user_not_admin(fixture_message_not_admin):
    message = fixture_message_not_admin
    assert message.admin == False


def test_user_is_banned(fixture_message_not_admin):
    message = fixture_message_not_admin
    assert message.banned == True
    
