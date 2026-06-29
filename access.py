"""Authorization helpers for admin and ban checks."""


class AccessControl:
    """Centralized admin and ban policy for command execution."""

    def __init__(self, admins, banned):
        self.admins = set(admins or [])
        self.banned = banned if banned is not None else {}

    def is_admin(self, user_id):
        return user_id in self.admins

    def is_banned(self, user_id):
        return user_id in self.banned

    def ban_message(self):
        return "You are banned. Please contact an admin."

    def admin_denied_message(self, actor_id):
        return "<@{0}>, you are not an admin".format(actor_id)

    def block_if_banned(self, message):
        """Stop command execution for banned users. Returns True if blocked."""
        if not self.is_banned(message.user):
            return False
        message.msg = self.ban_message()
        message.channel = message.user
        message.banned = True
        return True

    def require_admin(self, message):
        """Return an denial message for non-admins, otherwise None."""
        if self.is_admin(message.user):
            return None
        message.channel = message.user
        return self.admin_denied_message(message.user)

    def ban_user(self, user_id):
        if user_id and user_id != "none":
            self.banned[user_id] = True

    def unban_user(self, user_id):
        self.banned.pop(user_id, None)

    def unban_all(self):
        self.banned.clear()
