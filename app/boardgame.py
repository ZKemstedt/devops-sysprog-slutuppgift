from typing import List

# how to perform check? eg: is the value '5' ok for field (key) 'duration' ?
# check_result = BOARDGAME_FIELD_CHECK['duration']('5')
# -> True
BOARDGAME_FIELD_CHECK = {
    'title':                lambda x: not x.isdigit(),
    'players':              lambda x: x.isdigit(),
    'duration':             lambda x: x.isdigit(),
    'age_recommendation':   lambda x: x.isdigit(),
    'times_played':         lambda x: x.isdigit(),
    'rating':               lambda x: x.isdigit(),
    }


class BoardGame(object):

    def __init__(self, title: str, players: str, duration: str, age: str, times_played: str = '0', rating: str = ''):
        self.title = title
        self.players = players
        self.duration = duration
        self.age_recommendation = age
        self.times_played = times_played
        self.rating = rating
        self.name = self.title

    def modify(self, field: str, value: str) -> None:
        setattr(self, field, value)

    def save(self) -> List:
        return [self.title, self.players, self.duration, self.age_recommendation, self.rating, self.times_played]

    def __str__(self) -> str:
        return (str_sized(self.title, 29).ljust(30)
                + str_sized(self.players, 4).rjust(5)
                + (str_sized(self.duration, 8) + 'm ').rjust(10)
                + str_sized(self.age_recommendation, 16).rjust(17)
                + str_sized(self.times_played, 13).rjust(14)
                + str_sized(self.rating, 7).rjust(8)
                )

    def inc_times_played(self, inc: int = 1) -> None:
        # I like storing my integers as strings, okay!?
        self.times_played = f'{int(self.times_played) + inc}'


def str_sized(string: str, lenth: int) -> str:
    """Force a string to be max `lenth` characters long by cutting off any extra characters.

    Args:
        string (str): the string to format
        lenth (int): the max lenth of the string

    Returns:
        str: the lenth-formatted string
    """
    return string if len(string) <= lenth else string[:lenth] + ' '
