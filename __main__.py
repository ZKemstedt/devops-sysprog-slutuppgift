import yaml
import typing as t
from pathlib import Path


FILENAME = 'boardgamecollections.yml'


class BoardGame(object):

    def __init__(self, title: str, nplayers: int, duration: int, age: int):
        self.title = title
        self.nplayers = nplayers
        self.duration = duration
        self.age_recommendation = age

    def modify(self):
        options = ['title', 'age_recommendation', 'duration', 'players']
        print('What do you want to modify?\n'
              f'Can only select one of {", ".join(options).rstrip(", ")}.')
        field = get_user_input(options=options)

        print(f'Set a new value for {field}.')
        value = get_user_input(isint=field not in 'title')
        setattr(self, field, value)
        print(f'Set {field} to {value}.')

    def save(self) -> t.List:
        return [self.title, self.nplayers, self.duration, self.age_recommendation]


class Collection(object):

    def __init__(self, name: str, games: t.List[BoardGame] = []):
        self.boardgames = games
        self.name = name  # name to differentiate between different collections, default name = 'default' ?

    def __str__(self) -> str:
        return ''  # List games

    def add_game(self):
        pass

    def remove_game(self):
        pass

    def edit_game(self):
        pass

    def save(self) -> t.Dict:
        return {
            'name': self.name,
            'boardgames': [game.save() for game in self.boardgames]
        }


def load_data(filename: str = FILENAME) -> t.List[t.Dict]:
    """Load data from filename (default: boardgamecollections.yml). If the file does not exist, create it"""
    file = Path(filename)
    if not file.exists():
        print(f"Creating {filename} ...")
        file.touch()
        data = []
    else:
        with Path(filename).open(mode='r', encoding="UTF-8") as f:
            data = yaml.safe_load_all(f)
    return data


def save_data(data: dict, filename: str = FILENAME) -> None:
    """Save data to filename (default: boardgamecollections.yml)."""
    with Path(filename).open(mode='w', encoding="UTF-8") as f:
        yaml.dump_all(data, f, default_flow_style=False, explicit_start=True)


def get_user_input(prompt: str = '>> ', isint: bool = False, options: t.List[str] = None) -> t.Union[str, int]:
    pass


if __name__ == "__main__":
    # load data
    collections = []
    for collection in load_data():
        boardgames = [BoardGame(*args) for args in collection['boardgames']]
        collections.append(Collection(name=collection['name'], games=boardgames))
        print(collections)

    # do stuff

    # save data
    save_data([collection.save() for collection in collections])
    # exit


# -- Data --

# - load -
# file -> List [ Collection [ BoardGames ] ]
#
#   fileformat -> List [
#       Dict { (Collection)
#           name: str,
#           boardgames: List [
#               Dict { (BoardGame)
#                   title: str,
#                   nplayers: int,
#                   duration: int,
#                   age_recommendation: int
#               }
#           ]
#       }
#   ]


# - save -
# List [ Collection [ BoardGames ] ] -> file


# -- Input & Menu Loop --

# - Basic -
# list all boardgames (in collection)
# create new boardgame
# select boardgame (??)
# edit existing boardgame
# remove boardgame

# - Advanced -
# search (filter) collection of boardgames

# - Bonus -
# list all boardgames (in all collections)
# change collection
# played
# user_ratings
# filter-extension: show non-exact matches at bottom of list.
