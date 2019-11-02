class Message(object):
    """ A message returned from the slack RTM Client

    Attributes:
    admin(bool): User admin status
    banned(bool): User ban status
    channel(str): A channel ID from slack
    commands(str): First command from text, Defaults to empty value
    msg(str): The formatted message to return to the client
    user(str): This is the user who sent the message
    target_users(str): Obtain user ids fortarge users from text

    Methods:
    check_admin: Checks if user is an admin
    check_banned: Checks if the user is banned
    check_bot:
    check_command: Checks for first command in text
    check_message:
    check_user: Checks for users in text
    run_command:
    run_fake_points:

    Note:
    This just creates a message object based on the returned payload from
    slack. I expect overloading the msg attribute will ultimately be the
    correct way to set a value there. I only intend on tageting the first
    command in an individual post.
    """

    def __init__(self, data, **kwargs):
        self._data = data
        self._kwargs = kwargs
        self._list_commands = self._kwargs.get('commands')
        self._text = data.get('text')
        self.user = data.get('user')
        self.msg = ''
        self.admin = self.check_admin()
        self.banned = self.check_banned()
        self.channel = data.get('channel')
        self.target_users = self.check_users()
        self.check_command()
        self.run_command()

    def __str__(self):
        value = "\nUSER:{0}\nTARGETS:{1}\n"
        value += "COMMAND:{2}\nORIGINAL_TEXT:{3}\n"
        value += "MSG:{4}\nADMIN:{5}\nBANNED:{6}"
        format_value = value.format(
                self.user,
                self.target_users,
                self.command,
                self._text,
                self.msg,
                self.admin,
                self.banned)
        return format_value

    def check_admin(self):
        ''' Checks to see if the user is an admin: returns boolean '''
        if self.user in self._kwargs.get('admins'):
            return True
        else:
            return False

    def check_banned(self):
        ''' Checks to see if the user is banned: returns boolean '''
        myworkdir = self._kwargs.get('myworkdir')
        try:
            banned_users = []
            with open('{0}/data/BANNED'.format(myworkdir), 'r') as _banfile:
                for banneduser in _banfile.read().split('\n'):
                    banned_users.append(banneduser)
            if user in banned_users:
                self.msg = "@<{0}> you are banned. "
                self.msg += "Please contact an admin."
                self.msg = self.msg.format(self.user)
                return True
        except:
            return False

    def check_bot(self):
        ''' Checks if the message was sent from the bot user '''
        if self._data.get('bot_id') == self._kwargs.get('botid'):
            self.command = ''
        return

    def check_command(self):
        ''' Grabs the first command from text: intentially only one '''
        if not self._text:
            return
        for value in self._text.split(' '):
            if value in self._list_commands:
                self.command = value
                return
            if value.startswith('-') or value.startswith('+'):
                self.command = ''
                self.msg = self.run_fake_points(value)
        return

    def check_message(self):
        ''' Checks the message type againsts ignore list '''
        ignore_types = ['message_changed',
                        'bot_message',
                        'message_deleted']
        if self._data.get('subtype') in ignore_types:
            self.command = ''
        return

    def check_users(self):
        ''' Grabs all of the user ids from the text: returns list '''
        import re
        target_users = []
        if not self._text:
            return target_users
        reg = re.compile('<@.*>')
        for value in self._text.split(' '):
            if reg.match(value):
                if value in target_users:
                    #  This little gem is to prevent multiple entries for
                    #  a user in the list inspired by Dylan
                    continue
                target_users.append(value.strip('<>@'))
        return target_users

    def run_command(self):
        self.check_bot()
        self.check_message()
        if self.command:
            for _user in self.target_users:
                comargs = dict(user=_user,
                               message=self,
                               workdir=self._kwargs.get('myworkdir'))
                self.msg += self._list_commands.get(self.command)(**comargs)
        return

    def run_fake_points(self, value):
        ''' This method incorporates the FakeInternetPoints class '''
        from fake_points import FakeInternetPoints
        self._fipchange = value
        return FakeInternetPoints(self)
