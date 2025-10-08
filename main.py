import argparse

import arrow
import json

from models.validator import Validator
from util.pretty_print import pretty_print_players, pretty_print_player_list
from discord_timestamps import format_timestamp, TimestampType

from automation import *
import asyncio

C2_Qualifiers = json.load(open("C2-QIDs.json"))

Qualifier = "Q3"

battlefy_csv_filename = "Testing/sendou-download.csv"
gform_csv_filename = "Testing/g-down-download.csv"

async def runner():
    """
    Runs the validation checks and prints results for splashtag errors and missing registrations.
    """
    
    download_google_sheet()
    await download_sendou_sheet(ID=C2_Qualifiers[Qualifier]["ID"])
    
    # Print the timestamp of when the script was run
    print("*The below message was generated on", format_timestamp(arrow.utcnow(), TimestampType.LONG_DATETIME),
          "via an automatic script*")

    # Create a Validator instance with the provided CSV filenames
    validation = Validator(battlefy_csv_filename, gform_csv_filename)

    print("\n## Splashtag Errors on sendou.ink")

    # Get teams with missing or invalid splashtags from Battlefy
    missing_splashtag_result = validation.get_missing_splashtags_from_battlefy()

    # If no errors, print success message
    if len(missing_splashtag_result.keys()) == 0:
        print("No Splashtag errors found. Good job everyone!")
    else:
        print("The below teams have improperly formatted Splashtags on sendou.ink:")

        # Sort team names alphabetically for output
        sorted_team_names = sorted(missing_splashtag_result.keys())

        for team in sorted_team_names:
            # Format the list of bad splashtags for this team
            bad_splashtags = pretty_print_players(missing_splashtag_result[team])
            # Get the Discord username of the team captain
            team_captain_discord = validation.battlefy_teams[team].captain.discord

            # second contact string - untested since there are no teams with this issue aws of 10/7 - cyanne
            gform_team = validation.gform_teams[team]
            second_contact_string = ", @" + gform_team.second_contact + " " if gform_team.second_contact else ""
            print(f"- {team}: {team_captain_discord}{second_contact_string} |{bad_splashtags}")

        print("\n`Splashtag Errors on sendou.ink`")
        print("- **If your team in this section, this means there are player(s) that do not have a valid Splashtag on sendou.ink.**")
        print("- We do require the full Splashtag, including the pound sign and the 4 or 5 digit number afterwards. For example, `VeronIKA#1234` is a valid Splashtag. `VeronIKA` is not acceptable. Please confirm that the splashtag are valid using the [CCA's Splatoon 3 Splashtag Character Checker](https://docs.google.com/spreadsheets/u/0/d/19zMKlFB3kGDASFhCbDimNpBQQupUM6SWBLTqAJhJtRU/htmlview#gid=0) before updating on sendou.ink")

    print("\n## Teams that have not registered via Google form")

    # Get teams that are on Battlefy but not registered via Google Form
    teams_not_on_gform = validation.get_teams_not_on_gform()

    # If no missing registrations, print success message
    if len(teams_not_on_gform) == 0:
        print("No missing Google Form Registrations. Good job everyone!")
    else:
        print("The below teams registered on sendou.ink but did not register via Google Form:")

        for team_diff in teams_not_on_gform:
           #  print(team_diff)
            # team_name = team_diff.battlefy.name
            team_name = team_diff
            team_captain_discord = validation.battlefy_teams[team_name].captain.discord
            print(f"- `{team_name}`: {team_captain_discord}")

        print("\n`Teams that have not registered via Google form`")
        print("- **If your team in this section, this means that you have not registered your team using the Google form or that there is difference betwen team name on sendou.ink and the one used in the google form.**")
        print("- All teams are required to fill out the CCA Circuit Google Registration; please double check the [CCA Circuit Season 2 Google Registered Teams](https://docs.google.com/spreadsheets/d/e/2PACX-1vS9FofFA3esOId-Cj2fq4-TdEGq2PJ63awf60B8zAe_XG_nm5a6h65Uq6R0q9Y88DL5X7RsaxXbxWJO/pubhtml?gid=384553618&single=true) to ensure that your team is listed there. If not, please submit a response to the [CCA Circuit Season 2 Registration](https://docs.google.com/forms/d/e/1FAIpQLSfkRzCe_dDSrH7acfxTP71-oOCvc7jg5Oe0wAX2FioGkywyKA/viewform) in full.")

    print("\n## Splashtag Cross Check")

    # Check for splashtag conflicts between Battlefy and Google Form registrations
    splashtag_conflicts = validation.get_splashtag_conflicts()

    # If no conflicts, print success message
    if len(splashtag_conflicts) == 0:
        print("No Splashtag conflicts. Good job everyone!")
    else:
        print("The below teams have players with splashtags that are different across sendou.ink and Google Form "
              "registrations:")

        for team_name, player_diff in splashtag_conflicts.items():
            only_in_battlefy = pretty_print_player_list(list(player_diff.battlefy))
            only_in_gform = pretty_print_player_list(list(player_diff.gform))

            gform_team = validation.gform_teams[team_name]
            second_contact_string = ", @" + gform_team.second_contact + " " if gform_team.second_contact else ""
            print(f"- {team_name}: {validation.battlefy_teams[team_name].captain.discord}{second_contact_string}")

            if len(only_in_battlefy) > 0:
                print(f"  - Players only on sendou.ink:{only_in_battlefy}")
            if len(only_in_gform) > 0:
                print(f"  - Players only on Google Form:{only_in_gform}")

        print("\n`Splashtag Cross Check`")
        print("- **If your team in this section, this means that there are players that are not on sendou.ink or part of your roster originally submitted during Google Registration.**")
        print("- Player(s) may be in this section if their Splashtag are different between registrations. If a Splashtag change needs to be made, please confirm that the splashtag are valid using the [CCA's Splatoon 3 Splashtag Character Checker](https://docs.google.com/spreadsheets/u/0/d/19zMKlFB3kGDASFhCbDimNpBQQupUM6SWBLTqAJhJtRU/htmlview#gid=0) and then submit a response to the [CCA Circuit Season 2 | Roster Changes & Splashtag Updates](https://forms.gle/gYj82DCasMMjtJNe7) so it can be updated.")
        print("- Sendou.ink only support teams up to 6, therefore, any 7th or 8th players needs to be manually added by CCA staff. To have this done, please to go #circuit-helpdesk stating your team name and the links to their sendou.ink pages")

    print("\n**Please note that all registration issues must be resolved by " + C2_Qualifiers[Qualifier]["Timestamp"] + ". Any players with missing or incorrect Splashtags after this date will be dropped and cannot play in " + C2_Qualifiers[Qualifier]["Tag"] + ". Any teams with less than 4 players or teams that have not registered via Google form will also be dropped.  __This deadline cannot be extended for any reason.__ You will be unable to update player names after " + C2_Qualifiers[Qualifier]["Timestamp"] + "! Please read the ruleset found in #circuit-info for more information.**")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='SplashtagChecker',
        description='Checks Splashtags given two csvs from Google Forms and Battlefy',
        epilog='Written by dama for the CCA, hi Frosty!')

    parser.add_argument('-b', '--battlefy-filename', help='File path to Battlefy\'s csv export')
    parser.add_argument('-g', '--gform-filename', help='File path to Google Form\'s csv export')
    args = parser.parse_args()

    if args.battlefy_filename is not None:
        battlefy_csv_filename = args.battlefy_filename
    if args.gform_filename is not None:
        gform_csv_filename = args.gform_filename


asyncio.run(runner())
