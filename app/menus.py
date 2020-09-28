# flake8: noqa

from typing import Dict, Callable

from app.utils import Whitespace

#  NOTE ALWAYS pass the instance of `CollectionManager` as the first argument to menus' lambda-functions


class Menu(object):
    name: str
    title: str
    instructions: str
    choices: Dict[str, Callable]


class GameMenu(Menu):
    name = 'Main Menu'
    title = Whitespace.big_title(name)
    instructions = """
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
    choices = {
            # action    arguments               execution                                     # return value
            '1': lambda m, *args:               m.active.add_game(*args),                     # None
            '2': lambda m, key:                 m.active.remove_item(key),                    # None
            '3': lambda m, key, field, value:   m.active.edit_game(key, field, value),        # None
            '4': lambda m, *args:               m.active.list_games(*args),                   # str
            '5': lambda m, key, value:          m.active.edit_game(key, 'rating', value),     # None
            '6': lambda m, key:                 m.active.play_game(key),                      # None
            # - - - - - - - - - - - - - - - - -
            '8': lambda m:                      CollectionMenu(),                             # Menu derived object
            '?': lambda m:                      GameMenu.instructions,                        # str
            '0': lambda m:                      0,                                            # int
        }


class CollectionMenu(object):
    name = 'Manage Collections'
    title = Whitespace.big_title(name)
    instructions = """
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
    choices = {
            # action    arguments               execution                                     # return value
            '1': lambda m, name:                m.add_item(name),                             # None
            '2': lambda m, key:                 m.remove_item(key),                           # None
            '3': lambda m, key, name:           m.edit_item(key, 'name', name),               # None
            '4': lambda m:                      str(m),                                       # str
            '5': lambda m, key:                 m.select_active(key),                         # None
            # - - - - - - - - - - - - - - - - -
            '8': lambda m:                      GameMenu(),                                   # Menu derived object
            '?': lambda m:                      CollectionMenu.instructions,                  # str
            '0': lambda m:                      0,                                            # int
        }
