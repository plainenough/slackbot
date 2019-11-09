#!/usr/bin/env python3
import pytest

class Message(object):
    ''' Test class for command test '''

    def __init__(self):
        self._text = 'roll d10'
        self.channel = '#general'
        self.user = 'bob'


@pytest.fixture
def fixture_dice():
    from commands import dice
    commands = dice.alias()
    message = Message()
    kwargs = dict(user=message.user,
                  channel=message.channel,
                  message=message)
    myroll = dice.roll(**kwargs)
    return commands, myroll


def test_alias(fixture_dice):
    commands, myroll = fixture_dice
    assert commands


def test_roll(fixture_dice):
    commands, myroll = fixture_dice
    value = int(myroll.split('is')[1])
    assert value >= 0
    assert value <= 10
