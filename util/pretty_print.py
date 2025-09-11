"""
This module provides pretty print utility functions for SplashtagChecker.
"""

from models.player import Player


def pretty_print_player_list(players: list[str]) -> str:
    """
    Returns a comma-separated string of player names, each wrapped in backticks.

    Args:
        players (list[str]): List of player names (splashtags).

    Returns:
        str: Comma-separated string of player names.
    """
    player_list = ""
    for player in players:
        player_list += f" `{player}`,"  # Add each player name wrapped in backticks
    return player_list[:-1]  # Remove trailing comma


def pretty_print_players(players: list[Player]) -> str:
    """
    Returns a comma-separated string of splashtags from a list of Player objects.

    Args:
        players (list[Player]): List of Player objects.

    Returns:
        str: Comma-separated string of player splashtags.
    """
    return pretty_print_player_list([player.splashtag for player in players])
