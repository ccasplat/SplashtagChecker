"""
DataSource Enum for SplashtagChecker.
Represents the source of team/player data (Google Forms, Battlefy, Sendou).
"""

from enum import Enum


class DataSource(Enum):
    """
    Enum representing the source of team/player data.
    Members:
        GOOGLE_REGISTRATION: Data from Google Forms registration.
        BATTLEFY: Data from Battlefy export.
        SENDOU: Data from Sendou.
    """

    GOOGLE_REGISTRATION = 1
    BATTLEFY = 2
    SENDOU = 3
