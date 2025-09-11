"""
This module provides utility functions for checking CSV file existence and modification times for SplashtagChecker.
"""

import os
import datetime
import warnings

from config.settings import MAX_THRESHOLD_FILE_DIFF_SEC


def check_csv_files_exist(battlefy_filename: str, gform_filename: str):
    """
    Checks if the specified Battlefy and Google Form CSV files exist.
    Raises FileNotFoundError if either file is missing.
    Args:
        battlefy_filename (str): Path to the Battlefy CSV file.
        gform_filename (str): Path to the Google Form CSV file.
    """
    # Check if Battlefy file exists
    if not os.path.isfile(battlefy_filename):
        raise FileNotFoundError(f"Battlefy csv file `{battlefy_filename}` not found")
    # Check if Google Form file exists
    if not os.path.isfile(gform_filename):
        raise FileNotFoundError(f"Google form csv file `{gform_filename}` not found")


def check_csv_files_datetime(battlefy_filename: str, gform_filename: str):
    """
    Checks the modification times of the Battlefy and Google Form CSV files.
    Warns if the files differ in age by more than MAX_THRESHOLD_FILE_DIFF_SEC seconds.
    Args:
        battlefy_filename (str): Path to the Battlefy CSV file.
        gform_filename (str): Path to the Google Form CSV file.
    """
    # Get modification times for both files
    battlefy_mod_date = os.path.getmtime(battlefy_filename)
    gform_mod_date = os.path.getmtime(gform_filename)

    # Convert timestamps to datetime objects
    battlefy_mod_date_datetime = datetime.datetime.fromtimestamp(battlefy_mod_date)
    gform_mod_date_datetime = datetime.datetime.fromtimestamp(gform_mod_date)

    # Calculate the difference in modification times
    date_diff = battlefy_mod_date_datetime - gform_mod_date_datetime

    # Warn if the difference exceeds the threshold
    if abs(date_diff.total_seconds()) > MAX_THRESHOLD_FILE_DIFF_SEC:
        warning_str = (
            f"Files `{battlefy_filename}` and `{gform_filename}` have an age difference of {date_diff}, "
            f"more than {MAX_THRESHOLD_FILE_DIFF_SEC} seconds"
        )
        warnings.warn(warning_str, RuntimeWarning)
