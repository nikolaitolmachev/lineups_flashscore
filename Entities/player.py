import enum

class Position(enum.Enum):
    Goalkeepers = 'G'
    Defenders = 'D'
    Midfielders = 'M'
    Forwards = 'A'
    Unknown = '?'

    @staticmethod
    def get_names():
        return [Position.Goalkeepers.name, Position.Defenders.name,
                    Position.Midfielders.name, Position.Forwards.name]

class Squad(enum.Enum):
    in_XI = 1
    on_bench = 0
    absent = -1


class Player:
    """
    Describes a sport player.

    :var name: name of player.
    :var url: URL of player.
    :var nationality: nationality of player.
    :var number: number of player.
    :var age: age of player.
    :var position: type of Position.
    :var matches_played: matches played.
    :var goals_scored: goals scored.
    :var info_squad: type of Squad. Default: absent.
    :var info_squad_last_match: type of Squad. Default: absent.
    """

    def __init__(self, name: str, url: str, nationality: str, number: int, age: int, position: Position,
                 matches_played: int, goals_scored: int):
        self._name = name
        self._url = url
        self._nationality = nationality
        self._number = number
        self._age = age
        self._position = position
        self._matches_played = matches_played
        self.__goals_scored = goals_scored
        self._info_squad = Squad.absent
        self._info_squad_last_match = Squad.absent

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str:
        return self._url

    @property
    def nationality(self) -> str:
        return self._nationality

    @property
    def number(self) -> int:
        return self._number

    @property
    def age(self) -> int:
        return self._age

    @property
    def position(self) -> Position:
        return self._position

    @property
    def matches_played(self) -> int:
        return self._matches_played

    @property
    def goals_scored(self) -> int:
        return self.__goals_scored

    @property
    def info_squad(self) -> Squad:
        return self._info_squad
    @info_squad.setter
    def info_squad(self, squad: Squad) -> None:
        self._info_squad = squad

    @property
    def info_squad_last_match(self) -> Squad:
        return self._info_squad_last_match

    @info_squad_last_match.setter
    def info_squad_last_match(self, squad: Squad) -> None:
        self._info_squad_last_match = squad

    def __str__(self):
        if self._number is not None:
            return f'{self._number}\t{self._name}\t\t{self._position.value}\t{self._age}\t{self._nationality}\t' \
               f'{self._matches_played}\t{self.__goals_scored}'
        else:
            return f'{self._name}'

    def __hash__(self):
        return hash(self._url + self._name)

    def __eq__(self, other):
        if isinstance(other, Player):
            return self._url == other.url
        return False

    def __ne__(self, other):
        return not self == other


class IHGoalkeeper(Player):
    """
    Describes an ice hockey player.

    :var sv: save percentage.
    :var gaa: goals against average.
    :var so: shutouts.
    """

    def __init__(self, name: str, url: str, nationality: str, number: int, age: int, position: Position,
                 matches_played: int, sv: float, gaa: float, so: int):
        super().__init__(name, url, nationality, number, age, position, matches_played, 0)
        self.__sv = sv
        self.__gaa = gaa
        self.__so = so

    @property
    def sv(self) -> float:
        return self.__sv

    @property
    def gaa(self) -> float:
        return self.__gaa

    @property
    def so(self) -> int:
        return self.__so

    def __str__(self):
        if self.number is not None:
            return f'{self._number}\t{self._name}\t\t{self._position.value}\t{self._age}\t{self._nationality}\t' \
                   f'{self._matches_played}\t{self.__sv}\t{self.__gaa}\t{self.__so}'
        else:
            return f'{self.name}'



