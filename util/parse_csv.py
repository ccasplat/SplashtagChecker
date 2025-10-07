"""
This module provides functions to parse CSV files exported from Google Forms and Battlefy.
It converts CSV rows into Team and Player objects for further processing.
"""

import csv
from typing import Dict

# Import headers and models using absolute imports for package structure
from config import headers
from config.settings import MAX_PLAYERS_PER_TEAM
from models.data_source import DataSource
from models.player import Player
from models.team import Team


def parse_gform_csv(gform_csv_filename: str) -> Dict[str, Team]:
    """
    Parses a Google Forms CSV export and returns a dictionary of team name to Team objects.
    Each team contains a list of Player objects and a captain.

    Args:
        gform_csv_filename (str): Path to the Google Forms CSV file.

    Returns:
        Dict[str, Team]: Dictionary mapping team names to Team objects.
    """
    teams_list = []

    # Open the Google Forms CSV file for reading
    with open(gform_csv_filename, mode='r', newline='', encoding='utf8') as file:
        reader = csv.DictReader(file)

        # Iterate over each row (team registration)
        for row in reader:
            # Create a Team object for each row
            team = Team(name=row[headers.TEAM_NAME_GFORM_HEADER],
                        source=DataSource.GOOGLE_REGISTRATION,
                        second_contact=(row[headers.TEAM_SECOND_CONTACT_GFORM_HEADER]
                                        if row[headers.TEAM_SECOND_CONTACT_GFORM_HEADER]
                                        else None))

            # Add up to MAX_PLAYERS_PER_TEAM players to the team
            for i in range(MAX_PLAYERS_PER_TEAM):
                column_player_num = i + 1
                player_name_key = headers.PLAYER_NAME_GFORM_HEADER.format(column_player_num)
                player_discord_key = headers.PLAYER_DISCORD_GFORM_HEADER.format(column_player_num)
                player_name = row[player_name_key] if player_name_key in row else ""
                player_discord = row[player_discord_key] if player_discord_key in row else ""

                # Stop adding players if both name and discord are empty
                if player_name == "" and player_discord == "":
                    break

                # Create a Player object and add to the team
                player = Player(player_name, player_discord, DataSource.GOOGLE_REGISTRATION)
                team.players.append(player)

            # Assign the first player as the team captain if any players exist
            if team.players:
                team.captain = team.players[0]  # First player is captain

            teams_list.append(team)
            print(team)

    # Return a dictionary mapping team names to Team objects
    return {team.name: team for team in teams_list}


def parse_battlefy_csv(battlefy_csv_filename: str) -> Dict[str, Team]:
    """
    Parses a Battlefy CSV export and returns a dictionary of team name to Team objects.
    Each team contains a list of Player objects and a captain (discord only).

    Args:
        battlefy_csv_filename (str): Path to the Battlefy CSV file.

    Returns:
        Dict[str, Team]: Dictionary mapping team names to Team objects.
    """
    team_dict: Dict[str, Team] = {}

    # Open the Battlefy CSV file for reading
    with open(battlefy_csv_filename, mode='r', newline='', encoding='utf8') as file:
        reader = csv.DictReader(file)

        # Iterate over each row (player registration)
        for row in reader:
            team_name = row[headers.TEAM_NAME_BATTLEFY_HEADER]
            player_splashtag = row[headers.PLAYER_NAME_BATTLEFY_HEADER]
            captain_discord = row[headers.PLAYER_DISCORD_BATTLEFY_HEADER]

            # Create Player object for each row
            player = Player(splashtag=player_splashtag, source=DataSource.BATTLEFY)

            # If team not yet in dictionary, create new Team with captain
            if team_name not in team_dict:
                team_captain = Player(discord=captain_discord, source=DataSource.BATTLEFY)
                team_dict[team_name] = Team(name=team_name, captain=team_captain, players=[player], source=DataSource.BATTLEFY)
            else:
                # Otherwise, add player to existing team
                team_dict[team_name].players.append(player)

    # Return dictionary mapping team names to Team objects
    return team_dict
