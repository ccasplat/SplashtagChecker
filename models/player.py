from dataclasses import dataclass
import models.data_source as DataSource


@dataclass
class Player:
    splashtag: str = ""
    discord: str = ""
    source: DataSource = None

    def __eq__(self, other):
        return self.splashtag == other.splashtag and self.discord == other.discord and self.source == other.source

