#!/usr/bin/env python3


def alias():
    """ Custom commands and the functions they map too """
    #  This is a required portion of the commands to actually
    #  load all of the variations and new methods. Your commands
    #  can leverage the kwargs object. This will include wether
    #  not your user is banned or an admin.
    alias = dict(
            mycommand=my_command)
    return alias


def my_command(**kwargs: dict) -> str:
    """ A quick description of my_command """
    msg = kwargs['message'].user
    return msg