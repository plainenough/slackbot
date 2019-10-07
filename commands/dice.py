#!/usr/bin/env python3


def alias():
    commands = dict(roll=roll)
    return commands


def roll(**kwargs: dict) -> str:
    """rolls a dice: roll d20 """
    import random
    user = kwargs.get('user')
    channel = kwargs.get('channel')
    msg_text = kwargs.get('text')
    _commands = []
    msg = ''
    for com in msg_text.split():
        if com == 'roll' or '':
            continue
        _commands.append(com)
    for com in _commands:
        if 'd' not in com:
            continue
        upper = int(com.split('d')[1]) + 1
        msg += "\nYour {0} roll is {1}".format(com, random.randrange(1, upper))
    return msg


if __name__ == '__main__':
    print('RTFM')
