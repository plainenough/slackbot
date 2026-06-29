"""Test FakeInternetPoints functionality."""

import pytest

from access import AccessControl
from context import CommandContext
from fake_points import FakeInternetPoints


def _ctx(user, targets, fip_change, score=None):
    score = score or {}
    return CommandContext(
        actor_id=user,
        channel_id="C1",
        text="",
        target_users=targets,
        access=AccessControl([], {}),
        score=score,
        workdir="/tmp",
        commands={},
        reply_channel="C1",
        fip_change=fip_change,
    )


@pytest.fixture
def fixture_fip():
    ctx = _ctx("bob", ["FRED"], "++")
    return FakeInternetPoints(user="FRED", context=ctx)


@pytest.fixture
def fixture_fip_self():
    ctx = _ctx("bob", ["bob"], "++")
    return FakeInternetPoints(user="bob", context=ctx)


@pytest.fixture
def fixture_fip_negative():
    ctx = _ctx("bob", ["FRED"], "--")
    return FakeInternetPoints(user="FRED", context=ctx)


@pytest.fixture
def fixture_fip_gtv():
    ctx = _ctx("bob", ["FRED"], "+++++++++")
    pfip = FakeInternetPoints(user="FRED", context=ctx)
    ctx.fip_change = "-------"
    nfip = FakeInternetPoints(user="FRED", context=ctx)
    return pfip, nfip


def test_awarder(fixture_fip):
    assert fixture_fip.awarder == "bob"


def test_change(fixture_fip):
    assert fixture_fip.change == 1


def test_message(fixture_fip):
    assert fixture_fip.msg == "<@FRED> has changed by 1 point, now they have 1 in total.\n"


def test_awarder_self(fixture_fip_self):
    assert fixture_fip_self.msg == "<@bob> You are not allowed to assign yourself points."


def test_change_gtv(fixture_fip_gtv):
    pfip, nfip = fixture_fip_gtv
    assert pfip.change == 5
    assert nfip.change == -5


def test_change_negative(fixture_fip_negative):
    assert fixture_fip_negative.change == -1
