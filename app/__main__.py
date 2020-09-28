import yaml
from typing import Optional, List
from pathlib import Path

from app.collections import CollectionManager, BoardGameCollection
from app.boardgame import BoardGame
from app.menus import GameMenu, Menu
from app.utils import str_sized
from app.utils import Whitespace


INTRODUCTION = """
  Boardgame Collection Manager
  (Boardgames sold separately)

  All arguments to commands should be separated by spaces,
  If you want multi-worded names or the like, use
  dashes (-) in place of spaces. eg: Zephyro-Kemstedt-the-almighty

  Made by Zephyro @ https://github.com/ZKemstedt/devops-sysprog-slutuppgift
  """


def user_input(text: Optional[str] = '', prompt: Optional[str] = '') -> List[str, ]:
    if prompt:
        prompt = prompt.strip()
    return list(input(f'{text}{prompt} >> ').strip().lower().split(' '))


def main(manager: CollectionManager) -> None:
    """Main Menu loop"""
    print(Whitespace.clear)

    # Start at main menu
    menu = GameMenu
    print(menu.title)
    print(menu.instructions)

    while True:
        ret = None
        func = None

        # get user input
        try:
            prompt_text = (f'[c:{str_sized(manager.active.name, 25, "...")}]'
                           f'[m:{str_sized(menu.name.lower(), 25, "...")}]')
            args = user_input(prompt_text)
        except KeyboardInterrupt:
            return

        # execute action
        action = args.pop(0)
        if action in menu.choices:
            func = menu.choices[action]  # aquire the function to call
            args.insert(0, manager)  # manager instance must always be the first argument
            # try:
            ret = func(*args)  # call the function

            # TypeError: a function received too few or too many arguments
            # except (TypeError) as e:
            #     print('Error: Invalid argument count')
            #     print(f'Debug: {type(e)}')
            #     print(f'Debug: {e}')

            # follow up on any returned values
            if isinstance(ret, int):
                return
            elif isinstance(ret, str):
                print(ret)
            elif issubclass(ret.__class__, Menu):
                menu = ret
                print(Whitespace.clear)
                print(menu.title)
                print(menu.instructions)

        elif not action:
            print('Tips: type ? for help, 0 to exit')
        else:
            print('Error: Invalid command.')


if __name__ == "__main__":
    # program start
    print(Whitespace.clear)
    print('Debug: Program start.')

    # --- load data ---
    file = Path('collectiondata', 'boardgamecollections.yml')
    with file.open(encoding="UTF-8") as f:
        data = yaml.safe_load(f)
    collections = []
    # saved manager?
    if 'name' in data and 'items' in data and data['name'] == 'manager':
        # Convert data to Collection and BoardGame objects
        for collection in data['items']:
            boardgames = [BoardGame(*args) for args in collection['items']]
            collections.append(BoardGameCollection(name=collection['name'], items=boardgames))
        if collections:
            print(f'Info: Loaded {len(collections)} collections from file.')
    else:
        print('Warning: Could not read data from file')

    # cleanup
    del data

    # --- main ---
    print(INTRODUCTION)
    try:
        input('(press enter to start)')
    except Exception:
        pass
    else:
        # try:
        manager = CollectionManager(active=None, items=collections)
        main(manager)
        # except Exception as e:
        #     print('Critical: Unhandled error!')
        #     print(f'Critical: Type: {type(e)}')
        #     print(f'Critical: Message: {e}')
        # finally:

        # --- save data ---
        print('Info: Saving data and exiting...')

        data = manager.save()
        with file.open(mode='w', encoding="UTF-8") as f:
            yaml.dump(data, f, default_flow_style=False, explicit_start=True)
    # exit
    print('Debug: Program exit.')
