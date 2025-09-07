"""
Team model for SplashtagChecker.
Represents a team with a name, captain, list of players, and data source.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from models.player import Player
from models.data_source import DataSource


@dataclass
class Team:
    """
    Represents a team in SplashtagChecker.
    Attributes:
        name (str): The team's name.
        captain (Optional[Player]): The team's captain.
        players (List[Player]): List of players in the team.
        source (Optional[DataSource]): The source of the team's data.
    """
    name: str = ""
    captain: Optional[Player] = None
    players: List[Player] = field(default_factory=list)
    source: Optional[DataSource] = None

    def __sub__(self, other: object) -> 'Team':
        """
        Returns a new Team with players that are in self but not in other.
        Raises AttributeError if team names, captains, or sources differ.
        Args:
            other (object): The other Team to compare against.
        Returns:
            Team: A new Team with the difference in players.
        """
        if not isinstance(other, Team):
            raise TypeError("Subtraction only supported between Team objects.")
        if self.name != other.name:
            raise AttributeError(f"Team names are not the same: '{self.name}' and '{other.name}'")
        if self.captain != other.captain:
            raise AttributeError(f"Team captains are not the same: '{self.captain}' and '{other.captain}'")
        if self.source != other.source:
            raise AttributeError(f"Team sources are not the same: '{self.source}' and '{other.source}'")
        # Return a new Team with players in self but not in other
        diff_players = [player for player in self.players if player not in other.players]
        return Team(name=self.name, captain=self.captain, players=diff_players, source=self.source)


@dataclass
class TeamDiff:
    """
    Represents the difference between teams from Battlefy and Google Forms sources.
    Attributes:
        battlefy (Optional[Team]): Team from Battlefy source.
        gform (Optional[Team]): Team from Google Forms source.
    """
    battlefy: Optional[Team|set[str]] = None
    gform: Optional[Team|set[str]] = None
