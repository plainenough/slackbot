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
    workdir = kwargs.get('workdir')
    if message.admin:
        try:
            with open('{0}/data/BANNED'.format(workdir), 'a') as banned_list:
                banned_list.write('{0}\n'.format(user))
            msg = 'User <@{0}> is banned.\n'.format(user)
        except Exception as e:
            msg = "Failed to load banned file, check permissions"
    else:
        message.channel = message.user
        msg = '<@{0}>, you are not an admin'.format(message.user)
    return msg


def unban_all(**kwargs: dict) -> str:
    """unban_all will unban all users"""
    message = kwargs.get('message')
    workdir = kwargs.get('workdir')
    if message.admin:
        with open('{0}/data/BANNED'.format(workdir), 'w') as banned_list:
            banned_list.write('')
        msg = 'Cleared the ban list'
    else:
        message.channel = message.user
        msg = '<@{0}>, you are not an admin'.format(message.user)
    return msg


def unban_user(**kwargs: dict) -> str:
    """unban_user will lift an existing user ban"""
    user = kwargs.get('user')
    message = kwargs.get('message')
    workdir = kwargs.get('workdir')
    if message.admin:
        with open('{0}/data/BANNED'.format(workdir), 'r') as banned_list:
            temp_list = banned_list.readlines()
        with open('{0}/data/BANNED'.format(workdir), 'w') as banned_list:
            for line in temp_list:
                if line.strip('\n') != user:
                    banned_list.write(line)
        msg = 'User <@{0}> is unbanned.\n'.format(user)
    else:
        message.channel = message.user
        msg = '<@{0}>, you are not an admin'.format(message.user)
    return msg


if __name__ == '__main__':
    print('RTFM')
