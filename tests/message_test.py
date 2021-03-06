"""Test functionality of message class."""


import pytest


def ban(**kwargs):
    """Return true."""
    return 'True'


banned = {'NOADMIN': True}


@pytest.fixture
def fixture_message():
    """Fixture to test message."""
    from message import Message
    import os
    _mypath = os.path.abspath(__file__)
    myworkdir = os.path.dirname(_mypath)
    mycommands = dict(ban=ban)
    kwargs = dict(myworkdir=myworkdir,
                  commands=mycommands,
                  banned=banned,
                  admins=['UEMN5QPLM'])
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
    """Fixture to test non-admin message."""
    from message import Message
    import os
    _mypath = os.path.abspath(__file__)
    myworkdir = os.path.dirname(_mypath)
    #  Just a message I captured from my bot.
    mycommands = dict(ban=ban)
    kwargs = dict(myworkdir=myworkdir,
                  commands=mycommands,
                  banned=banned,
                  admins=['UEMN5QPLM'])
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


@pytest.fixture
def fixture_deleted_message():
    """Fixture to test deleted event message."""
    from message import Message
    import os
    _mypath = os.path.abspath(__file__)
    myworkdir = os.path.dirname(_mypath)
    #  Just a message I captured from my bot.
    mycommands = dict(ban=ban)
    kwargs = dict(myworkdir=myworkdir,
                  commands=mycommands,
                  banned=banned,
                  admins=['UEMN5QPLM'])
    _message = {'subtype': 'message_deleted',
                'hidden': True, 'deleted_ts': '1572708401.008200',
                'channel': 'CETRYVBDW',
                'previous_message':
                {'client_msg_id': '00ee0609-0b8b-4e14-b77d-36fcf0648182'},
                'event_ts': '1572708432.008400', 'ts': '1572708432.008400'}
    msg = Message(_message, **kwargs)
    return msg


@pytest.fixture
def fixture_bot_message():
    """Fixture to test bot message."""
    from message import Message
    import os
    _mypath = os.path.abspath(__file__)
    myworkdir = os.path.dirname(_mypath)
    mycommands = dict(ban=ban)
    kwargs = dict(myworkdir=myworkdir,
                  commands=mycommands,
                  banned=banned,
                  admins=['UEMN5QP'],
                  botid='ISABOT')
    #  Just a message I captured from my bot.
    _message = {'client_msg_id': 'just-a-message-id',
                'suppress_notification': False,
                'text': 'ban <@FRED>',
                'user': 'ISABOT',
                #  'bot_id': 'ISABOT',
                'team': 'TEMBBDTK6',
                'user_team': 'TEMBBDTK6',
                'source_team': 'TEMBBDTK6',
                'channel': 'CETRYVBDW',
                'event_ts': '1570120295.029800',
                'ts': '1570120295.029800'}
    msg = Message(_message, **kwargs)
    return msg


def test_message_user(fixture_message):
    """Test user assignment."""
    message = fixture_message
    assert message.user == 'UEMN5QPLM'


def test_message_channel(fixture_message):
    """Test channel assignment."""
    message = fixture_message
    assert message.channel == 'CETRYVBDW'


def test_user_is_admin(fixture_message):
    """Test if user is admin."""
    message = fixture_message
    assert message.admin is True


def test_user_not_banned(fixture_message):
    """Test user is not banned."""
    message = fixture_message
    assert message.banned is False


def test_message_command(fixture_message):
    """Test command identification."""
    message = fixture_message
    assert message.command == ban


def test_user_not_admin(fixture_message_not_admin):
    """Test if user is not admin."""
    message = fixture_message_not_admin
    assert message.admin is False


def test_user_is_banned(fixture_message_not_admin):
    """Test if user is banned."""
    message = fixture_message_not_admin
    assert message.banned is True


def test_message_delete(fixture_deleted_message):
    """Test for deleted message notification."""
    message = fixture_deleted_message
    assert message.msg == ''


def test_bot_message(fixture_bot_message):
    """Test if message originates from a bot."""
    message = fixture_bot_message
    assert message.msg == ''
