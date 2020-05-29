"""Example template test for new commands."""


import pytest


class Message(object):
    """Generate simple message object."""

    def __init__(self):
        """Initialize simple message object."""
        self.user = "bob"


def test_alias():
    """Test functionality of alias command."""
    from commands import template
    commands = template.alias()
    assert 'mycommand' in commands


def test_templateuserreturn():
    """Test template user return functionality."""
    from commands import template
    message = Message()
    kwargs = dict(message=message)
    assert template.my_command(**kwargs) == "bob"
