from Entities.player import Player, Squad

class Team:
    """
    Describes a sport team.

    :var name: name of team.
    :var url: URL of team.
    :var logo: path of team logo.
    :var players: list of players.
    :var new_players: list of players which are in lineup but are not in current squad.
    """

    def __init__(self, name: str, url: str, logo: str):
        self.__name = name
        self.__url = url
        self.__logo = logo
        self.__players = []
        self.__new_players = None

    @property
    def name(self) -> str:
        return self.__name

    @property
    def url(self) -> str:
        return self.__url

    @property
    def logo(self) -> str:
        return self.__logo

    @property
    def players(self) -> list:
        return self.__players
    @players.setter
    def players(self, players: list) -> None:
        self.__players = players

    @property
    def new_players(self) -> list:
        return self.__new_players

    def add_player(self, player: Player) -> None:
        """
        Addes player to list of players of a team.

        :param player: type of Player.
        """
        self.__players.append(player)

    def mark_players_info_squad(self, data_lineup: tuple):
        """
        Markes players by an information of lineup and sets new players which are not in current squad.

        :param data_lineup: tuple of (list of XI players, list of Sub players).
        """

        checked = []
        self.__new_players = []

        # check who in XI
        for player in self.__players:
            for xi in data_lineup[0]:
                if isinstance(xi, Player):
                    if xi == player:
                        player.info_squad = Squad.in_XI
                        checked.append(xi)
                        break
                else:
                    if xi in player.name:
                        player.info_squad = Squad.in_XI
                        checked.append(xi)
                        break

        # check who on Sub
        for player in self.__players:
            for sub in data_lineup[1]:
                if isinstance(sub, Player):
                    if sub == player:
                        player.info_squad = Squad.on_bench
                        checked.append(sub)
                        break
                else:
                    if sub in player.name:
                        player.info_squad = Squad.on_bench
                        checked.append(sub)
                        break

        # get players which weren't marked but were in lineup
        self.__new_players.extend(list(set(data_lineup[0] + data_lineup[1]).difference(set(checked))))

    def mark_players_info_squad_last_match(self, data_lineup: tuple):
        """
        Markes players by an information of last match lineup.

        :param data_lineup: tuple of (list of XI players, list of Sub players).
        """

        # check who was in XI
        for player in self.__players:
            for xi in data_lineup[0]:
                if isinstance(xi, Player):
                    if xi == player:
                        player.info_squad_last_match = Squad.in_XI
                        break
                else:
                    if xi in player.name:
                        player.info_squad_last_match= Squad.in_XI
                        break

        # check who was on Sub
        for player in self.__players:
            for sub in data_lineup[1]:
                if isinstance(sub, Player):
                    if sub == player:
                        player.info_squad_last_match = Squad.on_bench
                        break
                else:
                    if sub in player.name:
                        player.info_squad_last_match = Squad.on_bench
                        break