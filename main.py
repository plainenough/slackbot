#!/usr/bin/env python3
import logging
import os
from slack import RTMClient
from commands import discover_commands
from config import obtain_config
from message import Message

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s' +
                    ' %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='data/slackbot.log')
_mypath = os.path.abspath(__file__)
config = obtain_config(logging)
kwargs = dict(myworkdir=os.path.dirname(_mypath),
              commands=discover_commands(logging),
              slack_token=config.get('TOKEN'),
              botid=config.get('BOTID'),
              botuserid=config.get('BOTUSERID'),
              botname=config.get('BOTNAME'),
              admins=config.get('ADMINS'))


@RTMClient.run_on(event="message")
def catch_message(**payload):
    data = payload.get('data')
    logging.debug(data)
    message = Message(data, **kwargs)
    logging.debug(message)
    if message.msg == '':
        logging.debug("Empty message: skip processing, nothing to return")
        return
    send_message(message, payload)
    return


def send_message(message, payload):
    web_client = payload['webclient']
    web_client.chat_postMessage(
        username=config.get('BOTNAME'),
        user=config.get('BOTUSERID'),
        channel=message.channel,
        text=message.msg)
    return


def main():
    slack_token = config.get('TOKEN')
    rtm_client = RTMClient(token=slack_token)
    rtm_client.start()


if __name__ == '__main__':
    import sys
    try:
        main()
    except KeyboardInterrupt:
        logging.info("User interupt, stopping application")
        sys.exit(1)
