"""Simple message object."""


class Message(object):
    """A message returned from the slack RTM Client.

    Attributes:
    admin(bool): User admin status
    banned(bool): User ban status
    channel(str): A channel ID from slack
    commands(str): First command from text, Defaults to empty value
    msg(str): The formatted message to return to the client
    user(str): This is the user who sent the message
    target_users(list): Obtain user ids for target users from text

    Methods:
    check_admin: Checks if user is an admin
    check_banned: Checks if the user is banned
    check_bot: Checks to see if the bot user sent the message
    check_command: Checks for first command in text
    check_message: Check for blackisted message types
    check_text: Check original message for text
    check_users: Checks for users in text
    run_command: Executes the command based on text input
    run_multiuser_command: Executes the command for multiple users
    run_singleuser_command: Executes a command for 1 or less users
    run_fake_points: Executes fakepoint class

    Note:
    This just creates a message object based on the returned payload from
    slack. I expect overloading the msg attribute will ultimately be the
    correct way to set a value there. I only intend on tageting the first
    command in an individual post.
    """

    def __init__(self, data, **kwargs):
        """Message initilization."""
        self._data = data
        self._kwargs = kwargs
        self._list_commands = self._kwargs.get('commands')
        self._text = self.check_text()
        self.user = data.get('user')
        self.msg = ''
        self.admin = self.check_admin()
        self.banned = False
        self.channel = data.get('channel')
        self.target_users = []
        self.check_command()
        self.run_command()

    def __str__(self):
        """Return a printout of the object."""
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
        """Check to see if the user is an admin: returns boolean."""
        if self.user in self._kwargs.get('admins'):
            return True
        else:
            return False

    def check_banned(self):
        """Check to see if the user is banned: returns boolean."""
        banned = self._kwargs.get('banned')
        if self.user in banned:
            _msg = "You are banned. "
            _msg += "Please contact an admin."
            self.msg = _msg
            self.channel = self.user
            self.banned = True
        return

    def check_bot(self):
        """Check if the message was sent from the bot user."""
        if self._data.get('bot_id'):
            if self._data.get('bot_id') == self._kwargs.get('botid'):
                self.command = False
        elif self.user == self._kwargs.get('botid'):
            self.command = False
        return

    def check_command(self):
        """Grab the first command from text: intentially only one."""
        self.command = False
        for value in self._text.split(' '):
            if str(value) in self._list_commands:
                self.command = self._list_commands.get(value)
                return
            elif value.startswith('-') or value.startswith('+'):
                self.command = self.run_fake_points
                self._fipchange = value
        return

    def check_message(self):
        """Check the message type againsts ignore list."""
        ignore_types = ['message_changed',
                        'bot_message',
                        'message_deleted']
        if self._data.get('subtype') in ignore_types:
            self.command = False
        return

    def check_text(self):
        """Set _text value."""
        if self._data.get('text'):
            return self._data.get('text')
        else:
            return ' '

    def check_users(self):
        """Grab all of the user ids from the text: returns list."""
        import re
        target_users = []
        reg = re.compile('\<@.*\>')
        for value in self._text.split(' '):
            if reg.match(value):
                if value.strip('<>@') in target_users:
                    #  This little gem is to prevent multiple entries for
                    #  a user in the list inspired by Dylan
                    continue
                elif value.strip('<>@') == self._kwargs.get('botid'):
                    continue
                target_users.append(value.strip('<>@'))
        return target_users

    def run_command(self):
        """Run a single command targeted at a single user."""
        self.check_bot()
        self.check_message()
        self.target_users = self.check_users()
        if self.command:
            if len(self.target_users) > 1:
                self.run_multiuser_command()
                return
            else:
                self.run_singleuser_command()
                return

    def run_multiuser_command(self):
        """Run a single command targeted at multiple users."""
        self.check_banned()
        if self.banned is True:
            self.command = None
            return
        for _user in self.target_users:
            comargs = dict(user=_user,
                           message=self,
                           workdir=self._kwargs.get('myworkdir'))
            self.msg += self.command(**comargs)
        return

    def run_singleuser_command(self):
        """Run a single command targeted at a single user."""
        self.check_banned()
        if self.banned is True:
            self.command = None
            return
        user = 'none'
        if len(self.target_users) == 1:
            user = self.target_users[0]
        comargs = dict(user=user,
                       message=self,
                       workdir=self._kwargs.get('myworkdir'))
        self.msg = self.command(**comargs)
        return

    def run_fake_points(self, **comargs):
        """Run FakeInternetPoints class."""
        from fake_points import FakeInternetPoints
        self.check_banned()
        if self.banned is True:
            return self.msg
        if self.target_users.len() > 1:
          return
        fip = FakeInternetPoints(**comargs)
        self.msg = fip.msg
        return self.msg
