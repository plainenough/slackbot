"""Fakeinternet ultilities."""


def alias():
    """Define separate commands and map them to functions."""
    alias = dict(
            mypoints=my_points,
            scoreboard=all_points,
            deleteScore=del_points,
            resetScores=reset_points)
    return alias


def my_points(**kwargs: dict) -> str:
    """Get user FakeInternetPoints count for user."""
    user = kwargs.get('message').user
    score = kwargs.get('message')._kwargs.get('score')
    if user in score:
        msg = '<@{0}> has {1} points'.format(user, score[user])
    else:
        msg = "<@{0}> doesn't have points".format(user)
    return msg


def all_points(**kwargs: dict) -> str:
    """Get a sorted list of fakeinternetpoints for team; requires admin."""
    message = kwargs.get('message')
    score = message._kwargs.get('score')
    msg = ''
    if not kwargs['message'].admin:
        return msg
    if score == {}:
        msg = 'No one on your team has gained or lost any fake internet points'
    sorted_score = sorted(score, key=score.__getitem__)
    sorted_score.reverse()
    for user in sorted_score:
        msg += "<@{0}> has a score of {1}\n".format(user, score[user])
    return msg


def reset_points(**kwargs: dict) -> str:
    """Reset scoreboard for entire team; requires admin."""
    score = kwargs.get('message')._kwargs.get('score')
    msg = ''
    if not kwargs['message'].admin:
        return msg
    score.clear()
    msg = "All scores have been reset"
    return msg


def del_points(**kwargs: dict) -> str:
    """Delete all points record for a user; requires admin."""
    user = kwargs.get('user')
    score = kwargs.get('message')._kwargs.get('score')
    msg = ''
    if not kwargs['message'].admin:
        return msg
    if user in score:
        del score[user]
    msg = "<@{0}> has been removed from the scoreboard".format(user)
    return msg
