"""
Validator class for SplashtagChecker.
Provides methods to validate team and player data from Google Forms and Battlefy CSV exports.
"""

import re
from collections import defaultdict
from typing import Dict, List

from models.team import TeamDiff, Team
from util.parse_csv import parse_gform_csv, parse_battlefy_csv
from config.settings import SPLASHTAG_REGEX
from util.file_checks import check_csv_files_exist, check_csv_files_datetime
from models.player import Player


class Validator:
    """
    Provides validation methods for SplashtagChecker team and player data.
    Methods:
        __init__: Loads and checks CSV files, parses teams.
        get_missing_splashtags_from_battlefy: Finds players with invalid splashtags in Battlefy data.
        get_bad_team_names: Finds teams present in one source but not the other.
        get_splashtag_conflicts: Placeholder for future splashtag conflict detection.
        get_teams_not_on_battlefy: Finds teams missing from Battlefy.
        get_teams_not_on_gform: Finds teams missing from Google Forms.
    """

    def __init__(self, battlefy_filename: str, gform_filename: str):
        """
        Initializes the Validator by loading teams from Battlefy and Google Forms CSV files.
        Checks file existence and modification times before parsing.
        Args:
            battlefy_filename (str): Path to the Battlefy CSV file.
            gform_filename (str): Path to the Google Forms CSV file.
        """
        check_csv_files_exist(battlefy_filename, gform_filename)
        check_csv_files_datetime(battlefy_filename, gform_filename)

        self.battlefy_teams: Dict[str, Team] = parse_battlefy_csv(battlefy_filename)
        self.gform_teams: Dict[str, Team] = parse_gform_csv(gform_filename)

    def get_missing_splashtags_from_battlefy(self) -> Dict[str, List[Player]]:
        """
        Returns a dictionary mapping team names to lists of players with invalid splashtags in Battlefy data.
        Returns:
            Dict[str, List[Player]]: Team names mapped to lists of invalid Player objects.
        """
        bad_splashtags_by_team: Dict[str, List[Player]] = defaultdict(list)

        for team in self.battlefy_teams.values():
            for player in team.players:
                if not re.match(SPLASHTAG_REGEX, player.splashtag):
                    bad_splashtags_by_team[team.name].append(player)

        return bad_splashtags_by_team

    def get_splashtag_conflicts(self):
        player_comparison = {}

        for battlefy_team_name, battlefy_team_obj in self.battlefy_teams.items():
            if battlefy_team_name in self.gform_teams:
                gform_players = self.gform_teams[battlefy_team_name]

                battlefy_player_splashtags = {player.splashtag for player in battlefy_team_obj.players}
                gform_player_splashtags = {player.splashtag for player in gform_players.players}

                only_in_battlefy = battlefy_player_splashtags - gform_player_splashtags
                only_in_gform = gform_player_splashtags - battlefy_player_splashtags

                if only_in_battlefy or only_in_gform:
                    player_comparison[battlefy_team_name] = TeamDiff(battlefy=only_in_battlefy, gform=only_in_gform)

        return player_comparison

    def get_bad_team_names(self) -> List[TeamDiff]:
        """
        Returns a list of TeamDiff objects for teams found in one source but not the other.
        Returns:
            List[TeamDiff]: List of TeamDiff objects for mismatched teams.
        """
        combined_teams: List[TeamDiff] = []

        battlefy_teams_list = [team.name for team in self.battlefy_teams.values()]
        gform_teams_list = [team.name for team in self.gform_teams.values()]

        # Teams found in Google Forms but not in Battlefy
        for gform_team in self.gform_teams:
            if gform_team not in battlefy_teams_list:
                combined_teams.append(TeamDiff(gform=self.gform_teams[gform_team]))

        # Teams found in Battlefy but not in Google Forms
        for battlefy_team in self.battlefy_teams:
            if battlefy_team not in gform_teams_list:
                combined_teams.append(TeamDiff(battlefy=self.battlefy_teams[battlefy_team]))

        return combined_teams

    def get_teams_not_on_gform(self) -> List[str]:
        """
        Returns a list of team names that are present in Battlefy but missing from Google Form registration.
        """
        battlefy_team_names = set(self.battlefy_teams.keys())
        gform_team_names = set(self.gform_teams.keys())
        missing_teams = list(battlefy_team_names - gform_team_names)
        return missing_teams
