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
    mytext = message.text
    _text = mytext.split('wtfis')[-1]
    if len(_text) > 20:
        msg = "Search term too long"
        message.channel = message.user
        return msg
    return check_ud(_text)


def check_ud(term):
    import requests
    results = []
    url = 'http://api.urbandictionary.com/v0/define?term={0}'
    search = requests.get(url.format(term))
    data = search.json()
    for item in data['list']:
        myitem = str(item['definition'])
        results.append(myitem)
    msg = "Definitions: \n\n{0}".format('\n\n'.join(results))
    return msg