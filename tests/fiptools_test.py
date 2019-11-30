#!/usr/bin/env python3
import pytest


class Message(object):
    ''' Test class for command test '''

    def __init__(self):
        self._text = 'ban @<jan>'
        self.channel = '#general'
        self.user = 'bob'
        self.admin = True


score = {'fred': 1, 'bob': 2}


@pytest.fixture
def fixture_fiptools():
    from commands import fake_internet_points
    message = Message()
    kwargs = dict(user='bob',
                  channel=message.channel,
                  message=message,
                  score=score)
    mypoints = fake_internet_points.my_points(**kwargs)
    allpoints = fake_internet_points.all_points(**kwargs)
    return mypoints, allpoints


def test_alias():
    from commands import fake_internet_points
    commands = fake_internet_points.alias()
    assert 'mypoints' in commands
    assert 'scoreboard' in commands
    assert 'resetScores' in commands


def test_fipmypoints(fixture_fiptools):
    mypoints, allpoints = fixture_fiptools
    message = '<@bob> has 2 points'
    assert mypoints == message


def test_fipallpoints(fixture_fiptools):
    mypoints, allpoints = fixture_fiptools
    message = '<@bob> has a score of 2\n<@fred> has a score of 1\n'
    assert allpoints == message
