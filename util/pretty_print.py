from models.player import Player


def pretty_print_player_list(players: list[str]):
    player_list = ""
    for player in players:
        player_list += f" `{player}`,"
    return player_list[:-1]


def pretty_print_players(players: list[Player]):
    return pretty_print_player_list([player.splashtag for player in players])
