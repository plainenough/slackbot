#!/usr/bin/env python3
"""Main entry point for slackbot (Socket Mode)."""

import logging
import os
import signal
import sys
import threading
import time

from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse

from commands import discover_commands
from config import obtain_config
from message import Message
from storage import load_state, save_state, start_save_worker

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
STOP_EVENT = threading.Event()


def configure_logging(workdir):
    os.makedirs(os.path.join(workdir, "data"), exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M",
        handlers=[
            logging.FileHandler(os.path.join(workdir, "data", "slackbot.log")),
            logging.StreamHandler(sys.stdout),
        ],
    )


def build_kwargs(config):
    score, banned = load_state(WORK_DIR)
    return {
        "myworkdir": WORK_DIR,
        "commands": discover_commands(logging),
        "slack_token": config.get("BOT_TOKEN"),
        "botid": config.get("BOTID"),
        "botuserid": config.get("BOTUSERID"),
        "botname": config.get("BOTNAME", "slackbot"),
        "admins": config.get("ADMINS", []),
        "score": score,
        "banned": banned,
    }


def send_message(message, web_client, config):
    if not message.msg:
        return
    web_client.chat_postMessage(
        channel=message.channel,
        text=message.msg,
        username=config.get("BOTNAME", "slackbot"),
        icon_emoji=":{0}:".format(config.get("BOTNAME", "slackbot")),
    )


def handle_message_event(event, web_client, config, kwargs):
    message = Message(event, **kwargs)
    if message.msg == "":
        logging.debug("Empty response; skipping post")
        return
    send_message(message, web_client, config)


def main():
    configure_logging(WORK_DIR)
    config = obtain_config(logging)
    kwargs = build_kwargs(config)

    web_client = WebClient(token=config.get("BOT_TOKEN"))
    socket_client = SocketModeClient(
        app_token=config.get("APP_TOKEN"),
        web_client=web_client,
    )

    start_save_worker(WORK_DIR, kwargs["score"], kwargs["banned"], STOP_EVENT)

    def process(client: SocketModeClient, req: SocketModeRequest):
        try:
            if req.type == "events_api":
                event = req.payload.get("event", {})
                if event.get("type") == "message":
                    handle_message_event(event, web_client, config, kwargs)
        except Exception:
            logging.exception("Failed to process socket mode request")
        finally:
            client.send_socket_mode_response(
                SocketModeResponse(envelope_id=req.envelope_id)
            )

    socket_client.socket_mode_request_listeners.append(process)

    def shutdown(_signum, _frame):
        logging.info("Shutting down slackbot")
        STOP_EVENT.set()
        socket_client.close()

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    logging.info("Connecting to Slack via Socket Mode")
    socket_client.connect()
    try:
        while not STOP_EVENT.is_set():
            time.sleep(1)
    finally:
        save_state(WORK_DIR, kwargs["score"], kwargs["banned"])
        socket_client.disconnect()
        logging.info("Shutdown complete")


if __name__ == "__main__":
    main()
