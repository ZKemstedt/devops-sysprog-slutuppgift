import yaml
from typing import List, Tuple, Optional
from pathlib import Path

from app.collection import Collection
from app.boardgame import BoardGame
from app.constants import MAIN_MENU_INSTRUCTIONS, MANAGE_COLLECTIONS_INSTRUCTIONS, CLEAR, INTRODUCTION


def user_input(prompt: Optional[str] = '') -> Tuple[str, ]:
    if prompt:
        prompt = prompt.strip() + ' '
    return input(f'{prompt}>> ').strip().lower().split(' ')


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


def main(col: Collection, cols: List[Collection]) -> None:
    """Main Menu loop

    Args:
        col (Collection): The currently selected instance of `Collection`.
        cols: (List[Collection]) The currently registered collections.
    """
    # NOTE see MAIN_MENU_INSTRUCTIONS and MANAGE_COLLECTIONS_INSTRUCTIONS
    MAIN_MENU = {
        '1': lambda *args: col.add_game(*args),
        '2': lambda key: col.remove_game(col.get_game(key)),
        '3': lambda key, field, value: col.edit_game(col.get_game(key), field, value),
        '4': lambda x: col.list_games(),
        '5': lambda key, rating: col.rate_game(col.get_game(key), rating),
        '6': lambda key: col.play_game(col.get_game(key)),
        '7': lambda *args: col.list_games(*args),
        '8': lambda x: MANAGE_COLLECTIONS,
        '?': lambda x: MAIN_MENU_INSTRUCTIONS,
        '0': lambda x: 0,
        # "secret", not harmful
        'title': lambda x: big_title('Main Menu'),
        'name': lambda x: 'main',
    }

    MANAGE_COLLECTIONS = {
        '1': lambda name: cols.append(Collection(name)
                                      if not any(c.name == name for c in cols)
                                      else 'Error: a collection with that name already exists'),
        '2': lambda key: cols.remove(get_collection(cols, key)) if get_collection(cols, key) else None,
        '3': lambda key, name: get_collection(cols, key).change_name(name) if get_collection(cols, key) else None,
        '4': lambda x: CLEAR + '\n'.join([str(c) for c in cols]),
        '5': lambda key: get_collection(cols, key),
        '8': lambda x: MAIN_MENU,
        '?': lambda x: MANAGE_COLLECTIONS_INSTRUCTIONS,
        '0': lambda x: 0,
        # "secret", not harmful
        'title': lambda x: big_title('Manage Collections'),
        'name': lambda x: 'cols',
    }
    print(CLEAR)

    # Start at main menu
    menu = MAIN_MENU
    print(menu['title'](None))
    print(menu['?'](None))

    while True:
        ret = None

        # get user input
        if col:
            col_prompt = col.name if len(col.name) <= 15 else col.name[:13] + '...'
        else:
            col_prompt = ('< no collection >')
        try:
            menu_name = menu["name"](None)
            args = user_input(f'(col: {col_prompt}) [m:{menu_name}]')
        except KeyboardInterrupt:
            return 0
        action = args.pop(0)

        # act on user input
        if action in menu:
            try:
                if args:
                    ret = menu[action](*args)
                else:
                    # lambda functions always take at least 1 argument.
                    ret = menu[action](None)
                # print(f'Debug: type(ret): {type(ret)}')
                # print(f'Debug: value(ret): {ret}')

            # TypeError: a function that required x arguments received < x arguments
            # AttributeError: a function that required 1 argument did not receive that
            #                 argument -> gets called with argument: `None`
            except (TypeError, AttributeError) as e:
                print('Error: Invalid argument count')
                print(f'Debug: {type(e)}')
                print(f'Debug: {e}')

            # follow up action (if not None)
            if isinstance(ret, int):
                return
            elif isinstance(ret, str):
                print(ret)
            elif isinstance(ret, Collection):
                col = ret
            elif isinstance(ret, dict):
                menu = ret
                print(CLEAR)
                print(menu['title'](None))
                print(menu['?'](None))

        elif not action:
            print('Tips: type ? for help, 0 to exit')
        else:
            print('Error: Invalid command.')


if __name__ == "__main__":
    # program start
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
        collections.append(Collection(name='base'))
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
