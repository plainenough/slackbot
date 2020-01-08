#!/usr/bin/env python3
import pytest


class Message(object):
    """ A test class """

    def __init__(self):
        self.user = "bob"


def test_alias():
    from commands import template
    commands = template.alias()
    assert 'mycommand' in commands


def test_templateuserreturn():
    from commands import template
    message = Message()
    kwargs = dict(message=message)
    assert template.my_command(**kwargs) == "bob"
