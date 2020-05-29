"""Load all commands in the commands directory."""


def discover_commands(logging):
    """Discover files that exist in the commands directory.

    It will import those files and generate a dict with all
    of the predefined command aliases for each command. This
    will be templated and should be easy to understand.
    """
    file_list = filter_list(logging)
    commands = {}
    logging.debug("Checking files in file list for py extention.")
    for item in file_list:
        logging.debug("Checking file: {0}".format(item))
        if item.split('.')[1] == 'py':
            if __name__ == '__main__':
                _item = '{0}'.format(item.split('.')[0])
            else:
                _item = 'commands.{0}'.format(item.split('.')[0])
            check_alias(logging, _item, commands)
    return commands


def check_alias(logging, _item, commands):
    """Check imported commands for docstrings."""
    import importlib
    _aliases = {}
    _newcommand = importlib.import_module(_item)
    try:
        _aliases = _newcommand.alias()
    except Exception as e:
        logging.info("{0} did not have an alias function.".format(
            _item))
        logging.debug(e)
    logging.debug(_aliases)
    for alias, function in _aliases.items():
        commands[alias] = function
    return commands


def filter_list(logging):
    """Remove some files that don't need to be loaded into the slackbot."""
    import sys
    import os
    _mypath = os.path.abspath(__file__)
    MYWORKDIR = os.path.dirname(_mypath)
    logging.debug(MYWORKDIR)
    file_list = os.listdir(MYWORKDIR)
    _removal_list = ['__init__.py', '__pycache__', 'template.py']
    for item in _removal_list:
        logging.debug("removing {0}".format(item))
        file_list.remove(item)
    return file_list


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    print(discover_commands(logging))
