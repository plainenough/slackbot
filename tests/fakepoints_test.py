"""Test FakeInternetPoints functionality."""


import pytest


class Message(object):
    """Define simple message object for testing."""

    def __init__(self):
        """Initialize simple message object."""
        self._text = '<@FRED> ++ for good work homie'
        self.channel = '#general'
        self.user = 'bob'
        self.target_users = ['FRED']
        score = {}
        self._kwargs = dict(score=score)


@pytest.fixture
def fixture_fip():
    """Fixture for adding fake points."""
    import fake_points
    message = Message()
    #  Writing an empty score file
    message._fipchange = "++"
    comargs = dict(message=message, user=message.target_users[0])
    fip = fake_points.FakeInternetPoints(**comargs)
    return fip


@pytest.fixture
def fixture_fip_self():
    """Fixture for adding points to self."""
    import fake_points
    message = Message()
    #  Writing an empty score file
    score = {}
    message._fipchange = "++"
    message.target_users = ['bob']
    comargs = dict(message=message, user=message.target_users[0])
    fip = fake_points.FakeInternetPoints(**comargs)
    return fip


@pytest.fixture
def fixture_fip_negative():
    """Fixture for removing fake points."""
    import fake_points
    message = Message()
    #  Writing an empty score file
    score = {}
    message._fipchange = "--"
    comargs = dict(message=message, user=message.target_users[0])
    fip = fake_points.FakeInternetPoints(**comargs)
    return fip


@pytest.fixture
def fixture_fip_gtv():
    """Fixture for adding/removing too many fake points."""
    import fake_points
    message = Message()
    #  Writing an empty score file
    score = {}
    message._fipchange = "+++++++++"
    comargs = dict(message=message, user=message.target_users[0])
    pfip = fake_points.FakeInternetPoints(**comargs)
    message._fipchange = "-------"
    nfip = fake_points.FakeInternetPoints(**comargs)
    return pfip, nfip


def test_awarder(fixture_fip):
    """Test target user."""
    fip = fixture_fip
    assert fip.awarder == 'bob'


def test_change(fixture_fip):
    """Test point increment."""
    fip = fixture_fip
    assert fip.change == 1


def test_message(fixture_fip):
    """Test message for correct format."""
    fip = fixture_fip
    _msg1 = "<@FRED> has changed by 1 "
    _msg2 = ", now they have 1 in total.\n"
    msg = "{0}point{1}".format(_msg1, _msg2)
    assert fip.msg == msg


def test_awarder_self(fixture_fip_self):
    """Test functionality about adding points to ones self."""
    fip = fixture_fip_self
    msg = "<@bob> You are not allowed to assign yourself points."
    assert fip.msg == msg


def test_change_gtv(fixture_fip_gtv):
    """Test point change limitations."""
    pfip, nfip = fixture_fip_gtv
    assert pfip.change == 5
    assert nfip.change == -5


def test_change_negative(fixture_fip_negative):
    """Test functionality for negative additions."""
    fip = fixture_fip_negative
    assert fip.change == -1
