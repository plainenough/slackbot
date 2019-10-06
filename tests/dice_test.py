#!/usr/bin/env python3
import pytest


@pytest.fixture
def fixture_dice():
    from commands import dice
    commands = dice.alias()
    user, channel, text = 'bob', '#general', 'roll d10'
    kwargs = dict(user=user,
                  channel=channel,
                  text=text)
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
