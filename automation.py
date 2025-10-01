import os
import sendou
from dotenv import load_dotenv
import gdown

import sys

load_dotenv()

GOOGLE_SAVE_LOCATION = "Testing/g-down-download.csv"
SENDOU_SAVE_LOCATION = "Testing/sendou-download.csv"

TEAM_NAME_BATTLEFY_HEADER = 'teamName'
PLAYER_NAME_BATTLEFY_HEADER = 'inGameName'
PLAYER_DISCORD_BATTLEFY_HEADER  = 'Captain\'s Discord username'

GOOGLE_URL = os.getenv("GOOGLE_SHEET_LINK")
SENDOU_TOKEN = os.getenv("SENDOU_TOKEN")

def download_google_sheet(save_location=GOOGLE_SAVE_LOCATION):
    gdown.download(GOOGLE_URL, save_location)
    return True

async def download_sendou_sheet(ID, save_location=SENDOU_SAVE_LOCATION):
    client = sendou.Client(SENDOU_TOKEN)
    tournament_info = await client.get_tournament(ID)
    teams = await tournament_info.get_teams()

    tournament_teams = [{'team_name': team.name, 'players': [{'id': player.discord_id, 'splashtag': player.in_game_name} for player in team.members], 'link': team.team_page_url if team.team_page_url != None else team.url} for team in teams]

    with open(save_location, "w", encoding='utf8') as write_file:
        first_line = TEAM_NAME_BATTLEFY_HEADER + "," + PLAYER_NAME_BATTLEFY_HEADER + "," + PLAYER_DISCORD_BATTLEFY_HEADER + "\n"

        write_file.write(first_line)

        for info in tournament_teams:
            team = info["team_name"]
            captain_discord = "<@" + info["players"][0]["id"] + ">"

            for player in info["players"]:
                player_splashtag = player["splashtag"].replace("\"", "\"\"")

                line_output = team + ",\"" + player_splashtag + "\"," + captain_discord + "\n"

                print(line_output)
                write_file.write(line_output)
    
    return True