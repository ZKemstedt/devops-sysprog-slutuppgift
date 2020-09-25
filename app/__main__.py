import yaml
from typing import List, Dict, Tuple, Optional, Any
from pathlib import Path

CLEAR = 50 * '\n'

INTRODUCTION = """
    Boardgame Collection Manager
    (Boardgames sold separately)

    All arguments to commands should be separated by spaces,
    If you want multi-worded names or the like, use
    dashes (-) in place of spaces. eg: Zephyro-Kemstedt-the-almighty

    Made by Zephyro @ https://github.com/ZKemstedt/devops-sysprog-slutuppgift
    """

MAIN_MENU_INSTRUCTIONS = """
  1 add boardgame             ::= 1 [title] [players] [duration] [recommended_age]
  2 remove boardgame          ::= 2 [title|index]
  3 modify boardgame          ::= 3 [title|index] [field] [new value]
  4 list boardgames*          ::= 4
  5 rate boardgame            ::= 5 [title|index] [rating]
  6 play boardgame            ::= 6 [title|index]
  - - - - - - - - - - - - - - - - -
  8 manage collections        ::= 8
  ? show help                 ::= ?
  0 exit                      ::= 0
"""


MANAGE_COLLECTIONS_MENU_INSTRUCTIONS = """
  1 create new collection     ::= 1 [name]
  2 remove collection         ::= 2 [index|name]
  3 change collection name    ::= 3 [index|name] [new name]
  4 list all collections      ::= 4
  5 select active collection  ::= 5 [index|name]
  - - - - - - - - - - - - - - - - -
  8 main menu                 ::= 8
  ? show help                 ::= ?
  0 exit                      ::= 0
"""

FILTER_MARGINS = {
    # Collection
    'name': '',
    # BoardGame
    'title': '',
    'players': 2,
    'duration': 4,
    'age_recommendation': 3,
    'rating': 1,
    'times_played': 5,
}


class BoardGame(object):
    int_fields = ['players', 'duration', 'age_recommendation', 'rating', 'times_played']
    fields = int_fields + ['title']

    def __init__(self, title: str, players: str, duration: str, age: str, times_played: str = '', rating: str = ''):
        self.title = title
        self.players = players
        self.duration = duration
        self.age_recommendation = age
        self.times_played = times_played
        self.rating = rating

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

    def set_rating(self, rating: str) -> None:
        self.rating = rating

    def inc_times_played(self, inc: int = 1) -> None:
        # I like storing my integers as strings, okay!?
        self.times_played = f'{int(self.times_played) + int(inc)}'


class Collection(object):

    def __init__(self, name: str, games: List[BoardGame] = []):
        self.games = games
        self.name = name

    def change_name(self, name: str) -> None:
        if name.isdigit():
            print('Error: Collection name cannot be a number')
            return None
        self.name = name

    def __str__(self) -> str:
        text = f'\n\t\tCollection: {self.name}\n'
        text += self.list_games()
        return text

    def list_games(self, *filter_args) -> str:
        line = '\n' + '---' * 30 + '\n'
        weak_line = '\n' + '-  ' * 30 + '\n'
        header = (''
                  + 'title'.ljust(30)
                  + 'players'.rjust(5)
                  + 'duration'.rjust(10)
                  + 'recommended_age'.rjust(17)
                  + 'times_played'.rjust(14)
                  + 'rating'.rjust(8)
                  )

        if filter_args:
            filters = validate_filters(BoardGame.fields, *filter_args)
            if filters:
                print(f'Debug (l_g): filters: {filters}')
                return stringify_filter_results(header, *_filter(items=self.games, filters=filters))

        header = 'i'.ljust(3) + header
        text = '\n'.join(f'{i}'.ljust(3) + str(game) for i, game in enumerate(self.games))
        return line + header + weak_line + text + line

    def get_game(self, key: str) -> BoardGame:
        """Return the `BoardGames` instance at index `key` or with the title `key`"""
        if key.isdigit() and len(self.games) - 1 >= int(key):
            game = self.games[int(key)]
        elif key.isdigit():
            print('Error: index out of bounds.')
            return None
        else:
            game = next((game for game in self.games if game.title == key), None)
        if not game:
            print(f'Error: game `{key}` could not be found.')
        return game

    def add_game(self, title: str, players: str, duration: str, age: str,
                 times_played: str = '', rating: str = '') -> None:
        if any(game.title == title for game in self.games):
            print('Error: This game already exists.')
            return
        elif not all((players.isdigit(), duration.isdigit(), age.isdigit(), times_played.isdigit())):
            print('Error: [players], [duration] and [age_recommendation] must all be integers!')
            return
        else:
            self.games.append(BoardGame(title, players, duration, age, rating, times_played))
            print('Info: Successfully added the game.')

    def remove_game(self, game: BoardGame) -> None:
        if game in self.games:
            self.games.remove(game)
            print('Info: Successfully removed the game.')

    def edit_game(self, game: BoardGame, field: str, value: str) -> None:
        if game in self.games and field in BoardGame.fields:
            if field in BoardGame.int_fields and value.isdigit() or field not in BoardGame.int_fields:
                game.modify(field, value)
                print(f'Info: Successfully set {field} to {value} for {game.title}')

    def rate_game(self, game: BoardGame, rating: str) -> None:
        if game in self.games:
            game.set_rating(rating)
            print(f'Info: Successfully set rating to {rating} for {game.title}')

    def play_game(self, game: BoardGame) -> None:
        if game in self.games:
            game.inc_times_played()
            print(f'Info: You played the game, total times played: {game.times_played}')

    def save(self) -> Dict:
        return {
            'name': self.name,
            'boardgames': [game.save() for game in self.games]
        }


def user_input(prompt: Optional[str] = '') -> Tuple[str, ]:
    if prompt:
        prompt = prompt.strip() + ' '
    return input(f'{prompt}>> ').strip().lower().split(' ')


def str_sized(string: str, lenth: int) -> str:
    """Force a string to be max `lenth` characters long by cutting off any extra characters.

    Args:
        string (str): the string to format
        lenth (int): the max lenth of the string

    Returns:
        str: the lenth-formatted string
    """
    return string if len(string) <= lenth else string[:lenth] + ' '


def big_title(titletext: str) -> str:
    """Generate a fancy title spacer, takes the titletext as an argument which must be less than 40 characters long."""
    if len(titletext) > 40:
        print(f'Warning: titletext larger than 40 charachters!\n{titletext}')
        titletext = 'Invalid title, stupid.'
    line = f'>{"-"*50}<'
    space = f'>{" "*50}<'
    delta, remainder = divmod((50 - len(titletext)), 2)
    fill1 = '' if remainder < 1 else ' '
    fill2 = '' if remainder < 2 else ' '
    title = f'>{" "*delta}{fill1}{titletext}{fill2}{" "*delta}<'
    return '\n'.join('{:^80}'.format(s) for s in [line, space, title, space, line])


def get_collection(collections: List[Collection], key: str) -> Collection:
    """Return the Collection instance specified by `key` if found in `collections`, else None."""
    if key.isdigit() and len(collections) - 1 >= int(key):
        return collections[int(key)]
    elif key.isdigit():
        print('Error: index out of bounds.')
        return None
    else:
        collection = next((col for col in collections if col.name == key), None)
        if not collection:
            print(f'Error: collection `{key}` could not be found.')
        return collection


def validate_filters(fields: List[str], *filter_args: List[str]) -> List[Tuple[str, str]]:
    """Construct a list of valid filter tuples (field, value) from a list of valid fields and user input."""
    filters = []  # NOTE (v_f) v_f

    # print(f'Debug (v_f): len(args): {len(filter_args)}')
    # print(f'Debug (v_f): filter_args: {filter_args}')
    for i in range(0, len(filter_args), 2):
        try:
            # print(f'Debug (v_f): Trying filter construction {i}...')
            field = filter_args[i]
            value = filter_args[i+1]
            # print(f'Debug (v_f): Field: {field}, value: {value}')
            if any(field in fil[0] for fil in filters):
                print('Warning: Cannot have more than 1 filter per field!')
                print(f'Info: denied filter: ({field}, {value})')
                continue
            elif field in fields:
                filters.append((field, value))
                # print(f'Debug (v_f): Added to filters, filters is now: {filters}')
            else:
                print(f'Debug (v_f): invalid field {field}')
        except IndexError as e:
            print(f'Debug (v_f): filter construction failed during iteration {i}.')
            print(f'Debug (v_f): remaining args: {filter_args}')
            print(f'Debug (v_f): {e}')
            break
    return filters


# NOTE / TODO Actually `close_matches` is a list of str, not a list of Any, currently this is not a problem
# because the returned values of this function is always printed, this might cause issues in the future.
def _filter(items: List[Any], filters: List[Tuple[str, str]]) -> Tuple[List[Any], List[Any]]:
    """Apply a sequence of filters on a sequence of objects, return the exact- and close matches"""
    # 1. exact matches: iteratively filter out the intersection of all items and the matches
    exact_matches = set(items)
    for field, value in filters:
        exact_matches &= {item for item in items if getattr(item, field) == value}

    # 2. close matches:
    #       partial matches (matches that only match some fields)
    #       marginal matches (fields with margin match within it)
    # 2.1. Get ALL matches against the items not included in `exact matches`
    all_close_matches = []
    remaining_items = list(set(items) - exact_matches)
    for field, value in filters:
        if isinstance(FILTER_MARGINS[field], str):
            all_close_matches += [item for item in remaining_items if getattr(item, field) == value]
        else:
            all_close_matches += [item for item in remaining_items
                                  if abs(int(getattr(item, field)) - int(value)) <= FILTER_MARGINS[field]]
    # 2.2. Sort by match count
    match_count = {}
    for item in set(all_close_matches):
        match_count[all_close_matches.count(item)] = item
    close_matches = [v for k, v in sorted(match_count.items(), key=lambda item: item[0])]

    return exact_matches, close_matches  # NOTE actually `close_matches` is a list of str, not a list of Any


def stringify_filter_results(header: str, exact_result: List[Any], close_result: List[Any]) -> str:
    """Creates and returns a nice display format string for the results from a `_filter` call"""
    line = '\n' + '---' * 30 + '\n'
    weak_line = '\n' + '-  ' * 30 + '\n'
    if exact_result:
        exact_text = '\n'.join(str(item) for item in (exact_result))
    else:
        exact_text = f'{"< no exact matches >":^80}'
    if close_result:
        close_text = '\n'.join(str(item) for item in (close_result))
    else:
        close_text = f'{"< no close matches >":^80}'
    return line + header + weak_line + exact_text + weak_line + close_text + line


def main(col: Collection, cols: List[Collection]) -> None:
    """Main Menu loop

    Args:
        col (Collection): The currently selected instance of `Collection`.
        cols: (List[Collection]) The currently registered collections.
    """
    MAIN_MENU_CHOICES = {
        '1': lambda col, *args: col.add_game(*args),
        '2': lambda col, key: col.remove_game(col.get_game(key)),
        '3': lambda col, key, field, value: col.edit_game(col.get_game(key), field, value),
        '4': lambda x: col.list_games(),
        '5': lambda col, key, rating: col.rate_game(col.get_game(key), rating),
        '6': lambda col, key: col.play_game(col.get_game(key)),
        '7': lambda col, *args: col.list_games(*args),
        '8': lambda x: MANAGE_COLLECTIONS_MENU_CHOICES,
        '?': lambda x: MAIN_MENU_INSTRUCTIONS,
        '0': lambda x: 0,
        # "secret", not harmful
        'title': lambda x: big_title('Main Menu'),
    }

    MANAGE_COLLECTIONS_MENU_CHOICES = {
        '1': lambda name: cols.append(Collection(name)
                                      if not any(c.name == name for c in cols)
                                      else 'Error: a collection with that name already exists'),
        '2': lambda key: cols.remove(get_collection(key)) if get_collection(key) else None,
        '3': lambda key, name: get_collection(key).change_name(name) if get_collection(key) else None,
        '4': lambda x: CLEAR + [str(c) for c in cols],
        '5': lambda key: get_collection(key),
        '8': lambda x: MAIN_MENU_CHOICES,
        '?': lambda x: MANAGE_COLLECTIONS_MENU_INSTRUCTIONS,
        '0': lambda x: 0,
        # "secret", not harmful
        'title': lambda x: big_title('Manage Collections'),
    }
    print(CLEAR)

    # Start at main menu
    _menu = MAIN_MENU_CHOICES
    print(_menu['title'](None))
    print(_menu['?'](None))

    while True:
        ret = None
        if col:
            col_prompt = col.name if len(col.name) <= 15 else col.name[:13] + '...'
        else:
            col_prompt = ('< no collection >')
        try:
            args = user_input(f'(col: {col_prompt})')
        except KeyboardInterrupt:
            return 0
        action = args.pop(0)

        if action in _menu:
            try:
                if args:
                    ret = _menu[action](*args)
                else:
                    ret = _menu[action](None)
                # print(f'Debug: type(ret): {type(ret)}')
                # print(f'Debug: value(ret): {ret}')
            except ValueError as e:
                print('Error: Invalid argument count')
                print(f'Debug: {e}')

            if isinstance(ret, int):
                return
            elif isinstance(ret, str):
                print(ret)
            elif isinstance(ret, Collection):
                col = ret
            elif isinstance(ret, dict):
                _menu = ret
                print(CLEAR)
                print(_menu['title'](None))
                print(_menu['?'](None))

        elif not action:
            print('Tips: type ? for help, 0 to exit')
        else:
            print('Error: Invalid command.')


if __name__ == "__main__":
    print(CLEAR)
    print('Debug: Program start.')
    # load data
    file = Path('collectiondata', 'boardgamecollections.yml')
    with file.open(encoding="UTF-8") as f:
        data = yaml.safe_load(f)
    if not data:
        data = []
        print('Warning: File was empty or did not exist, no collections have been loaded.')

    # Convert data to Collection and BoardGame objects
    collections = []
    for collection in data:
        boardgames = [BoardGame(*args) for args in collection['boardgames']]
        collections.append(Collection(name=collection['name'], games=boardgames))
    if collections:
        print(f'Info: Loaded {len(collections)} collections from file.')

    # cleanup
    del data

    # starting point
    if not collections:
        collections.append(Collection(name='Base'))
    collection = collections[0]

    # start main (menu).
    print(INTRODUCTION)
    try:
        input('(press enter to start)')
    except Exception:
        pass
    else:
        main(collection, collections)
    print('Info: Saving data and exiting...')

    # save data
    data = [collection.save() for collection in collections]
    with file.open(mode='w', encoding="UTF-8") as f:
        yaml.dump(data, f, default_flow_style=False, explicit_start=True)

    # exit
    print('Debug: Program exit.')
