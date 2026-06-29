"""Integration tests for socket mode handlers."""

from unittest.mock import MagicMock

from access import AccessControl
from bot_state import BotState
from commands import dice
from main import handle_slash_command, process_socket_request


def test_dispatch_roll_command():
    from bot_state import BotState
    from dispatcher import CommandDispatcher
    from message_parser import MessageParser

    access = AccessControl([], {})
    state = BotState(
        workdir="/tmp",
        commands=dice.alias(),
        access=access,
        score={},
        banned={},
    )
    parsed = MessageParser.parse_slash(
        {"command": "/roll", "text": "d6", "user_id": "U1", "channel_id": "C1"},
        state,
    )
    response = CommandDispatcher(state).dispatch(parsed)
    assert "d6" in response.text


def test_handle_slash_command_posts_message():
    access = AccessControl([], {})
    kwargs = {
        "myworkdir": "/tmp",
        "commands": dice.alias(),
        "access": access,
        "score": {},
        "banned": {},
        "botid": "",
        "botuserid": "",
    }
    web_client = MagicMock()
    config = {"BOTNAME": "slackbot"}
    handle_slash_command(
        {"command": "/roll", "text": "d20", "user_id": "U1", "channel_id": "C1"},
        web_client,
        config,
        kwargs,
    )
    web_client.chat_postMessage.assert_called_once()


def test_process_socket_request_slash():
    kwargs = {
        "myworkdir": "/tmp",
        "commands": dice.alias(),
        "access": AccessControl([], {}),
        "score": {},
        "banned": {},
    }
    web_client = MagicMock()
    req = MagicMock(type="slash_commands", payload={"command": "/roll", "text": "d6", "user_id": "U1", "channel_id": "C1"})
    process_socket_request(req, web_client, {"BOTNAME": "slackbot"}, kwargs)
    web_client.chat_postMessage.assert_called_once()

