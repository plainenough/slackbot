#!/usr/bin/env python3
import logging
import os
import pickle
import threading
import time
from slack import RTMClient
from commands import discover_commands
from config import obtain_config
from message import Message

score = {}
banned = {}

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
              admins=config.get('ADMINS'),
              score=score,
              banned=banned)


@RTMClient.run_on(event="message")
def catch_message(**payload):
    data, web_client = payload.get('data'), payload.get('web_client')
    logging.debug(data)
    message = Message(data, **kwargs)
    logging.debug(message)
    if message.msg == '':
        logging.debug("Empty message: skip processing, nothing to return")
        return
    send_message(message, web_client)
    return


def send_message(message, web_client):
    web_client.chat_postMessage(
        username=config.get('BOTNAME'),
        user=config.get('BOTUSERID'),
        channel=message.channel,
        text=message.msg)
    return


def save_to_disk(fname, data):
    while True:
        time.sleep(30)
        mwd = kwargs.get(myworkdir)
        myfile = open('{0}/data/{1}'.format(mwd, fname), 'wb')
        pickle.dump(data, myfile)
        myfile.close()
    return


def pull_from_disk(fname):
    try:
        mwd = kwargs.get(myworkdir)
        myfile = open('{0}/data/{1}'.format(mwd, fname), 'rb')
        data = pickle.load(myfile)
        kwargs[fname] = data
        myfile.close()
    except Exception as error:
        text = "Failed to load filename: {0} --- {1}"
        logging.debug(text.format(fname, error))
        data = {}
    return data


def main():
    slack_token = config.get('TOKEN')
    rtm_client = RTMClient(token=slack_token)
    score = pull_from_disk('score')
    banned = pull_from_disk('banned')
    score = threading.Thread(target=save_to_disk, args=('score', score))
    banned = threading.Thread(target=save_to_disk, args=('banned', banned))
    client = threading.Thread(target=rtm_client.start, args=())
    logging.info("Starting score threading")
    score.start()
    logging.info("Starting banned threading")
    banned.start()
    logging.info("Starting client threading")
    client.start()
    score.join()
    banned.join()
    client.join()
    return


if __name__ == '__main__':
    import sys
    try:
        main()
    except KeyboardInterrupt:
        logging.info("User interupt, stopping application")
        sys.exit(1)
