"""Test tools around fake internet points."""


import pytest


class Message(object):
    """Test class for command test."""

    def __init__(self):
        """Initialize simple message object."""
        self._text = 'ban @<jan>'
        self.channel = '#general'
        self.user = 'bob'
        self.admin = True
        score = {'fred': 1, 'bob': 2}
        self._kwargs = dict(score=score)


@pytest.fixture
def fixture_fiptools():
    """Fixture for fiptools."""
    from commands import fake_internet_points
    message = Message()
    kwargs = dict(user='bob',
                  channel=message.channel,
                  message=message)
    mypoints = fake_internet_points.my_points(**kwargs)
    allpoints = fake_internet_points.all_points(**kwargs)
    return mypoints, allpoints


@pytest.fixture
def fixture_delpoints():
    """Fixture for fiptools."""
    from commands import fake_internet_points
    message = Message()
    message._text = 'deleteScore <@fred>'
    kwargs = dict(user='fred',
                  channel=message.channel,
                  message=message)
    mypoints = fake_internet_points.del_points(**kwargs)
    score = message._kwargs
    return mypoints, score


def test_alias():
    """Test alias functionality."""
    from commands import fake_internet_points
    commands = fake_internet_points.alias()
    assert 'mypoints' in commands
    assert 'scoreboard' in commands
    assert 'resetScores' in commands


def test_fipmypoints(fixture_fiptools):
    """Test ability to list ones own points."""
    mypoints, allpoints = fixture_fiptools
    message = '<@bob> has 2 points'
    assert mypoints == message


def test_fipallpoints(fixture_fiptools):
    """Test display of all user points."""
    mypoints, allpoints = fixture_fiptools
    message = '<@bob> has a score of 2\n<@fred> has a score of 1\n'
    assert allpoints == message


def test_fipdelpoints(fixture_delpoints):
    """Test the ability for admin to delete user reference."""
    mypoints, score = fixture_delpoints
    message = '<@fred> has been removed from the scoreboard'
    assert mypoints == message
    assert score.get('score') == {'bob': 2}
