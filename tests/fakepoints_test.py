#!/usr/bin/env python3
import pytest


class Message(object):
    ''' Test class for command test '''

    def __init__(self):
        self._text = '<@FRED> ++ for good work homie'
        self.channel = '#general'
        self.user = 'bob'
        self.target_users = ['FRED']
        score = {}
        self._kwargs = dict(score=score)


@pytest.fixture
def fixture_fip():
    import fake_points
    message = Message()
    #  Writing an empty score file
    message._fipchange = "++"
    comargs = dict(message=message)
    fip = fake_points.FakeInternetPoints(**comargs)
    return fip


@pytest.fixture
def fixture_fip_self():
    import fake_points
    message = Message()
    #  Writing an empty score file
    score = {}
    message._fipchange = "++"
    message.target_users = ['bob']
    comargs = dict(message=message)
    fip = fake_points.FakeInternetPoints(**comargs)
    return fip


@pytest.fixture
def fixture_fip_negative():
    import fake_points
    message = Message()
    #  Writing an empty score file
    score = {}
    message._fipchange = "--"
    comargs = dict(message=message)
    fip = fake_points.FakeInternetPoints(**comargs)
    return fip


@pytest.fixture
def fixture_fip_gtv():
    import fake_points
    message = Message()
    #  Writing an empty score file
    score = {}
    message._fipchange = "+++++++++"
    comargs = dict(message=message)
    pfip = fake_points.FakeInternetPoints(**comargs)
    message._fipchange = "-------"
    nfip = fake_points.FakeInternetPoints(**comargs)
    return pfip, nfip


def test_awarder(fixture_fip):
    fip = fixture_fip
    assert fip.awarder == 'bob'


def test_change(fixture_fip):
    fip = fixture_fip
    assert fip.change == 1


def test_message(fixture_fip):
    fip = fixture_fip
    _msg1 = "<@FRED> has changed by 1 "
    _msg2 = ", now they have 1 in total.\n"
    msg = "{0}point{1}".format(_msg1, _msg2)
    assert fip.msg == msg


def test_awarder_self(fixture_fip_self):
    fip = fixture_fip_self
    msg = "<@bob> You are not allowed to assign yourself points."
    assert fip.msg == msg


def test_change_gtv(fixture_fip_gtv):
    pfip, nfip = fixture_fip_gtv
    assert pfip.change == 5
    assert nfip.change == -5


def test_change_negative(fixture_fip_negative):
    fip = fixture_fip_negative
    assert fip.change == -1
