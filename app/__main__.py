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

MAIN_MENU_CHOICES = [
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '8',
    '?',
    '0',
]

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

MANAGE_COLLECTIONS_MENU_CHOICES = [
    '1',
    '2',
    '3',
    '4',
    '5',
    '8',
    '?',
    '0',
]

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

    def validate_game(self, key: str) -> BoardGame:
        if key.isdigit() and len(self.games) - 1 >= int(key):
            game = self.games[int(key)]
        elif key.isdigit():
            print('Error: index out of bounds.')
            game = None
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

    def remove_game(self, key: str) -> None:
        game = self.validate_game(key)
        if game:
            self.games.remove(game)
            print('Info: Successfully removed the game.')

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
                game.modify(field, value)
                print(f'Info: Successfully set {field} to {value} for {game.title}')

    def rate_game(self, key: str, rating: str) -> None:
        game = self.validate_game(key)
        if game:
            game.set_rating(rating)
            print(f'Info: Successfully set rating to {rating} for {game.title}')

    def play_game(self, key: str) -> None:
        game = self.validate_game(key)
        if game:
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


def validate_collection(collections: List[Collection], key: str) -> Collection:
    """Return the collection specified by `key` if found, else None.

    Args:
        collections (List[Collection]): the currently registered Collections
        key (str): Either the index of the Collection or the name of the Collection

    Returns:
        Collection: the Collection that was identified. If no collection was found, this is None
    """
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
    """Construct a list of valid filter tuples (field, value) from user input.

    Args:
        fields (List[str]): the fields that can be filtered
        filter_args (List[str]): the user's input

    Returns:
        List[Tuple[str, str]]: list of filter tuples (field, value)
    """
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


def _filter(items: List[Any], filters: List[Tuple[str, str]]) -> Tuple[List[Any], List[Any]]:
    """Filter through a sequence of objects, return the exact- and close matches

    Args:
        items (List[Any]): the sequence of items to filter
        filters (List[Tuple[str, str]]): the filters to use, as returned by `validate_filters()`.

    Returns:
        Tuple[List[Any], List[Any]]: Two lists containing the exact matches and close matches respectively
    """
    # 1. exact matches by iterative intersection of items and matches
    exact_matches = set(items)
    for field, value in filters:
        exact_matches &= {item for item in items if getattr(item, field) == value}

    # 2 close matches:
    #       partial matches (matches that only match some fields)
    #       marginal matches (fields with margin match within it)
    # 2.1 close matches ~ get ALL matches against the items not included in `exact matches`
    all_close_matches = []
    remaining_items = list(set(items) - exact_matches)
    for field, value in filters:
        if isinstance(FILTER_MARGINS[field], str):
            all_close_matches += [item for item in remaining_items if getattr(item, field) == value]
        else:
            all_close_matches += [item for item in remaining_items
                                  if abs(int(getattr(item, field)) - int(value)) <= FILTER_MARGINS[field]]
    # 2.2 close matches ~ sort by match count
    match_count = {}
    for item in set(all_close_matches):
        match_count[str(item)] = all_close_matches.count(item)
    close_matches = [k for k, v in sorted(match_count.items(), key=lambda item: item[1])]

    return exact_matches, close_matches


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


def main_menu(collection: Collection) -> int:
    """Main Menu loop

    Args:
        collection (Collection): The currently selected collection instance.

    Returns:
        ccode (int): 0 to exit, 2 to go to manage_collections
    """
    print(CLEAR)
    print(big_title('Main Menu'))
    print(MAIN_MENU_INSTRUCTIONS)
    while True:

        col = collection.name if len(collection.name) <= 15 else collection.name[:13] + '...'
        prompt = f'(col: {col})'
        try:
            args = user_input(prompt)
            action = args.pop(0)
            if not action:
                print('Tips: type ? for help, 0 to exit')

            elif action not in MAIN_MENU_CHOICES:
                print('Error: Invalid command.')

            elif not args:
                if action == '?':
                    print(MAIN_MENU_INSTRUCTIONS)
                elif action == '0':
                    ccode = 0
                    break
                elif action == '4':
                    print(collection.list_games())
                elif action == '8':
                    ccode = 2
                    break
                else:
                    print('Error: Invalid argument count')
            else:
                if action == '1' and len(args) >= 4 and len(args) <= 6:
                    collection.add_game(*args)

                elif action == '2' and len(args) == 1:
                    key = args[0]
                    collection.remove_game(key)

                elif action == '3' and len(args) == 3:
                    key, field, value = args
                    collection.edit_game(key, field, value)

                elif action == '4':
                    print(collection.list_games(*args))

                elif action == '5' and len(args) == 2:
                    key, rating = args
                    collection.rate_game(key, rating)

                elif action == '6' and len(args) == 1:
                    key = args[0]
                    collection.play_game(key)
                else:
                    print('Error: Invalid argument count')

        except KeyboardInterrupt:
            ccode = 0
            break
    return ccode


def manage_collections_menu(collection: Collection, collections: List[Collection]) -> Tuple[Collection, int]:
    """Manage collections menu loop

    Args:
        collection (Collection): the currently active Collection
        collections (List[Collection]): the currently registered Collections

    Returns:
        Collection: the currently selected Collection. If deleted, this will be None
        ccode (int): 0 to exit, 1 to go to main menu [ccode]
    """
    print(CLEAR)
    print(big_title('Manage Collections'))
    print(MANAGE_COLLECTIONS_MENU_INSTRUCTIONS)
    while True:

        if collection:
            col = collection.name if len(collection.name) <= 15 else collection.name[:13] + '...'
            prompt = f'(col: {col})'
        else:
            prompt = '(<no collection>)'
        try:
            args = user_input(prompt)
            action = args.pop(0)
            if not action:
                print('Tips: type ? for help, 0 to exit')

            elif action not in MANAGE_COLLECTIONS_MENU_CHOICES:
                print('Error: Invalid command')

            elif not args:
                if action == '?':
                    print(MANAGE_COLLECTIONS_MENU_INSTRUCTIONS)
                elif action == '0':
                    ccode = 0
                    break
                elif action == '4':
                    print(CLEAR)
                    for col in collections:
                        print(col)
                elif action == '8':
                    ccode = 1
                    break
                else:
                    print('Error: Invalid argument count')
            else:
                if action == '1' and len(args) == 1:
                    collections.append(Collection(name=args[0]))
                    print(f'Info: Successfully added new collection {args[0]}.')

                elif action == '2' and len(args) == 2:
                    col = validate_collection(collections, args[0])
                    if col:
                        if col == collection:
                            collection = None
                            print('Warning: The currently active collection was removed.')
                        collections.remove(col)
                        print('Info: Successfully removed collection.')

                elif action == '3' and len(args) == 2:
                    col = validate_collection(collections, args[0])
                    if col:
                        col.change_name(args[1])
                        print(f'Successfully renamed collection to {args[0]}.')

                elif action == '4':
                    print(CLEAR)
                    fields = 'name'
                    filters = validate_filters(fields, *args)
                    exact, close = _filter(items=collections, filters=filters)
                    print(exact)  # only show exact matches

                elif action == '5':
                    col = validate_collection(collections, args[0])
                    if col:
                        collection = col
                else:
                    print('Error: Invalid argument count')

        except KeyboardInterrupt:
            ccode = 0
            break
    return collection, ccode


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
    ccode = 1  # NOTE core-code (ccode): 0: exit, 1: main_menu, 2: manage_collections

    # Core loop.
    print(INTRODUCTION)
    input('(press enter to start)')
    while True:
        # Main menu
        if ccode == 1:
            if not collection:
                print('Warning: the last selected collection was deleted.')
                if not collections:
                    print('Info: Creating default collection \"Base\"...')
                    collections.append(Collection(name='Base'))
                collection = collections[0]
                print(f'Info: Selected collection {collection.name}.')

            ccode = main_menu(collection)
        # Manage collections menu
        elif ccode == 2:
            collection, ccode = manage_collections_menu(collection, collections)
        # User request exit
        if ccode == 0:
            break

    print('Info: Saving data and exiting...')
    # save data
    data = [collection.save() for collection in collections]
    with file.open(mode='w', encoding="UTF-8") as f:
        yaml.dump(data, f, default_flow_style=False, explicit_start=True)

    # exit
    print('Debug: Program exit.')
