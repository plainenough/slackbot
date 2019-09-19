#!/usr/bin/env python3


def alias():
    """ Custom commands and the functions they map too """
    #  This is a required portion of the commands to actually
    #  load all of the variations and new methods. Your commands
    #  can leverage the kwargs object. This will include wether
    #  not your user is banned or an admin.
    alias = dict(
            mypoints=my_points)
    return alias


def my_points(**kwargs: dict) -> str:
    """ Get user FakeInternetPoints count """
    import pickle
    user = kwargs['message'].user
    try:
        _scorefile = open('data/score', 'rb')
        _scoredict = pickle.load(_scorefile)
        _scorefile.close()
    except Exception:
        _scoredict = { }
    if user in _scoredict:
        msg = '<@{0}> has {1} points'.format(user, _scoredict[user])
    else:
        msg = "<@{0}> doesn't have points".format(user)
    return msg
