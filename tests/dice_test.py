"""Test dice roll functionality."""


import pytest


class Message(object):
    """Test class for command test."""

    def __init__(self):
        """Initialize simple message object for dice roll."""
        self._text = 'roll d10'
        self.channel = '#general'
        self.user = 'bob'


@pytest.fixture
def fixture_dice():
    """Ficture for dice roll."""
    from commands import dice
    commands = dice.alias()
    message = Message()
    kwargs = dict(user=message.user,
                  channel=message.channel,
                  message=message)
    myroll = dice.roll(**kwargs)
    return commands, myroll


@pytest.fixture
def fixture_bad_dice():
    """Ficture for bad dice roll."""
    from commands import dice
    commands = dice.alias()
    message = Message()
    message._text = 'roll d20+1'
    kwargs = dict(user=message.user,
                  channel=message.channel,
                  message=message)
    myroll = dice.roll(**kwargs)
    return commands, myroll


@pytest.fixture
def fixture_d0_dice():
    """Ficture for d0 roll."""
    from commands import dice
    commands = dice.alias()
    message = Message()
    message._text = 'roll d0'
    kwargs = dict(user=message.user,
                  channel=message.channel,
                  message=message)
    myroll = dice.roll(**kwargs)
    return commands, myroll


@pytest.fixture
def fixture_d1_dice():
    """Ficture for d1 roll."""
    from commands import dice
    commands = dice.alias()
    message = Message()
    message._text = 'roll d1'
    kwargs = dict(user=message.user,
                  channel=message.channel,
                  message=message)
    myroll = dice.roll(**kwargs)
    return commands, myroll


def test_alias():
    """Test alias functionality."""
    from commands import dice
    commands = dice.alias()
    assert 'roll' in commands


def test_roll(fixture_dice):
    """Test valid roll functionality."""
    commands, myroll = fixture_dice
    value = int(myroll.split('is')[1])
    assert value >= 0
    assert value <= 10


def test_bad_roll(fixture_bad_dice):
    """Test bad dice logic functionality."""
    commands, myroll = fixture_bad_dice
    assert myroll == ''


def test_d0_roll(fixture_d0_dice):
    """Test zero dice logic functionality."""
    commands, myroll = fixture_d0_dice
    assert myroll == ''


def test_d1_roll(fixture_d1_dice):
    """Test dest 1 sided dice functionality."""
    commands, myroll = fixture_d1_dice
    value = int(myroll.split('is')[1])
    assert value == 1
