#!/usr/bin/env python3


def alias():
    """ Custom commands and the functions they map too """
    #  This is a required portion of the commands to actually
    #  load all of the variations and new methods. Your commands
    #  can leverage the kwargs object. This will include wether
    #  not your user is banned or an admin.
    alias = dict(
            help_me=generate_help)
    return alias


def generate_help(**kwargs):
    """ Pulls the doc string out of all of the commands """
    message = kwargs.get('message')
    commands = message._list_commands
    # This directs the message to the user.
    message.channel = message.user
    ret = '\n'.join(['{:<30}: {}'.format(name, func.__doc__.strip())
                     for name, func in sorted(commands.items())])
    return '```{}```'.format(ret)