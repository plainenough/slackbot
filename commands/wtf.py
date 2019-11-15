#!/usr/bin/env python3


def alias():
    """ Custom commands and the functions they map too """
    alias = dict(
            wtf_is=get_def)
    return alias


def get_def(**kwargs: dict) -> str:
    """ This will lookup the string following wtfis """
    message = kwargs.get('message')
    message.channel = message.user
    mytext = message._text
    _text = mytext.split('wtfis')[-1]
    if len(_text) > 30:
        msg = 'Search term "{0}" is too long. ' 
        msg += "keep it under 30."
        return msg.format(_text)
    return check_ud(_text)


def check_ud(term):
    ''' This will lookup against urban dictionary '''
    import requests
    results = []
    url = 'http://api.urbandictionary.com/v0/define?term={0}'
    search = requests.get(url.format(term))
    data = search.json()
    results.append(data['list'][0]['definition'])
    msg = "Definition: \n\n{0}".format('\n\n'.join(results))
    return msg
