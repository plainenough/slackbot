#!/usr/bin/env python3
import pytest


class Message(object):
    """ A test class """

    def __init__(self):
        self._list_commands = dict(mycmd=mycmd)
        self._text = "help"
        self.user = "bob"


def mycmd():
    """ returns true """
    return True


def test_alias():
    from commands import help
    commands = help.alias()
    assert 'help' in commands


def test_printout():
    from commands import help
    message = Message()
    kwargs = dict(message=message)
    msg = '```mycmd                         : returns true```'
    assert msg == help.generate_help(**kwargs)
    assert message.channel == "bob"
