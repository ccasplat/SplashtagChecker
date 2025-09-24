import argparse

import arrow

from models.validator import Validator
from util.pretty_print import pretty_print_players, pretty_print_player_list
from discord_timestamps import format_timestamp, TimestampType

from automation import *
import asyncio


# Use the below if you want to run the script w/o using command line arguments
battlefy_csv_filename = "Testing/sendou-download.csv"
gform_csv_filename = "Testing/g-down-download.csv"

async def runner():
    """
    Runs the validation checks and prints results for splashtag errors and missing registrations.
    """
    
    download_google_sheet()
    await download_sendou_sheet(ID=2536)
    
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
            print(f"- {team}: {team_captain_discord} |{bad_splashtags}")

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
            print(f"- {team_name}: {validation.battlefy_teams[team_name].captain.discord}")

            if len(only_in_battlefy) > 0:
                print(f"  - Players only on sendou.ink:{only_in_battlefy}")
            if len(only_in_gform) > 0:
                print(f"  - Players only on Google Form:{only_in_gform}")


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
