"""Test scoreboard formatting."""

from scoreboard import format_leaderboard, load_snapshot, save_snapshot


def test_format_leaderboard_with_medals():
    text = format_leaderboard({"U1": 10, "U2": 5}, {})
    assert "🥇" in text
    assert "🥈" in text


def test_format_leaderboard_with_delta(tmp_path):
    previous = {"U1": 8, "U2": 5}
    text = format_leaderboard({"U1": 10, "U2": 3}, previous)
    assert "+2 since last scoreboard" in text
    assert "-2 since last scoreboard" in text


def test_snapshot_roundtrip(tmp_path):
    save_snapshot(str(tmp_path), {"U1": 4})
    assert load_snapshot(str(tmp_path)) == {"U1": 4}
