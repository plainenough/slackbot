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
        load_score_file: Loads scorefile from disc
        process_command: Counts the qualifiers in a command
        set_user_points: Loads existing points and appends new values to dict

        Note:
        Fake internet points are really the main goal here.
        Under the hood we will really only be operating on
        a dictionary that will be flushed to dish on every
        change.
        """

    def __init__(self, message):
        self._kwargs = message._kwargs
        self._command = message._fipchange
        self._subjects = message.target_users
        self.awarder = message.user
        self.change = self.process_command(self._command)
        self.msg = self.check_valid_user(message)

    def check_valid_user(self, message):
        if self.awarder in self._subjects:
            _msg = "<@{0}> You are not allowed to assign yourself points."
            msg = _msg.format(self.awarder)
        else:
            msg = self.set_user_points(message)
        return msg

    def load_score_file(self):
        ''' Handles Loading the score file '''
        import pickle
        myworkdir = self._kwargs.get('myworkdir')
        try:
            _scorefile = open('{0}/data/score'.format(myworkdir), 'rb')
        except Exception as error:
            points = {}
            _scorefile = open('{0}/data/score'.format(myworkdir), 'wb')
            pickle.dump(points, _scorefile)
            _scorefile.close
            _scorefile = open('{0}/data/score'.format(myworkdir), 'rb')
        scoredict = pickle.load(_scorefile)
        _scorefile.close()
        return scoredict

    def process_command(self, message):
        ''' Hardcoded to only allow a change of 5 or -5 '''
        _change = 0
        count = 0
        for value in message:
            if count == 0:
                count += 1
                #  skip the first record so it requires two ++ to get a point
                continue
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
        """ Extracts dict from pickle rewrites on change. """
        import pickle
        msg = ''
        points = {}
        scoredict = self.load_score_file()
        for user, value in scoredict.items():
            points[user] = int(value)
        for user in message.target_users:
            _msg1 = "<@{0}> has changed by {1} "
            _msg2 = ", now they have {2} in total.\n"
            if user in points:
                points[user] += self.change
            else:
                points[user] = self.change
            if self.change == 0:
                return msg
            elif self.change in [1, -1]:
                _msg = "{0}point{1}".format(_msg1, _msg2)
            else:
                _msg = "{0}points{1}".format(_msg1, _msg2)
            msg += _msg.format(user,
                               self.change,
                               points[user])
        myworkdir = self._kwargs.get('myworkdir')
        _scorefile = open('{0}/data/score'.format(myworkdir), 'wb')
        pickle.dump(points, _scorefile)
        _scorefile.close()
        return msg
