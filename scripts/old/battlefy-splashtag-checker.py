import csv
import re
from collections import defaultdict
from dataclasses import dataclass

csv_file_name = "/path/to/battlefy.csv"

splashtag_regex = r"^[^\x00-\x1F]{1,15}#\d{4,5}$"


@dataclass
class Team:
    name: str
    team_captain_discord: str
    bad_splashtags: list[str]


bad_splashtags_by_team = defaultdict(list)
# bad_splashtags_by_team[str] -> Team
# input: team name (str), output: Team class

with open(csv_file_name, mode='r', newline='') as file:
    reader = csv.DictReader(file)

    for row in reader:
        team_name = row['teamName']
        player_name = row['inGameName']
        captain_discord_username = row[
            'Discord Username of team captain (all lowercase, please do not include the @ symbol)']

        if not re.match(splashtag_regex, player_name):
            if team_name not in bad_splashtags_by_team:
                bad_splashtag_obj = Team(team_name, captain_discord_username, [player_name])
                bad_splashtags_by_team[team_name] = bad_splashtag_obj
            else:
                bad_splashtags_by_team[team_name].bad_splashtags.append(player_name)

sorted_team_names = sorted(bad_splashtags_by_team.keys())

for team in sorted_team_names:
    bad_splashtags = ""
    for player in bad_splashtags_by_team[team].bad_splashtags:
        bad_splashtags += f" `{player}`,"

    print(f"- {team}: @{bad_splashtags_by_team[team].team_captain_discord} |{bad_splashtags[:-1]}")
