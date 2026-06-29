"""Ban command utilities."""


def alias():
    """Define separate commands and map them to functions."""
    return {
        "ban": ban_user,
        "unban": unban_user,
        "unbanall": unban_all,
    }


def ban_user(**kwargs: dict) -> str:
    """Ban a user from using commands."""
    user = kwargs.get("user")
    message = kwargs.get("message")
    access = message.access
    denied = access.require_admin(message)
    if denied:
        return denied
    if user == "none":
        return ""
    access.ban_user(user)
    return "User <@{0}> is banned.\n".format(user)


def unban_all(**kwargs: dict) -> str:
    """Unban all users."""
    message = kwargs.get("message")
    access = message.access
    denied = access.require_admin(message)
    if denied:
        return denied
    access.unban_all()
    return "Cleared the ban list"


def unban_user(**kwargs: dict) -> str:
    """Unban an existing user ban."""
    user = kwargs.get("user")
    message = kwargs.get("message")
    access = message.access
    denied = access.require_admin(message)
    if denied:
        return denied
    access.unban_user(user)
    return "User <@{0}> is unbanned.\n".format(user)


if __name__ == "__main__":
    print("RTFM")
