"""Fakeinternet ultilities."""


def alias():
    """Define separate commands and map them to functions."""
    return {
        "mypoints": my_points,
        "scoreboard": all_points,
        "deleteScore": del_points,
        "resetScores": reset_points,
    }


def my_points(**kwargs: dict) -> str:
    """Get user FakeInternetPoints count for user."""
    message = kwargs.get("message")
    user = message.user
    score = message._kwargs.get("score")
    if user in score:
        return "<@{0}> has {1} points".format(user, score[user])
    return "<@{0}> doesn't have points".format(user)


def all_points(**kwargs: dict) -> str:
    """Get a sorted list of fakeinternetpoints for team; requires admin."""
    message = kwargs.get("message")
    denied = message.access.require_admin(message)
    if denied:
        return denied
    score = message._kwargs.get("score")
    if score == {}:
        return "No one on your team has gained or lost any fake internet points"
    sorted_score = sorted(score, key=score.__getitem__, reverse=True)
    msg = ""
    for user in sorted_score:
        msg += "<@{0}> has a score of {1}\n".format(user, score[user])
    return msg


def reset_points(**kwargs: dict) -> str:
    """Reset scoreboard for entire team; requires admin."""
    message = kwargs.get("message")
    denied = message.access.require_admin(message)
    if denied:
        return denied
    message._kwargs.get("score").clear()
    return "All scores have been reset"


def del_points(**kwargs: dict) -> str:
    """Delete all points record for a user; requires admin."""
    user = kwargs.get("user")
    message = kwargs.get("message")
    denied = message.access.require_admin(message)
    if denied:
        return denied
    score = message._kwargs.get("score")
    if user in score:
        del score[user]
    return "<@{0}> has been removed from the scoreboard".format(user)
