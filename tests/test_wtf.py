"""Tests for wtf command."""

from unittest.mock import MagicMock

import requests

from access import AccessControl
from context import CommandContext
from commands import wtf


def _ctx(text):
    return CommandContext(
        actor_id="U1",
        channel_id="C1",
        text=text,
        target_users=[],
        access=AccessControl([], {}),
        score={},
        workdir="/tmp",
        commands={},
        reply_channel="C1",
    )


def test_too_long():
    result = wtf.get_def(context=_ctx("wtf_is " + ("x" * 31)))
    assert "too long" in result


def test_empty_term():
    result = wtf.get_def(context=_ctx("wtf_is"))
    assert "Usage" in result


def test_lookup_failure(monkeypatch):
    def boom(*args, **kwargs):
        raise requests.RequestException("timeout")

    monkeypatch.setattr(requests, "get", boom)
    result = wtf.check_ud("test")
    assert "Lookup failed" in result


def test_no_results(monkeypatch):
    response = MagicMock(ok=True, status_code=200)
    response.json.return_value = {"list": []}
    monkeypatch.setattr(requests, "get", lambda *a, **k: response)
    result = wtf.check_ud("notarealword12345")
    assert "No definition found" in result
