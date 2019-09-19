#!/usr/bin/env python3


class FakeInternetPoints(object):
    """ A tracking system for fake internet points awarded
        by users for users.

        Atributes:
        awarder(str): The initator for change in FakeInternetPoints
        change(int): The amount of information to be changed
        msg(str): The message posted by the bot

        Methods:
        check_valid_user: Verifies the user isn't giving themselves points
        process_command: Counts the qualifiers in a command
        set_user_points:

        Note:
        Fake internet points are really the main goal here.
        Under the hood we will really only be operating on
        a dictionary that will be flushed to dish on every
        change.
        """

    def __init__(self, message):
        self._subjects = message.target_users
        self.awarder = message.user
        self.change = self.process_command(message.command)
        self.msg = self.check_valid_user(message)

    def check_valid_user(self, message):
        if self.awarder in self.sunjects:
            _msg = "<@{0}> You are not allowed to assign yourself points."
            msg = _msg.format(self.awarder)
        else:
            msg = self.set_user_points()
        return msg

    def process_command(self, message):
        ''' Hardcoded to only allow a change of 5 or -5 '''
        _change = 0
        for value in message:
            if value == "+":
                _change += 1
            if value == "-":
                _change -= 1
        if _change < -5:
            _change = -5
        if _change > 5:
            _change = 5
        return _change

    def set_user_points(self, message):
        import pickle
        msg = '' 
        points = {}
        _scorefile = open('data/score', 'rb')
        scoredict = pickle.load(_scorefile)
        for user,value in scoredict.items():
            points[user] = int(value)
        for user in message.target_users:
            points[user] += self.change
            msg =+ "<@{0}> was given {1} points, \
                    now they have {2} total".format(
                            user,
                            self.change,
                            points[user])
        return msg
