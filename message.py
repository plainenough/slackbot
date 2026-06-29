"""Simple message object."""

import re


class Message(object):
    """Parse a Slack message event and dispatch the first matching command."""

    def __init__(self, data, **kwargs):
        self._data = data
        self._kwargs = kwargs
        self._list_commands = self._kwargs.get("commands", {})
        self._text = self._parse_text()
        self.user = data.get("user")
        self.msg = ""
        self.banned = False
        self.channel = data.get("channel")
        self.target_users = []
        self.command = False
        self._resolve_command()
        self._dispatch()

    def __str__(self):
        value = "\nUSER:{0}\nTARGETS:{1}\n"
        value += "COMMAND:{2}\nORIGINAL_TEXT:{3}\n"
        value += "MSG:{4}\nADMIN:{5}\nBANNED:{6}"
        return value.format(
            self.user,
            self.target_users,
            self.command,
            self._text,
            self.msg,
            self.admin,
            self.banned,
        )

    @property
    def access(self):
        return self._get_access()

    @property
    def admin(self):
        return self.access.is_admin(self.user)

    def _get_access(self):
        access = self._kwargs.get("access")
        if access is None:
            from access import AccessControl

            access = AccessControl(
                self._kwargs.get("admins", []),
                self._kwargs.get("banned", {}),
            )
            self._kwargs["access"] = access
        return access

    def _parse_text(self):
        if self._data.get("text"):
            return self._data.get("text")
        return " "

    def _resolve_command(self):
        for value in self._text.split(" "):
            if str(value) in self._list_commands:
                self.command = self._list_commands.get(value)
                return
            if value.startswith("-") or value.startswith("+"):
                self.command = self._run_fake_points
                self._fipchange = value
                return

    def _should_ignore(self):
        if self._is_bot_message():
            return True
        ignore_types = ["message_changed", "bot_message", "message_deleted"]
        return self._data.get("subtype") in ignore_types

    def _is_bot_message(self):
        bot_id = self._kwargs.get("botid")
        bot_user_id = self._kwargs.get("botuserid")
        if self._data.get("bot_id") and self._data.get("bot_id") == bot_id:
            return True
        if self.user and (self.user == bot_user_id or self.user == bot_id):
            return True
        return False

    def _parse_target_users(self):
        target_users = []
        mention = re.compile("<@.*>")
        for value in self._text.split(" "):
            if not mention.match(value):
                continue
            user_id = value.strip("<>@")
            if user_id in target_users:
                continue
            if user_id == self._kwargs.get("botid"):
                continue
            target_users.append(user_id)
        return target_users

    def _dispatch(self):
        if self._should_ignore():
            self.command = False
            return
        if not self.command:
            return

        self.target_users = self._parse_target_users()
        if self.access.block_if_banned(self):
            self.command = None
            return

        if len(self.target_users) > 1:
            self._run_multiuser_command()
            return
        self._run_singleuser_command()

    def _command_args(self, user=None):
        return {
            "user": user,
            "message": self,
            "workdir": self._kwargs.get("myworkdir"),
        }

    def _run_multiuser_command(self):
        for target_user in self.target_users:
            self.msg += self.command(**self._command_args(user=target_user))

    def _run_singleuser_command(self):
        user = self.target_users[0] if len(self.target_users) == 1 else None
        self.msg = self.command(**self._command_args(user=user))

    def _run_fake_points(self, **comargs):
        from fake_points import FakeInternetPoints

        if len(self.target_users) > 1:
            return ""
        fip = FakeInternetPoints(**comargs)
        self.msg = fip.msg
        return self.msg
