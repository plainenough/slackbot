"""Generate help message from docstrings."""


def alias():
    """Load custom commands and the functions they map too."""
    alias = dict(help=generate_help)
    return alias


def generate_help(**kwargs):
    """Pull the doc string out of all of the commands."""
    message = kwargs.get('message')
    commands = message._list_commands
    if len(message._text) > 25:
        return ''
    # This directs the message to the user.
    message.channel = message.user
    ret = '\n'.join(['{:<30}: {}'.format(name, func.__doc__.strip())
                     for name, func in sorted(commands.items())])
    return '```{}```'.format(ret)
