#!/usr/bin/env python3
import pytest


@pytest.fixture
def fixture_fip():
    from fake_points import FakeInternetPoints
    from main import Message
    import pickle
    #  Writing a blank banned file for this fixture
    with open('data/BANNED', 'w') as _bannedfile:
        _bannedfile.write('')
    #  Writing an empty score file
    _score = {}
    with open('data/score', 'wb') as _scorefile:
        pickle.dump(_score, _scorefile)
    #  Just a message I captured from my bot.
    _message = {'client_msg_id': 'just-a-message-id',
                'suppress_notification': False,
                'text': '<@FRED> ++ for good work homie',
                'user': 'UEMN5QPLM',
                'team': 'TEMBBDTK6',
                'user_team': 'TEMBBDTK6',
                'source_team': 'TEMBBDTK6',
                'channel': 'CETRYVBDW',
                'event_ts': '1570120295.029800',
                'ts': '1570120295.029800'}
    message = Message(_message)
    fip_object = FakeInternetPoints(message)
    return message, fip_object


@pytest.fixture
def fixture_fip_self():
    from fake_points import FakeInternetPoints
    from main import Message
    import pickle
    #  Writing a blank banned file for this fixture
    with open('data/BANNED', 'w') as _bannedfile:
        _bannedfile.write('')
    #  Writing an empty score file
    _score = {}
    with open('data/score', 'wb') as _scorefile:
        pickle.dump(_score, _scorefile)
    #  Just a message I captured from my bot.
    _message = {'client_msg_id': 'just-a-message-id',
                'suppress_notification': False,
                'text': '<@UEMN5QPLM> ++ for good work homie',
                'user': 'UEMN5QPLM',
                'team': 'TEMBBDTK6',
                'user_team': 'TEMBBDTK6',
                'source_team': 'TEMBBDTK6',
                'channel': 'CETRYVBDW',
                'event_ts': '1570120295.029800',
                'ts': '1570120295.029800'}
    message = Message(_message)
    fip_object = FakeInternetPoints(message)
    return message, fip_object


@pytest.fixture
def fixture_fip_negative():
    #  Setup for checking on negative points.
    from fake_points import FakeInternetPoints
    from main import Message
    import pickle
    #  Writing a blank banned file for this fixture
    with open('data/BANNED', 'w') as _bannedfile:
        _bannedfile.write('')
    #  Writing an empty score file
    _score = {}
    with open('data/score', 'wb') as _scorefile:
        pickle.dump(_score, _scorefile)
    #  Just a message I captured from my bot.
    _message = {'client_msg_id': 'just-a-message-id',
                'suppress_notification': False,
                'text': '<@FRED> -- for bad work homie',
                'user': 'UEMN5QPLM',
                'team': 'TEMBBDTK6',
                'user_team': 'TEMBBDTK6',
                'source_team': 'TEMBBDTK6',
                'channel': 'CETRYVBDW',
                'event_ts': '1570120295.029800',
                'ts': '1570120295.029800'}
    message = Message(_message)
    fip_object = FakeInternetPoints(message)
    return message, fip_object


@pytest.fixture
def fixture_fip_gtv():
    #  Setup for a point change > 5
    from fake_points import FakeInternetPoints
    from main import Message
    import pickle
    #  Writing a blank banned file for this fixture
    with open('data/BANNED', 'w') as _bannedfile:
        _bannedfile.write('')
    #  Writing an empty score file
    _score = {}
    with open('data/score', 'wb') as _scorefile:
        pickle.dump(_score, _scorefile)
    #  Just a message I captured from my bot.
    _message = {'client_msg_id': 'just-a-message-id',
                'suppress_notification': False,
                'text': '<@FRED> +++++++++ for good work homie',
                'user': 'UEMN5QPLM',
                'team': 'TEMBBDTK6',
                'user_team': 'TEMBBDTK6',
                'source_team': 'TEMBBDTK6',
                'channel': 'CETRYVBDW',
                'event_ts': '1570120295.029800',
                'ts': '1570120295.029800'}
    message = Message(_message)
    fip_object = FakeInternetPoints(message)
    return message, fip_object


def test_awarder(fixture_fip):
    message, fip = fixture_fip
    assert fip.awarder == 'UEMN5QPLM'


def test_targets(fixture_fip):
    message, fip = fixture_fip
    assert message.target_users == ['FRED']


def test_change(fixture_fip):
    message, fip = fixture_fip
    assert fip.change == 1


def test_message(fixture_fip):
    message, fip = fixture_fip
    msg = ''
    _msg1 = "<@{0}> has changed by {1} "
    _msg2 = ", now they have {2} points in total.\n"
    _msg = "{0}point{1}".format(_msg1, _msg2)
    for user in message.target_users:
        msg += _msg.format(user,
                           fip.change,
                           1)
    assert fip.msg == msg


def test_awarder_self(fixture_fip_self):
    message, fip = fixture_fip_self
    _msg = "<@{0}> You are not allowed to assign yourself points."
    msg = _msg.format(fip.awarder)
    assert fip.msg == msg


def test_change_gtv(fixture_fip_gtv):
    message, fip = fixture_fip_gtv
    assert fip.change == 5


def test_change_negative(fixture_fip_negative):
    message, fip = fixture_fip_negative
    assert fip.change == -1
