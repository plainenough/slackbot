#!/usr/bin/env python3
import logging
import os
import pickle
import threading
import time
import asyncio
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


async def save_to_disk(fname, data, **kwargs):
    while True:
        await asyncio.sleep(30)
        mwd = kwargs.get('myworkdir')
        myfile = open('{0}/data/{1}'.format(mwd, fname), 'wb')
        pickle.dump(data, myfile)
        myfile.close()
    return


def pull_from_disk(fname):
    try:
        mwd = kwargs.get('myworkdir')
        myfile = open('{0}/data/{1}'.format(mwd, fname), 'rb')
        data = pickle.load(myfile)
        kwargs[fname] = data
        myfile.close()
    except Exception as error:
        text = "Failed to load filename: {0} --- {1}"
        logging.debug(text.format(fname, error))
        data = {}
    return data


async def run_client(**kwargs):
    try:
        print("starting client")
        slack_token = config.get('TOKEN')
        rtm_client = RTMClient(token=slack_token)
        rtm_client.start()
    except Exception as error:
        logging.debug(error)
    return


def main():
    loop = asyncio.get_event_loop()
    score = pull_from_disk('score')
    banned = pull_from_disk('banned')
    try:
        asyncio.ensure_future(run_client(**kwargs))
        asyncio.ensure_future(save_to_disk('score', score, **kwargs))
        asyncio.ensure_future(save_to_disk('banned', banned, **kwargs))
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()
    return


if __name__ == '__main__':
    import sys
    try:
        main()
    except KeyboardInterrupt:
        logging.info("User interupt, stopping application")
        sys.exit(1)
