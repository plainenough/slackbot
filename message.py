class Message(object):
    """ A message returned from the slack RTM Client

    Attributes:
    admin(bool): User admin status
    banned(bool): User ban status
    channel(str): A channel ID from slack
    commands(str): First command from text, Defaults to empty value
    text(str): The original un-edited value from the RTM client
    target_users(str): Obtain user ids fortarge users from text
    user(str): A user ID from slack

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

    def __init__(self, **kwargs):
        self._kwargs = kwargs
        self._logger = self._kwargs.logger
        self.admin = self.check_admin()
        self.banned = self.check_banned()
        self.channel = data['channel']
        self.command = self.check_command()
        self.text = self._kwargs.text
        self.target_users = self.check_users()
        self.user = self._kwargs.user

    def __str__(self):
        value = "\nUSER:{0}\nTARGETS:{1}\n"
        value += "COMMAND:{2}\nORIGINAL_TEXT:{3}\n"
        value += "ADMIN:{4}\nBANNED:{5}\n"
        format_value = value.format(
                self.user,
                self.target_users,
                self.command,
                self.text,
                self.admin,
                self.banned)
        return format_value

    def check_admin(self):
        ''' Checks to see if the user is an admin: returns boolean '''
        logging = self._kwargs.logging
        user = self._kwargs.user
        if user in self._kwargs.ADMINS:
            logging.debug('{0} is an admin'.format(user))
            return True
        else:
            logging.debug('{0} is not an admin'.format(user))
            return False

    def check_banned(self):
        ''' Checks to see if the user is banned: returns boolean '''
        logging = self._kwargs.logging
        myworkdir = self._kwargs.myworkdir
        user = self._kwargs.user
        try:
            banned_users = []
            with open('{0}/data/BANNED'.format(myworkdir), 'r') as _banfile:
                for banneduser in _banfile.read().split('\n'):
                    banned_users.append(banneduser)
            if user in banned_users:
                logging.info("{0} is banned".format(user))
                return True
        except Exception as e:
            logging.info("Banned file doesn't exist")
            logging.debug(e)
        return False

    def check_command(self):
        ''' Grabs the first command from text: intentially only one '''
        command = ''
        commands = self._kwargs.commands
        logging = self._kwargs.logging
        text = self._kwargs.text
        if text == '':
            return command
        for value in text.split(' '):
            if value in commands:
                command = value
            if value.startswith('-') or value.startswith('+'):
                logging.info('Detected fake_points event')
                command = {'fake_points': value}
        return command

    def check_users(self, text):
        ''' Grabs all of the user ids from the text: returns list '''
        import re
        target_users = []
        text = self._kwargs.text
        reg = re.compile('<@.*>')
        for value in text.split(' '):
            if reg.match(value):
                if value in target_users:
                    #  This little gem is to prevent multiple entries for
                    #  a user in the list inspired by Dylan
                    continue
                target_users.append(value.strip('<>@'))
        return target_users
