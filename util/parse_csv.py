import csv
from collections import defaultdict
from typing import Final

from models.data_source import DataSource
from models.player import Player
from models.team import Team

SPLASHTAG_REGEX: Final = r"^[^\x00-\x1F]{1,15}#\d{4,5}$"

TEAM_NAME_GFORM_HEADER: Final = 'Team Name'
PLAYER_NAME_GFORM_HEADER: Final = 'Player {}\'s Splashtag'
PLAYER_DISCORD_GFORM_HEADER: Final = 'Player {}\'s Discord Username'

TEAM_NAME_BATTLEFY_HEADER: Final = 'teamName'
PLAYER_NAME_BATTLEFY_HEADER: Final = 'inGameName'
PLAYER_DISCORD_BATTLEFY_HEADER: Final = 'Captain\'s Discord username'

MAX_PLAYERS_PER_TEAM: Final = 8


def parse_gform_csv(gform_csv_filename: str):
    teams_list = []

    with open(gform_csv_filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)

        for row in reader:
            team = Team(name=row[TEAM_NAME_GFORM_HEADER], source=DataSource.GOOGLE_REGISTRATION)

            for i in range(0, MAX_PLAYERS_PER_TEAM):
                column_player_num = i + 1
                player_name = row[PLAYER_NAME_GFORM_HEADER.format(column_player_num)]
                player_discord = row[PLAYER_DISCORD_GFORM_HEADER.format(column_player_num)]

                # end loop if no more players are found
                if player_name == "" and player_discord == "":
                    break

                player = Player(player_name, player_discord, DataSource.GOOGLE_REGISTRATION)
                team.players.append(player)

            team.captain = team.players[0]  # team captain will always be the 1st player on the roster
            teams_list.append(team)
    return {team.name: team for team in teams_list}


def parse_battlefy_csv(battlefy_csv_filename: str):
    team_dict = defaultdict(Team)
    with open(battlefy_csv_filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)

        for row in reader:
            team_name = row[TEAM_NAME_BATTLEFY_HEADER]
            player_splashtag = row[PLAYER_NAME_BATTLEFY_HEADER]
            captain_discord = row[PLAYER_DISCORD_BATTLEFY_HEADER]

            # Note that we don't know the player's discord nor do we know the
            # captain's splashtag from looking at only battlefy's export
            player = Player(splashtag=player_splashtag, source=DataSource.BATTLEFY)

            if team_name not in team_dict:
                team_captain = Player(discord=captain_discord, source=DataSource.BATTLEFY)

                team_dict[team_name] = Team(name=team_name, captain=team_captain, players=[player],
                                            source=DataSource.BATTLEFY)
            else:
                team_dict[team_name].players.append(player)
    return team_dict

