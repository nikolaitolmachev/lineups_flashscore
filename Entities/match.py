import enum
from Entities.team import Team

class Sport(enum.Enum):
    football = 'Football'
    hockey = 'Hockey'

class Match:
    """
    Describes a sport match.

    :var sport: type of Sport.
    :var url: URL of a match.
    :var tournament: name of tournament.
    :var team_a: type of Team.
    :var team_b: type of Team.
    """

    def __init__(self, sport: Sport, url: str, tournament: str, team_a: Team, team_b: Team):
        self.__sport = sport
        self.__url = url
        self.__tournament = tournament
        self.__team_a = team_a
        self.__team_b = team_b

    @property
    def sport(self) -> Sport:
        return self.__sport

    @property
    def url(self) -> str:
        return self.__url

    @property
    def tournament(self) -> str:
        return self.__tournament

    @property
    def team_a(self) -> Team:
        return self.__team_a

    @property
    def team_b(self) -> Team:
        return self.__team_b



