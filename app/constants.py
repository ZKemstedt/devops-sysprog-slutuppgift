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


MANAGE_COLLECTIONS_INSTRUCTIONS = """
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
