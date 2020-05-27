"""Template for new commands."""

def alias():
    """Define separate commands and map them to functions."""
    #  This is a required portion of the commands to actually
    #  load all of the variations and new methods. Your commands
    #  can leverage the message and kwargs object.
    alias = dict(
            mycommand=my_command)
    return alias


def my_command(**kwargs: dict) -> str:
    """Describe my_command functionality."""
    msg = kwargs['message'].user
    return msg
