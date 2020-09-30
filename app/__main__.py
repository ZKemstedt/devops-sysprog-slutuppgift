import yaml
import logging
from typing import Optional, List, Tuple, Union, Callable
from pathlib import Path

from app.collections import CollectionManager, BoardGameCollection
from app.boardgame import BoardGame
from app.menus import GameMenu, Menu
from app.utils import str_sized
from app.utils import Whitespace

log = logging.getLogger(__name__)

FILENAME = 'boardgamecollections.yml'
FILEDIR = 'collectiondata'

INTRODUCTION = """
  Boardgame Collection Manager
  (Boardgames sold separately)

  All arguments to commands should be separated by spaces,
  If you want multi-worded names or the like, use
  dashes (-) in place of spaces. eg: Zephyro-Kemstedt-the-almighty

  Made by Zephyro @ https://github.com/ZKemstedt/devops-sysprog-slutuppgift
  """


def excecute_action(func: Callable, args: List[Union[CollectionManager, str]]) -> Optional[Union[Menu, str, int, None]]:
    try:
        return func(*args)
    except TypeError:
        print('Invalid argument count')
        return None


def get_user_input(menu: Menu, manager: CollectionManager) -> Tuple[str, List[str]]:
    prompt = (f'[c:{str_sized(manager.active.name, 25, "...")}]'
              f'[m:{str_sized(menu.name.lower(), 25, "...")}]'
              ' >> ')
    try:
        args = list(input(f'{prompt}').lower().strip().split())
        log.trace(f'(get_user_input) user >> {args}')
    except KeyboardInterrupt:
        return 0, 0
    if len(args) == 0:
        return 0, 0
    else:
        action = args.pop(0)
        args.insert(0, manager)
        log.trace(f'(get_user_input) -> ({action}, {args})')
        return (action, args)


def main(menu: Menu, manager: CollectionManager) -> None:
    while True:
        action, args = get_user_input(menu, manager)
        if action in menu.choices:
            ret = excecute_action(menu.choices[action], args)
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


def get_menu() -> Menu:
    menu = GameMenu()
    print(Whitespace.clear)
    print(menu.title)
    print(menu.instructions)
    return menu


def get_manager(p: Path) -> CollectionManager:
    with p.open(encoding='utf-8') as f:
        data = yaml.safe_load(f)
    if 'name' in data and 'items' in data and data['name'] == 'manager':
        try:
            manager = CollectionManager(active=None, items=                             # noqa E251
                [BoardGameCollection(name=collection['name'],items=                     # noqa E251
                    [BoardGame(*args) for args in collection['items']]                  # noqa E128
                ) for collection in data['items']]
            )
        except Exception as e:
            log.error('Error when reading file', exc_info=e)
        else:
            log.info(f'Loaded {len(manager.items)} collections from file.')
            return manager
    manager = CollectionManager(active=None, items=[])
    log.warning('Could not read data from file')
    return manager


def save_manager(p: Path, m: CollectionManager) -> None:
    with p.open(mode='w', encoding="UTF-8") as f:
        yaml.dump(manager.save(), f, default_flow_style=False, explicit_start=True)


if __name__ == "__main__":
    print(Whitespace.clear)
    log.info('Program start.')
    print(INTRODUCTION)

    file = Path(FILEDIR, FILENAME)
    manager = get_manager(file)
    try:
        input('(press enter to start)')
        menu = get_menu()
        main(menu, manager)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        log.critical('Unhandled error! the program will exit.', exc_info=e)
    finally:
        log.info('Saving data and exiting...')
        save_manager(file, manager)
        log.info('Program exit.')
