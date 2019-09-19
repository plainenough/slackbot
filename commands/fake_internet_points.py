#!/usr/bin/env python3


def alias():
    """ Custom commands and the functions they map too """
    #  This is a required portion of the commands to actually
    #  load all of the variations and new methods. Your commands
    #  can leverage the kwargs object. This will include wether
    #  not your user is banned or an admin.
    alias = dict(
            mypoints=my_points,
            scoreboard=all_points,
            resetScores=reset_points)
    return alias


def my_points(**kwargs: dict) -> str:
    """ Get user FakeInternetPoints count for user """
    import pickle
    user = kwargs['message'].user
    try:
        _scorefile = open('data/score', 'rb')
        _scoredict = pickle.load(_scorefile)
        _scorefile.close()
    except Exception:
        _scoredict = {}
    if user in _scoredict:
        msg = '<@{0}> has {1} points'.format(user, _scoredict[user])
    else:
        msg = "<@{0}> doesn't have points".format(user)
    return msg


def all_points(**kwargs: dict) -> str:
    """ Get a sorted list of fakeinternetpoints for team; requires admin """
    import pickle
    msg = ''
    if not kwargs['message'].admin:
        return msg
    try:
        _scorefile = open('data/score', 'rb')
        _scoredict = pickle.load(_scorefile)
        _scorefile.close()
    except Exception:
        return msg
    if _scoredict == {}:
        msg = 'No one on your team has gained or lost any fake internet points.'
    sorted_score = sorted(_scoredict, key=_scoredict.__getitem__)
    sorted_score.reverse()
    for user in sorted_score:
        msg += "<@{0}> has a score of {1}\n".format(user, _scoredict[user])
    return msg

def reset_points(**kwargs: dict) -> str:
    """ Resets scoreboard for entire team; requires admin """
    import pickle
    msg = ''
    if not kwargs['message'].admin:
        return msg
    _mydict = {}
    _scorefile = open('data/score', 'wb')
    pickle.dump(_mydict, _scorefile)
    _scorefile.close()
    msg = "All scores have been reset"
    return msg
