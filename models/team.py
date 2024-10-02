from dataclasses import dataclass, field
import models.player as Player
import models.data_source as DataSource


@dataclass
class Team:
    name: str = ""
    captain: Player = None
    players: list[Player] = field(default_factory=list)
    source: DataSource = None

    def __sub__(self, other):
        if self.name != other.name:
            raise AttributeError(f"Team names are not the same: \"{self.name}\" and \"{other.name}\"")
        if self.captain != other.captain:
            raise AttributeError(f"Team captains are not the same: \"{self.captain.discord}\" and "
                                 f"\"{other.captain.discord}\"")
        if self.source != other.source:
            raise AttributeError(f"Team sources are not the same: \"{self.source}\" and "
                                 f"\"{other.source}\"")
        return Team(self.name, self.captain.discord, [splashtag for splashtag in self.players if splashtag
                                                      not in other.players], self.source)


@dataclass
class TeamDiff:
    battlefy: [] = None
    gform: [] = None
