"""Main function for slackbot."""


import logging
import sys
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
kwargs = {}


def set_args():
    """Set the default config/settings."""
    kwargs = dict(myworkdir=os.path.dirname(_mypath),
                  commands=discover_commands(logging),
                  slack_token=config.get('TOKEN'),
                  botid=config.get('BOTID'),
                  botuserid=config.get('BOTUSERID'),
                  botname=config.get('BOTNAME'),
                  admins=config.get('ADMINS'),
                  score=score,
                  banned=banned)
    return kwargs


@RTMClient.run_on(event="message")
def catch_message(**payload):
    """Slack provided example to retrieve a message from slack."""
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
    """Return the processed message using the web client."""
    web_client.chat_postMessage(
        username=config.get('BOTNAME'),
        user=config.get('BOTUSERID'),
        icon_emoji=":{0}:".format(config.get('BOTNAME')),
        channel=message.channel,
        text=message.msg)
    return


async def save_to_disk(fname, data, **kwargs):
    """Worker to save data to disk."""
    logging.debug("starting {0} worker".format(fname))
    while True:
        await asyncio.sleep(30)
        mwd = kwargs.get('myworkdir')
        myfile = open('{0}/data/{1}'.format(mwd, fname), 'wb')
        pickle.dump(data, myfile)
        myfile.close()
    return


async def check_for_runners(loop):
    """Check if worker dies. If so, kill the process."""
    while True:
        await asyncio.sleep(10)
        if len(asyncio.Task.all_tasks(loop)) < 5:
            logging.error("A worker died. So should I. :(")
            tasks = []
            sys.exit(1)
        else:
            logging.debug("{0} Runners in loop.".format(
                len(asyncio.Task.all_tasks(loop))))
    return


def pull_from_disk(fname):
    """Retrive saved content off disk."""
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
    """Run slack RTM server."""
    logging.info("starting client")
    slack_token = config.get('TOKEN')
    rtm_client = RTMClient(token=slack_token)
    rtm_client.start()
    return


def main():
    """Execute setup and start the application."""
    loop = asyncio.get_event_loop()
    score = pull_from_disk('score')
    banned = pull_from_disk('banned')
    asyncio.ensure_future(run_client(**kwargs))
    asyncio.ensure_future(save_to_disk('score', score, **kwargs))
    asyncio.ensure_future(save_to_disk('banned', banned, **kwargs))
    asyncio.ensure_future(check_for_runners(loop))
    loop.run_forever()
    return


if __name__ == '__main__':
    kwargs = set_args()
    main()
