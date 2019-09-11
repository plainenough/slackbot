#!/usr/bin/env python3


class FakeInternetPoints(object):
    """ A tracking system for fake internet points awarded
        by users for users.

        Atributes:
        awarder(str): The initator for change in FakeInternetPoints
        msg(str): The message posted by the bot
        subjects(list): Single or group of people affected by the awarder

        Methods:
        process_command: 

        Note:
        Fake internet points are really the main goal here.
        Under the hood we will really only be operating on
        a dictionary that will be flushed to dish on every
        change.
        """

    def __init__(self, message):
        self.awarder = message.user
        self.change = self.process_command(message.command)
        self.subjects = message.target_users

    def process_command(self, message):
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


