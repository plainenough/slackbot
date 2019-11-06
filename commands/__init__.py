#!/usr/bin/env python3


def discover_commands(logging):
    """ This function will discover files that exist in the CWD.
        It will import those files and generate a dict with all
        of the predefined command aliases for each command. This
        will be templated and should be easy to understand.
    """
    import os
    import sys
    import importlib
    _mypath = os.path.abspath(__file__)
    MYWORKDIR = os.path.dirname(_mypath)
    logging.debug(MYWORKDIR)
    _removal_list = ['__init__.py', '__pycache__', 'template.py']
    file_list = os.listdir(MYWORKDIR)
    logging.info("Remove files in the ban list - files to not import.")
    for item in _removal_list:
        logging.debug("removing {0}".format(item))
        file_list.remove(item)
    commands = {}
    logging.debug("Checking files in file list for py extention.")
    for item in file_list:
        _aliases = {}
        logging.debug("Checking file: {0}".format(item))
        if item.split('.')[1] == 'py':
            if __name__ == '__main__':
                _item = '{0}'.format(item.split('.')[0])
            else:
                _item = 'commands.{0}'.format(item.split('.')[0])
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


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    print(discover_commands(logging))
