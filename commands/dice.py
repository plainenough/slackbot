"""Dice utilities."""


def alias():
    """Define separate commands and map them to functions."""
    commands = dict(roll=roll)
    return commands


def roll(**kwargs: dict) -> str:
    """Roll a dice: roll d20."""
    message = kwargs.get('message')
    _commands = []
    for com in message._text.split():
        if com == 'roll' or '':
            continue
        _commands.append(com)
    return generate_message(_commands)


def generate_message(_commands):
    """Construct the message for dice roll."""
    import random
    msg = ''
    for com in _commands:
        if 'd' not in com:
            continue
        try:
            upper = int(com.split('d')[1]) + 1
        except Exception:
            continue
        if upper < 2:
            continue
        msg += "\nYour {0} roll is {1}".format(com, random.randrange(1, upper))
    return msg


if __name__ == '__main__':
    print('RTFM')
