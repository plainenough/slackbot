#!/usr/bin/env python3
import pytest


class Message(object):
    ''' Test class for command test '''

    def __init__(self):
        self._text = 'wtf_is test because this string is too long to lookup'
        self.channel = '#general'
        self.user = 'bob'


@pytest.fixture
def fixture_wtf():
    from commands import wtf
    message = Message()
    kwargs = dict(user=message.user,
                  channel=message.channel,
                  message=message)
    text = wtf.get_def(**kwargs)
    return message, text


def test_too_long(fixture_wtf):
    message, text = fixture_wtf
    msg = 'Search term "{0}" is too long. '
    msg += "keep it under 30."
    msg = msg.format(message._text)
    assert text == msg
