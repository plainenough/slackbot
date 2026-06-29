"""Fakeinternet ultilities."""

from audit import record
from context import get_context
from scoreboard import format_leaderboard, load_snapshot, save_snapshot


def alias():
    """Define separate commands and map them to functions."""
    return {
        "mypoints": my_points,
        "scoreboard": all_points,
        "deleteScore": del_points,
        "resetScores": reset_points,
    }


def my_points(**kwargs):
    """Get user FakeInternetPoints count for user."""
    ctx = get_context(kwargs)
    user = ctx.actor_id
    score = ctx.score
    if user in score:
        return "<@{0}> has {1} points".format(user, score[user])
    return "<@{0}> doesn't have points".format(user)


def all_points(**kwargs):
    """Get a sorted list of fakeinternetpoints for team; requires admin."""
    ctx = get_context(kwargs)
    denied = ctx.access.require_admin(ctx)
    if denied:
        return denied
    previous = load_snapshot(ctx.workdir)
    message = format_leaderboard(ctx.score, previous)
    save_snapshot(ctx.workdir, ctx.score)
    record(ctx.workdir, ctx.actor_id, "scoreboard")
    return message


def reset_points(**kwargs):
    """Reset scoreboard for entire team; requires admin."""
    ctx = get_context(kwargs)
    denied = ctx.access.require_admin(ctx)
    if denied:
        return denied
    ctx.score.clear()
    save_snapshot(ctx.workdir, ctx.score)
    record(ctx.workdir, ctx.actor_id, "reset_scores")
    return "All scores have been reset"


def del_points(**kwargs):
    """Delete all points record for a user; requires admin."""
    ctx = get_context(kwargs)
    user = kwargs.get("user")
    denied = ctx.access.require_admin(ctx)
    if denied:
        return denied
    if user in ctx.score:
        del ctx.score[user]
    record(ctx.workdir, ctx.actor_id, "delete_score", target=user)
    return "<@{0}> has been removed from the scoreboard".format(user)
