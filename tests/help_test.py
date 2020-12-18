"""Test for help message generation."""


import pytest


class Message(object):
    """Create simple message object."""

    def __init__(self):
        """Initialize simple testing object."""
        self._list_commands = dict(mycmd=mycmd)
        self._text = "help"
        self.user = "bob"


def mycmd():
    """Return true."""
    return True


def test_alias():
    """Test alias functionality in help commands."""
    from commands import help
    commands = help.alias()
    assert 'help' in commands


def test_printout():
    """Test help message generation."""
    from commands import help
    message = Message()
    kwargs = dict(message=message)
    msg = '```mycmd                         : Return true.```'
    assert msg == help.generate_help(**kwargs)
    assert message.channel == "bob"
