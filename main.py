#!/usr/bin/env python3
import logging
import os
from slack import RTMClient
from commands import discover_commands
from config import obtain_config

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s' +
                    ' %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='data/slackbot.log')

_mypath = os.path.abspath(__file__)
MYWORKDIR = os.path.dirname(_mypath)
COMMANDS = discover_commands(logging)
CONFIG = obtain_config(logging)
slack_token = CONFIG.get('TOKEN')
BOTID = CONFIG.get('BOTID')
BOTUSERID = CONFIG.get('BOTUSERID')
BOTNAME = CONFIG.get('BOTNAME')
ADMINS = CONFIG.get('ADMINS')


class Message(object):
    """ A message returned from the slack RTM Client

    Attributes:
    admin(bool): User admin status
    banned(bool): User ban status
    channel(str): A channel ID from slack
    commands(str): First command from text, Defaults to empty value
    text(str): The original un-edited value from the RTM client
    target_users(str): Obtain user ids fortarge users from text
    user(str): A user ID from slack

    Methods:
    check_admin: Checks if user is an admin
    check_banned: Checks if the user is banned
    check_command: Checks for first command in text
    check_user: Checks for users in text

    Note:
    This just creates a message object based on the returned payload from
    slack. I expect overloading the msg attribute will ultimately be the
    correct way to set a value there. I only intend on tageting the first
    command in an individual post.
    """

    def __init__(self, data):
        _text = data['text']
        _user = data['user']
        self.admin = self.check_admin(_user)
        self.banned = self.check_banned(_user)
        self.channel = data['channel']
        self.command = self.check_command(_text)
        self.text = _text
        self.target_users = self.check_users(_text)
        self.user = _user
        self._logger = logging.getLogger(__name__)

    def __str__(self):
        value = "\nUSER:{0}\nTARGETS:{1}\n"
        value += "COMMAND:{2}\nORIGINAL_TEXT:{3}\n"
        value += "ADMIN:{4}\nBANNED:{5}\n"
        format_value = value.format(
                self.user,
                self.target_users,
                self.command,
                self.text,
                self.admin,
                self.banned)
        return format_value

    def check_admin(self, user):
        ''' Checks to see if the user is an admin: returns boolean '''
        if user in ADMINS:
            logging.debug('{0} is an admin'.format(user))
            return True
        else:
            logging.debug('{0} is not an admin'.format(user))
            return False

    def check_banned(self, user):
        ''' Checks to see if the user is banned: returns boolean '''
        try:
            banned_users = []
            with open('{0}/data/BANNED'.format(MYWORKDIR), 'r') as _banfile:
                for banneduser in _banfile.read().split('\n'):
                    banned_users.append(banneduser)
            if user in banned_users:
                logging.info("{0} is banned".format(user))
                return True
        except Exception as e:
            logging.info("Banned file doesn't exist")
            logging.debug(e)
        return False

    def check_command(self, text):
        ''' Grabs the first command from text: intentially only one '''
        command = ''
        if text == '':
            return command
        for value in text.split(' '):
            if value in COMMANDS:
                command = value
            if value.startswith('-') or value.startswith('+'):
                logging.info('Detected fake_points event')
                command = {'fake_points': value}
        return command

    def check_users(self, text):
        ''' Grabs all of the user ids from the text: returns list '''
        import re
        target_users = []
        reg = re.compile('<@.*>')
        for value in text.split(' '):
            if reg.match(value):
                if value in target_users:
                    #  This little gem is to prevent multiple entries for
                    #  a user in the list inspired by Dylan
                    continue
                target_users.append(value.strip('<>@'))
        return target_users


@RTMClient.run_on(event="message")
def catch_message(**payload):
    web_client = payload['web_client']
    data = payload['data']
    if data.get('bot_id') == BOTID:
        logging.info('No reply it is the bot')
        logging.debug(data)
        return
    elif data.get('subtype') == 'message_changed':
        logging.info('Message was updated')
        return
    elif data.get('subtype') == 'bot_message':
        return
    print(payload)
    message = Message(data)
    logging.debug(message)
    if message.banned:
        if message.command:
            msg = "<@{0}> you are banned, reach out to an admin".format(
                   message.user)
        else:
            return None
    else:
        msg = process_work(message)
    if msg == '':
        logging.debug("Empty message: return None")
        return None
    else:
        web_client.chat_postMessage(
                username=BOTNAME,
                user=BOTUSERID,
                channel=message.channel,
                text=msg)
    return


def process_work(_message):
    logging.info("Processing command: {0}".format(_message.command))
    msg = ''
    if 'fake_points' in _message.command:
        from fake_points import FakeInternetPoints
        logging.info("fake_points event")
        process_points = FakeInternetPoints(_message)
        logging.debug(process_points)
        return process_points.msg
    command = COMMANDS.get(_message.command)
    if command:
        logging.debug("Splitting up target users from: {0}".format(
            _message.target_users))
        if _message.command == 'unbanall':
            _message.target_users.append('unbanall')
        for _user in _message.target_users:
            kwargs = dict(user=_user,
                          message=_message,
                          workdir=MYWORKDIR)
            logging.debug(kwargs)
            msg += command(**kwargs)
    return msg


def main():
    rtm_client = RTMClient(token=slack_token)
    rtm_client.start()


if __name__ == '__main__':
    import sys
    try:
        main()
    except KeyboardInterrupt:
        logging.info("User interupt, stopping application")
        sys.exit(1)
