"""A simple class that constructs a points object."""

from __future__ import annotations

from context import CommandContext, get_context


class FakeInternetPoints:
    """Award or remove fake internet points for a target user."""

    def __init__(self, **comargs):
        ctx = get_context(comargs)
        self.context = ctx
        self.message = comargs.get("message")
        self._command = ctx.fip_change or getattr(self.message, "_fipchange", "")
        self._subjects = ctx.target_users
        self.user = comargs.get("user")
        self.awarder = ctx.actor_id
        self.change = self.process_command(self._command)
        self.msg = self.check_valid_user()

    def check_upper_value(self, change: int) -> int:
        if change < -5:
            return -5
        if change > 5:
            return 5
        return change

    def check_valid_user(self) -> str:
        if self.awarder in self._subjects:
            return "<@{0}> You are not allowed to assign yourself points.".format(self.awarder)
        return self.set_user_points()

    def process_command(self, command: str) -> int:
        change = 0
        count = 0
        for value in command:
            if count == 0:
                count += 1
                continue
            if value == "+":
                change += 1
            if value == "-":
                change -= 1
        return self.check_upper_value(change)

    def set_original_message(self) -> str:
        suffix = "point" if self.change in (1, -1) else "points"
        return "<@{0}> has changed by {1} {2}, now they have {3} in total.\n".format(
            self.user,
            self.change,
            suffix,
            self.context.score[self.user],
        )

    def set_user_points(self) -> str:
        if self.change == 0:
            return ""
        score = self.context.score
        if self.user in score:
            score[self.user] += self.change
        else:
            score[self.user] = self.change
        return self.set_original_message()
