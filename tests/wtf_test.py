"""Test suite for wtf.py."""


import pytest


class Message(object):
    """Create simple message object for tests."""

    def __init__(self):
        """Initialize simple object for tests."""
        self._text = 'test because this string is too long to lookup'
        self.channel = '#general'
        self.user = 'bob'


@pytest.fixture
def fixture_wtf():
    """Fixture for wtf tests."""
    from commands import wtf
    message = Message()
    kwargs = dict(user=message.user,
                  channel=message.channel,
                  message=message)
    text = wtf.get_def(**kwargs)
    return message, text


def test_too_long(fixture_wtf):
    """Test for long strings."""
    message, text = fixture_wtf
    msg = 'Search term "{0}" is too long. '
    msg += "keep it under 30."
    msg = msg.format(message._text)
    assert text == msg
