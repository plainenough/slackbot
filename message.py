class Message(object):
    """ A message returned from the slack RTM Client

    Attributes:
    admin(bool): User admin status
    banned(bool): User ban status
    channel(str): A channel ID from slack
    commands(str): First command from text, Defaults to empty value
    target_users(str): Obtain user ids fortarge users from text

    Methods:
    check_admin: Checks if user is an admin
    check_banned: Checks if the user is banned
    check_command: Checks for first command in text
    check_user: Checks for users in text

    Note:
    This just creates a message object based on the returned payload from
    slack. I expect overloading the msg attribute will ultimately be the
    correct way to set a value there. I only intend on tageting the first
    command in an individual post.
    """

    def __init__(self, data, **kwargs):
        self._kwargs = kwargs
        self._list_commands = self._kwargs.get('commands')
        self._text = data.get('text')
        self._user = data.get('user')
        self.admin = self.check_admin()
        self.banned = self.check_banned()
        self.channel = data.get('channel')
        self.command = self.check_command()
        self.target_users = self.check_users()

    def __str__(self):
        value = "\nUSER:{0}\nTARGETS:{1}\n"
        value += "COMMAND:{2}\nORIGINAL_TEXT:{3}\n"
        value += "ADMIN:{4}\nBANNED:{5}\n"
        format_value = value.format(
                self._user,
                self.target_users,
                self.command,
                self._text,
                self.admin,
                self.banned)
        return format_value

    def check_admin(self):
        ''' Checks to see if the user is an admin: returns boolean '''
        user = self._user
        if user in self._kwargs.get('admins'):
            return True
        else:
            return False

    def check_banned(self):
        ''' Checks to see if the user is banned: returns boolean '''
        myworkdir = self._kwargs.get('myworkdir')
        user = self._user
        try:
            banned_users = []
            with open('{0}/data/BANNED'.format(myworkdir), 'r') as _banfile:
                for banneduser in _banfile.read().split('\n'):
                    banned_users.append(banneduser)
            if user in banned_users:
                return True
        except Exception as e:
            print("message.py:68")
            exit(1)
        return False

    def check_command(self):
        ''' Grabs the first command from text: intentially only one '''
        command = ''
        myworkdir = self._kwargs.get('myworkdir')
        commands = self._list_commands
        text = self._text
        if text == '':
            return command
        for value in text.split(' '):
            if value in commands:
                command = value
            if value.startswith('-') or value.startswith('+'):
                command = {'fake_points': value}
        return command

    def check_users(self):
        ''' Grabs all of the user ids from the text: returns list '''
        import re
        target_users = []
        text = self._text
        reg = re.compile('<@.*>')
        for value in text.split(' '):
            if reg.match(value):
                if value in target_users:
                    #  This little gem is to prevent multiple entries for
                    #  a user in the list inspired by Dylan
                    continue
                target_users.append(value.strip('<>@'))
        return target_users
