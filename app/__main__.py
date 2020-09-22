import yaml
from typing import List, Dict, Tuple
from pathlib import Path


INTRODUCTION = """
    Collection Manager v1
            by Zephyro
    """
MAIN_INSTRUCTIONS = """
    1 add boardgame         ::= 1 [title] [nplayers] [duration] [recommended_age]
    2 remove boardgame      ::= 2 [title|index]
    3 modify boardgame      ::= 3 [title|index] [field] [new value]
    4 list boardgames*      ::= 4
    5 rate boardgame*       ::= 5 [title|index] [rating]
    6 play boardgame*       ::= 6 [title|index]
    7 manage collections    ::= 7
    ? show help             ::= ?
    0 exit                  ::= 0
"""


class BoardGame(object):
    int_fields = ['nplayers', 'duration', 'age_recommendation', 'rating', 'times_played']
    hard_ints = ['times_played']

    def __init__(self, title: str, nplayers: str, duration: str, age: str, rating: str = '',
                 times_played: int = 0):
        self.title = title
        self.nplayers = nplayers
        self.duration = duration
        self.age_recommendation = age
        self.rating = rating  # text-based ratings are ok, eg: 'really-bad'
        self.times_played = times_played

    def modify(self, field: str, value: str) -> None:
        setattr(self, field, value)

    def save(self) -> List:
        return [self.title, self.nplayers, self.duration, self.age_recommendation, self.rating, self.times_played]

    def __str__(self) -> str:
        return (self.title.ljust(30) +
                self.nplayers.rjust(5) +
                (self.duration + ' min').rjust(10) +
                self.age_recommendation.rjust(17) +
                str(self.times_played).rjust(14) +
                self.rating.rjust(8)
                )

    def set_rating(self, rating: str) -> None:
        self.rating = rating

    def inc_times_played(self, inc: int = 1) -> None:
        self.times_played += inc


class Collection(object):

    def __init__(self, name: str, games: List[BoardGame] = []):
        self.games = games
        self.name = name

    def list_games(self) -> None:
        text = ('i'.ljust(3) +
                'title'.ljust(30) +
                'players'.rjust(5) +
                'duration'.rjust(10) +
                'recommended_age'.rjust(17) +
                'times_played'.rjust(14) +
                'rating'.rjust(8) +
                '\n\n')
        text += '\n'.join(f'{i}'.ljust(3) + str(game) for i, game in enumerate(self.games))
        print(text)

    def validate_game(self, key: str) -> BoardGame:
        if key.isdigit() and len(self.games) - 1 >= int(key):
            game = self.games[int(key)]
        elif key.isdigit():
            print('Error: index out of bounds.')
            game = None
        else:
            game = next((game for game in self.games if game.title == key), None)
            if not game:
                print(f'Error: game not found {key}')
        return game

    def add_game(self, title: str, nplayers: str, duration: str, age: str, rating: str = '',
                 times_played: int = 0) -> None:
        if any(game.title == title for game in self.games):
            print('Error: This game already exists.')
            return
        elif not all((nplayers.isdigit(), duration.isdigit(), age.isdigit(), isinstance(times_played, int))):
            # don't bother telling the user about times_played having to be an integer
            print('Error: [nplayers], [duration] and [age_recommendation] must all be integers!')
            return
        else:
            self.games.append(BoardGame(title, nplayers, duration, age, rating, times_played))
            print('Successfully added the game.')

    def remove_game(self, key: str) -> None:
        game = self.validate_game(key)
        if game:
            self.games.remove(game)
            print('Successfully removed the game.')

    def edit_game(self, key: str, field: str, value: str) -> None:
        game = self.validate_game(key)
        if game:
            if field not in vars(game):
                print(f'Error: Invalid field `{field}`')
                return
            if field in BoardGame.int_fields and not value.isdigit():
                print(f'Error: {field} must be an integer!')
                return
            else:
                if field in BoardGame.hard_ints:
                    value = int(value)
                game.modify(field, value)
                print(f'Successfully set {field} to {value} for {game.title}')

    def rate_game(self, key: str, rating: str) -> None:
        game = self.validate_game(key)
        if game:
            game.set_rating(rating)
            print(f'Successfully set rating to {rating} for {game.title}')

    def play_game(self, key: str) -> None:
        game = self.validate_game(key)
        if game:
            game.inc_times_played()
            print(f'Played the game once, total times played: {game.times_played}')

    def save(self) -> Dict:
        return {
            'name': self.name,
            'boardgames': [game.save() for game in self.games]
        }


def user_input() -> Tuple[str, ]:
    return input('>> ').strip().lower().split(' ')


def main_menu(collections) -> Tuple[List, int]:
    while True:

        try:
            args = user_input()
            action = args.pop(0)

            if not args:  # only action
                if not action:
                    print('type ? for help, 0 to exit')
                elif action == '?':
                    print(MAIN_INSTRUCTIONS)
                elif action == '0':
                    print('Saving data and exiting...')
                    break
                elif action == '4':
                    collection.list_games()
                elif action == '7':
                    return 2
                else:
                    print('Invalid action or argument count.')
            else:
                try:
                    if action == '1':
                        collection.add_game(*args)
                    elif action == '2':
                        collection.remove_game(*args)
                    elif action == '3':
                        collection.edit_game(*args)
                    elif action == '5':
                        collection.rate_game(*args)
                    elif action == '6':
                        collection.play_game(*args)
                    else:
                        print('Invalid action or argument count.')
                except TypeError as e:
                    print(e)  # for debugging
                    print('Invalid argument count, returning to main menu...')

        except KeyboardInterrupt:
            print('Saving data and exiting...')
            break
    return 0


if __name__ == "__main__":
    # load data
    file = Path('collectiondata', 'boardgamecollections.yml')
    with file.open(encoding="UTF-8") as f:
        data = yaml.safe_load(f)
    if not data:
        data = []
        print('File was empty or did not exist, no collections have been loaded.')

    # Convert data to Collection and BoardGame objects
    collections = []
    for collection in data:
        boardgames = [BoardGame(*args) for args in collection['boardgames']]
        collections.append(Collection(name=collection['name'], games=boardgames))
    if collections:
        print(f'Loaded {len(collections)} collections from file.')

    # cleanup
    del data

    # starting point
    if not collections:
        collections.append(Collection(name='Base'))

    collection = collections[0]
    code = 1  # 0: exit, 1: main_menu, 2: manage_collections

    # start main loop
    print(INTRODUCTION)
    print(MAIN_INSTRUCTIONS)
    while True:
        if code == 1:
            if not collection:
                print('Warning: the last selected collection was deleted.')
                if not collections:
                    print('Creating default collection \"Base\"...')
                    collections.append(Collection(name='Base'))
                collection = collections[0]
                print(f'Selected collection {collection.name}.')
            code = main_menu(collection)
        elif code == 2:
            print('Not yet implemented')
            code = 1

        if code == 0:
            break

    # save data
    data = [collection.save() for collection in collections]
    with file.open(mode='w', encoding="UTF-8") as f:
        yaml.dump(data, f, default_flow_style=False, explicit_start=True)
    # exit


# TODO

# - Advanced -
# list (filter) collection of boardgames

# - Bonus -
# list all boardgames (in all collections)
# change collection
# filter-extension: show non-exact matches at bottom of lis
