"""
Player model for SplashtagChecker.
Represents a player with splashtag, discord, and data source information.
"""

from dataclasses import dataclass
from typing import Optional
from models.data_source import DataSource


@dataclass
class Player:
    """
    Represents a player in SplashtagChecker.
    Attributes:
        splashtag (str): The player's Splashtag (in-game name).
        discord (str): The player's Discord username.
        source (Optional[DataSource]): The source of the player's data.
    """

    splashtag: str = ""
    discord: str = ""
    source: Optional[DataSource] = None

    def __eq__(self, other: object) -> bool:
        """
        Checks if two Player objects are equal based on splashtag, discord, and source.
        Args:
            other (object): The object to compare with.
        Returns:
            bool: True if equal, False otherwise.
        """
        if not isinstance(other, Player):
            return NotImplemented
        return (
            self.splashtag == other.splashtag
            and self.discord == other.discord
            and self.source == other.source
        )
