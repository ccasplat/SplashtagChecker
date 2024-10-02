import re
from collections import defaultdict

from models.team import TeamDiff
from util.parse_csv import parse_gform_csv, parse_battlefy_csv, SPLASHTAG_REGEX
from util.file_checks import check_csv_files_exist, check_csv_files_datetime


class Validator:
    def __init__(self, battlefy_filename: str, gform_filename: str):
        check_csv_files_exist(battlefy_filename, gform_filename)
        check_csv_files_datetime(battlefy_filename, gform_filename)

        self.battlefy_teams = parse_battlefy_csv(battlefy_filename)
        self.gform_teams = parse_gform_csv(gform_filename)

    def get_missing_splashtags_from_battlefy(self):
        bad_splashtags_by_team = defaultdict(list)

        for team in self.battlefy_teams.values():
            for player in team.players:
                if not re.match(SPLASHTAG_REGEX, player.splashtag):
                    if team.name not in bad_splashtags_by_team:
                        bad_splashtags_by_team[team.name] = [player]
                    else:
                        bad_splashtags_by_team[team.name].append(player)

        return bad_splashtags_by_team

    def get_bad_team_names(self):
        combined_teams = []

        battlefy_teams_list = [team.name for team in self.battlefy_teams.values()]
        gform_teams_list = [team.name for team in self.gform_teams.values()]

        # team found in gform but not in battlefy
        for gform_team in self.gform_teams:
            if gform_team not in battlefy_teams_list:
                combined_teams.append(
                    TeamDiff(gform=self.gform_teams[gform_team]))

        # team found in battlefy but not on gform
        for battlefy_team in self.battlefy_teams:
            if battlefy_team not in gform_teams_list:
                combined_teams.append(
                    TeamDiff(battlefy=self.battlefy_teams[battlefy_team]))

        return combined_teams

    def get_splashtag_conflicts(self):
        player_comparison = {}

        for battlefy_team_name, battlefy_team_obj in self.battlefy_teams.items():
            if battlefy_team_name in self.gform_teams:
                gform_players = self.gform_teams[battlefy_team_name]

                battlefy_player_splashtags = {player.splashtag.strip().replace(" #", "#") for player in
                                              battlefy_team_obj.players}
                gform_player_splashtags = {player.splashtag.strip().replace(" #", "#") for player in
                                           gform_players.players}

                only_in_battlefy = battlefy_player_splashtags - gform_player_splashtags
                only_in_gform = gform_player_splashtags - battlefy_player_splashtags

                if only_in_battlefy or only_in_gform:
                    player_comparison[battlefy_team_name] = TeamDiff(battlefy=only_in_battlefy, gform=only_in_gform)

        return player_comparison

    def get_teams_not_on_battlefy(self):
        return [td for td in self.get_bad_team_names() if td.battlefy is None]

    def get_teams_not_on_gform(self):
        return [td for td in self.get_bad_team_names() if td.gform is None]
