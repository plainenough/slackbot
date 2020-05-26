#!/usr/bin/env python3


class FakeInternetPoints(object):
    """ A tracking system for fake internet points awarded
        by users for users.
        Atributes:
        awarder(str): The initator for change in FakeInternetPoints
        change(int): The amount of information to be changed
        msg(str): The message posted by the bot

        Methods:
        check_upper_value: Confirms an int isnt >5 or <-5
        check_valid_user: Verifies the user isn't giving themselves points
        process_command: Counts the qualifiers in a command
        set_user_points: Loads existing points and appends new values to dict

        Note:
        Fake internet points are really the main goal here.
        Under the hood we will really only be operating on
        a dictionary that will be flushed to dish on every
        change.
        """

    def __init__(self, **comargs):
        self.message = comargs.get('message')
        self._kwargs = self.message._kwargs
        self._command = self.message._fipchange
        self._subjects = self.message.target_users
        self.awarder = self.message.user
        self.change = self.process_command(self._command)
        self.msg = self.check_valid_user(self.message)

    def check_valid_user(self, message):
        if self.awarder in self._subjects:
            _msg = "<@{0}> You are not allowed to assign yourself points."
            msg = _msg.format(self.awarder)
        else:
            msg = self.set_user_points(message)
        return msg

    def process_command(self, message):
        """ Counts all of the values to generate a number """
        _change = 0
        count = 0
        for value in self._command:
            if count == 0:
                count += 1
                #  skip the first record so it requires two ++ to get a point
                continue
            if value == "+":
                _change += 1
            if value == "-":
                _change -= 1
        return self.check_upper_value(_change)

    def check_upper_value(self, _change):
        """ Hardcoded to only allow a change of 5 or -5 """
        if _change < -5:
            _change = -5
        if _change > 5:
            _change = 5
        return _change

    def set_user_points(self, message):
        """ Adds users points to score dict """
        msg = ''
        score = message._kwargs.get('score')
        for user in message.target_users:
            _msg1 = "<@{0}> has changed by {1} "
            _msg2 = ", now they have {2} in total.\n"
            if user in score:
                score[user] += self.change
            else:
                score[user] = self.change
            if self.change == 0:
                return msg
            elif self.change in [1, -1]:
                _msg = "{0}point{1}".format(_msg1, _msg2)
            else:
                _msg = "{0}points{1}".format(_msg1, _msg2)
            msg += _msg.format(user,
                               self.change,
                               score[user])
        return msg
