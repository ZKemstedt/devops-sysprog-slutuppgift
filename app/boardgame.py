from typing import List, Dict, Callable

from app.utils import str_sized


# -- how to use field checks --
# if field in FIELD_CHECK and FIELD_CHECK[field](value):
#   do stuff...
# eg: try to set field 'name' to 'test'
# if field in FIELD_CHECK and FIELD_CHECK['name']('test'):
#   item._modify('name', 'test')

BOARDGAME_FIELD_CHECK: Dict[str, Callable[[str], bool]] = {
    'title':                lambda x: not x.isdigit(),          # noqa 
    'players':              lambda x: x.isdigit(),              # noqa 
    'duration':             lambda x: x.isdigit(),              # noqa 
    'recommended_age':      lambda x: x.isdigit(),              # noqa 
    'times_played':         lambda x: x.isdigit(),              # noqa 
    'rating':               lambda x: x.isdigit(),              # noqa 
    }


class BoardGame(object):

    def __init__(self,
                 title: str,
                 players: str,
                 duration: str,
                 recommended_age: str,
                 times_played: str = '0',
                 rating: str = ''):

        self.title = title
        self.players = players
        self.duration = duration
        self.recommended_age = recommended_age
        self.times_played = times_played
        self.rating = rating
        self.name = self.title  # just an alias

    def _modify(self, field: str, value: str) -> None:
        setattr(self, field, value)

    def save(self) -> List:
        return [self.title, self.players, self.duration, self.recommended_age, self.rating, self.times_played]

    def __str__(self) -> str:
        return (''
                + str_sized(self.title, 29).ljust(30)
                + str_sized(self.players, 4).rjust(5)
                + (str_sized(self.duration, 8) + 'm ').rjust(10)
                + str_sized(self.recommended_age, 16).rjust(17)
                + str_sized(self.times_played, 13).rjust(14)
                + str_sized(self.rating, 7).rjust(8)
                )

    def inc_times_played(self, inc: int = 1) -> None:
        # I like storing my integers as strings, okay!?
        self.times_played = f'{int(self.times_played) + inc}'
