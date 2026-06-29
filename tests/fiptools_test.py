"""Test tools around fake internet points."""


import pytest

from access import AccessControl


class Message(object):
    """Test stub for fake internet points commands."""

    def __init__(self, admins=None):
        self._text = "ban @<jan>"
        self.channel = "#general"
        self.user = "bob"
        score = {"fred": 1, "bob": 2}
        admin_list = ["bob"] if admins is None else admins
        self._kwargs = dict(score=score)
        self.access = AccessControl(admin_list, {})


@pytest.fixture
def fixture_fiptools():
    """Fixture for fiptools."""
    from commands import fake_internet_points

    message = Message()
    kwargs = dict(user="bob", channel=message.channel, message=message)
    mypoints = fake_internet_points.my_points(**kwargs)
    allpoints = fake_internet_points.all_points(**kwargs)
    return mypoints, allpoints


@pytest.fixture
def fixture_delpoints():
    """Fixture for fiptools."""
    from commands import fake_internet_points

    message = Message()
    message._text = "deleteScore <@fred>"
    kwargs = dict(user="fred", channel=message.channel, message=message)
    result = fake_internet_points.del_points(**kwargs)
    return result, message._kwargs


def test_alias():
    """Test alias functionality."""
    from commands import fake_internet_points

    commands = fake_internet_points.alias()
    assert "mypoints" in commands
    assert "scoreboard" in commands
    assert "resetScores" in commands


def test_fipmypoints(fixture_fiptools):
    """Test ability to list ones own points."""
    mypoints, _allpoints = fixture_fiptools
    assert mypoints == "<@bob> has 2 points"


def test_fipallpoints(fixture_fiptools):
    """Test display of all user points."""
    _mypoints, allpoints = fixture_fiptools
    assert allpoints == "<@bob> has a score of 2\n<@fred> has a score of 1\n"


def test_fipdelpoints(fixture_delpoints):
    """Test the ability for admin to delete user reference."""
    result, score = fixture_delpoints
    assert result == "<@fred> has been removed from the scoreboard"
    assert score.get("score") == {"bob": 2}
