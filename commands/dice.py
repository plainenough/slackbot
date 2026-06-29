"""Dice utilities."""

from context import get_context


def alias():
    """Define separate commands and map them to functions."""
    return {"roll": roll}


def roll(**kwargs):
    """Roll a dice: roll d20."""
    ctx = get_context(kwargs)
    parts = [part for part in ctx.text.split() if part != "roll"]
    return generate_message(parts)


def generate_message(commands):
    """Construct the message for dice roll."""
    import random

    msg = ""
    for com in commands:
        if "d" not in com:
            continue
        try:
            upper = int(com.split("d")[1]) + 1
        except (ValueError, IndexError):
            continue
        if upper < 2:
            continue
        msg += "\nYour {0} roll is {1}".format(com, random.randrange(1, upper))
    return msg
