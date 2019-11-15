#!/usr/bin/env python3


def alias():
    """ Custom commands and the functions they map too """
    #  This is a required portion of the commands to actually
    #  load all of the variations and new methods. Your commands
    #  can leverage the kwargs object. This will include wether
    #  not your user is banned or an admin.
    alias = dict(
            wtfis=get_def)
    return alias


def get_def(**kwargs: dict) -> str:
    """ This will lookup the string following wtfis """
    message = kwargs.get('message')
    message.channel = message.user
    mytext = message._text
    _text = mytext.split('wtfis')[-1]
    if len(_text) > 30:
        msg = 'Search term "{0}" is too long. ' 
        msg += "keep it under 30.".format(_text)
        return msg
    return check_ud(_text)


def check_ud(term):
    import requests
    results = []
    url = 'http://api.urbandictionary.com/v0/define?term={0}'
    search = requests.get(url.format(term))
    data = search.json()
    results.append(data['list'][0]['definition'])
    msg = "Definition: \n\n{0}".format('\n\n'.join(results))
    return msg
