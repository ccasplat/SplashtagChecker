from typing import Final

# Maximum allowed difference in seconds between the modification times of the two files
MAX_THRESHOLD_FILE_DIFF_SEC: Final = 5 * 60  # 5 minutes

# Regular expression for validating Splashtags (in-game name format)
SPLASHTAG_REGEX: Final = r"^[^\x00-\x1F]{1,10}#\d{4,5}$"

# Maximum number of players allowed per team
MAX_PLAYERS_PER_TEAM: Final = 8
