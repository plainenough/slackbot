#!/usr/bin/env python3
import logging
import os
from slack import RTMClient
from commands import discover_commands
from config import obtain_config


_log = logging.basicConfig(level=logging.DEBUG,
                           format='%(asctime)s %(name)-12s %(levelname)-8s' +
                           ' %(message)s',
                           datefmt='%m-%d %H:%M',
                           filename='data/slackbot.log')
_mypath = os.path.abspath(__file__)
config = obtain_config(logging)
kwargs = dict(logging = _log,
              myworkdir = os.path.dirname(_mypath),
              commands = discover_commands(_log),
              slack_token = config.get('TOKEN'),
              botid = config.get('BOTID'),
              botuserid = config.get('BOTUSERID'),
              botname = config.get('BOTNAME'),
              admins = config.get('ADMINS'))


@RTMClient.run_on(event="message")
def catch_message(**payload):
    data = payload['data']
    logging = kwargs.get('logging')
    web_client = payload['web_client']
    logging.debug(data)
    #  This bit might be able to be moved into message.Message class
    if data.get('bot_id') == kwargs.get('botid'):
        logging.info('No reply it is the bot')
        return
    elif data.get('subtype') == 'message_changed':
        logging.info('Message was updated')
        return
    elif data.get('subtype') == 'bot_message':
        return
    #  end section
    message = Message(data)
    logging.debug(message)
    #  This portion might be able to be migrated into the message.Message class
    if message.banned:
        if message.command:
            msg = "<@{0}> you are banned, reach out to an admin".format(
                   message.user)
        else:
            return None
    else:
        msg = process_work(message)
    #  end section
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

#  This section might also be migrated in to the message.Message class
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
    if _message.command == 'help':
        return command
    if command:
        logging.debug("Splitting up target users from: {0}".format(
            _message.target_users))
        for _user in _message.target_users:
            kwargs = dict(user=_user,
                          message=_message,
                          workdir=MYWORKDIR)
            logging.debug(kwargs)
            msg += command(**kwargs)
    return msg
#  end section

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
