import os
import datetime
from typing import Final
import warnings

MAX_THRESHOLD_FILE_DIFF_SEC: Final = 5 * 60  # 5 minutes


def check_csv_files_exist(battlefy_filename: str, gform_filename: str):
    if not os.path.isfile(battlefy_filename):
        raise FileNotFoundError(f"Battlefy csv file `{battlefy_filename}` not found")
    if not os.path.isfile(gform_filename):
        raise FileNotFoundError(f"Google form csv file `{gform_filename}` not found")


def check_csv_files_datetime(battlefy_filename: str, gform_filename: str):
    battlefy_mod_date = os.path.getmtime(battlefy_filename)
    gform_mod_date = os.path.getmtime(gform_filename)

    battlefy_mod_date_datetime = datetime.datetime.fromtimestamp(battlefy_mod_date)
    gform_mod_date_datetime = datetime.datetime.fromtimestamp(gform_mod_date)

    date_diff = battlefy_mod_date_datetime - gform_mod_date_datetime

    if abs(date_diff.total_seconds()) > MAX_THRESHOLD_FILE_DIFF_SEC:
        warning_str = f"Files `{battlefy_filename}` and `{gform_filename}` have an age difference of {date_diff}, " \
                      f"more than {MAX_THRESHOLD_FILE_DIFF_SEC} seconds"
        warnings.warn(warning_str, RuntimeWarning)
