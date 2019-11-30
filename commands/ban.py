#!/usr/bin/env python3


def alias():
    commands = dict(ban=ban_user,
                    unban=unban_user,
                    unbanall=unban_all)
    return commands


def ban_user(**kwargs: dict) -> str:
    """ban_user will ban a user from using commands"""
    user = kwargs.get('user')
    message = kwargs.get('message')
    banned = kwargs.get('banned')
    if user == 'none':
        return ''
    if message.admin:
        banned[user] = True
        msg = 'User <@{0}> is banned.\n'.format(user)
    else:
        message.channel = message.user
        msg = '<@{0}>, you are not an admin'.format(message.user)
    return msg


def unban_all(**kwargs: dict) -> str:
    """unban_all will unban all users"""
    message = kwargs.get('message')
    banned = kwargs.get('banned')
    if message.admin:
        banned.clear()
        msg = 'Cleared the ban list'
    else:
        message.channel = message.user
        msg = '<@{0}>, you are not an admin'.format(message.user)
    return msg


def unban_user(**kwargs: dict) -> str:
    """unban_user will lift an existing user ban"""
    user = kwargs.get('user')
    message = kwargs.get('message')
    banned = kwargs.get('banned')
    if message.admin:
        banned.pop(user, None)
        msg = 'User <@{0}> is unbanned.\n'.format(user)
    else:
        message.channel = message.user
        msg = '<@{0}>, you are not an admin'.format(message.user)
    return msg


if __name__ == '__main__':
    print('RTFM')
