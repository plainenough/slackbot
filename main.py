"""Main function for slackbot."""


import asyncio
from commands import discover_commands
import logging
from message import Message
import os
import pickle
import requests
from slack_sdk.rtm import RTMClient
import sys
import threading
import time

score = {}
banned = {}

token = os.getenv('TOKEN')
log_level = os.getenv('LOGLEVEL')

logging.basicConfig(level=logging."{0}".format(log_level.upper()),
                    format='%(asctime)s %(name)-12s %(levelname)-8s' +
                    ' %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='data/slackbot.log')
_mypath = os.path.abspath(__file__)
kwargs = {}

def get_slack_users():
    """Retrieve slack user list and other settings."""
    HEADER = {"Authorization": "Bearer {0}".format(token)}
    URL = "https://slack.com/api/users.list"
    userlist = requests.post(URL, headers=HEADER)
    return userlist.content


def set_args():
    """Set the default config/settings."""
    userlist = get_slack_users()
    kwargs = dict(myworkdir=os.path.dirname(_mypath),
                  users=userlist,
                  commands=discover_commands(logging),
                  score=score,
                  banned=banned)
    return kwargs


@RTMClient.run_on(event="message")
async def catch_message(**payload):
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


async def save_to_disk(fname, data):
    """Worker to save data to disk."""
    logging.info("Starting {0} worker".format(fname))
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
            loop.stop()
        else:
            logging.debug("{0} Runners in loop.".format(
                len(asyncio.Task.all_tasks(loop))))
    return


def pull_from_disk(fname):
    """Retrive saved content off disk."""
    try:
        logging.info("Loading {0} from disk".format(fname))
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


async def run_client(loop, **kwargs):
    """Run slack RTM server."""
    logging.info("starting client")
    rtm_client = RTMClient(token=token, loop=loop, run_async=True)
    rtm_client.start()
    logging.info("started client server")
    return


def main():
    """Execute setup and start the application."""
    loop = asyncio.get_event_loop()
    score = pull_from_disk('score')
    banned = pull_from_disk('banned')
    asyncio.ensure_future(run_client(loop, **kwargs))
    asyncio.ensure_future(save_to_disk('score', score))
    asyncio.ensure_future(save_to_disk('banned', banned))
    asyncio.ensure_future(check_for_runners(loop))
    logging.info("running loop forever")
    loop.run_forever()
    return


if __name__ == '__main__':
    kwargs = set_args()
    main()
