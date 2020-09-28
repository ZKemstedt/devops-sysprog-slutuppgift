from typing import List, Dict, Any, Callable, Union, Optional

from app.boardgame import BoardGame, BOARDGAME_FIELD_CHECK
from app.filters import stringify_filter_results, _filter, validate_filters
from app.utils import Whitespace


# -- how to use field checks --
# if field in FIELD_CHECK and FIELD_CHECK[field](value):
#   do stuff...
# eg: try to set field 'name' to 'test'
# if field in FIELD_CHECK and FIELD_CHECK['name']('test'):
#   item._modify('name', 'test')

BOARDGAME_COLLECTION_FIELD_CHECK: Dict[str, Callable[[str], bool]] = {
    'name': lambda x: not x.isdigit()
}


class BaseCollection(object):
    """Base collection class"""

    def __init__(self,
                 name: str,
                 items: List[Any] = [],
                 *,
                 item_fields_check: Dict[str, Callable[[str], bool]] = {},
                 header: str = ''):
        self.items = items
        self.name = name
        self.item_fields_check = item_fields_check
        self.header = header

    def __str__(self) -> str:
        title = Whitespace.big_title(f'Collection: {self.name}')
        text = '\n'.join(f'{i}'.ljust(7) + str(item) for i, item in enumerate(self.items))
        return (title + Whitespace.line + self.header + Whitespace.weak_line + text + Whitespace.line + '\n')

    def save(self) -> Dict:
        """Return a dict representing the Collection's contents"""
        return {
            'name': self.name,
            'items': [item.save() for item in self.items]
        }

    def _modify(self, field: str, value: str):
        setattr(self, field, value)

    def assert_item(self, key: Union[str, Any]) -> Any:
        """
        Make sure we get an item. If `key` is not an item, use get_item(key)


        This method must be immplemented by a child class to specify the type/class to check the instance of.
        """
        raise NotImplementedError

        if isinstance(key, Any):
            if key in self.items:
                return key
            else:
                return None
        else:
            return self.get_item(key)

    def get_item(self, key: str) -> Any:
        """Return the item at index `key` or with the name `key`"""
        if key.isdigit():
            if len(self.items) - 1 >= int(key):
                return self.items[int(key)]
            else:
                print('Error: index out of bounds.')
                return None
        else:
            item = next((item for item in self.items if item.name == key), None)
            if not item:
                print(f'Error: no item with the name `{key}` could be found.')
            return item

    def remove_item(self, item: Union[str, Any]) -> None:
        """Remove an item from the collection."""
        item = self.assert_item(item)
        if item:
            self.items.remove(item)
            print('Info: Successfully removed the item.')

    def add_item(self, item: Any) -> None:
        """Add an item to the collection. No duplicates are accepted."""
        if not any(item.name == i.name for i in self.items):
            self.items.append(item)
            print('Info: Successfully added the item.')
        else:
            print('Info: Item already exists in collection.')

    def edit_item(self, item: Union[str, Any], field: str, value: str) -> None:
        """Set an item's field `field` to `value`"""
        item = self.assert_item(item)
        if item and field in self.item_fields_check and self.item_fields_check[field](value):
            item._modify(field, value)
            print(f'Info: Successfully set {field} to {value} for {item.name}')
        else:
            print('Error: invalid field(s) or value(s).')


class BoardGameCollection(BaseCollection):
    """A manager for a collection of BoardGames"""

    def __init__(self, name: str, items: List[BoardGame] = []):
        # NOTE BOARDGAME_FIELD_CHECK
        super().__init__(name, items, item_fields_check=BOARDGAME_FIELD_CHECK)
        self.header = (''
                       + 'title'.ljust(30)
                       + 'players'.rjust(5)
                       + 'duration'.rjust(10)
                       + 'recommended_age'.rjust(17)
                       + 'times_played'.rjust(14)
                       + 'rating'.rjust(8)
                       + '\n')

    # -- overrides --

    def assert_item(self, key: Union[str, BoardGame]) -> BoardGame:
        """override to set item-instance-type to `BoardGame`"""
        if isinstance(key, BoardGame):
            if key in self.items:
                return key
            return None
        else:
            return self.get_item(key)

    # -- extensions --

    def list_games(self, *filter_args: Optional[List[str, ]]) -> str:
        """
        Return a formatted string displaying the items in the collection.

        If filter_args are given, first show items that match the filter(s).
        Then show items that partially matched the filter(s) below the
        exact results, separated by a line and sorted by relevance.
        """
        if filter_args:
            filters = validate_filters(self.item_fields_check.keys(), *filter_args)
            if filters:
                print(f'Debug (l_g): filters: {filters}')
                return stringify_filter_results(self.header, *_filter(items=self.items, filters=filters))

        # no filter -> show index
        return (Whitespace.clear
                + 'index'.ljust(7) + self.header
                + '\n'.join([f'{str(i).ljust(7)}{str(item)}' for i, item in enumerate(self.items)])
                + '\n')

    def add_game(self, *args) -> None:
        """Crate a BoardGame instance and add it to the collection"""
        fields = list(self.item_fields_check.keys())
        checks = {fields[i]: arg for i, arg in enumerate(args)}
        if all(self.item_fields_check[field](value) for field, value in checks.items()):
            self.add_item(BoardGame(*args))
        else:
            print('Error: Failed to add game, invalid argument type(s).')

    def play_game(self, item: BoardGame) -> None:
        """Register that a game (item) has been played"""
        item = self.assert_item(item)
        if item:
            item.inc_times_played()
            print(f'Info: You played the game, total times played: {item.times_played}')

    # -- shortcuts / aliases --

    def rate_game(self, game: Union[str, BoardGame], rating: str) -> None:
        self.edit_item(game, 'rating', rating)


class CollectionManager(BaseCollection):
    """A manager for a collection of BoardGameCollections"""

    def __init__(self, active: BoardGameCollection = None, items: List[BoardGameCollection] = []):
        # NOTE BOARDGAME_COLLECTION_FIELD_CHECK
        super().__init__('manager', items, item_fields_check=BOARDGAME_COLLECTION_FIELD_CHECK)
        self.active = active
        self.reassure_base()

    # -- overrides --

    def __str__(self) -> str:
        return '\n'.join((str(item) for item in self.items))

    def assert_item(self, key: Union[str, BoardGameCollection]) -> BoardGameCollection:
        """override to set item-instance-type to `BoardGameCollection`"""
        if isinstance(key, BoardGameCollection):
            if key in self.items:
                return key
            else:
                return None
        else:
            return self.get_item(key)

    def remove_item(self, item: Any) -> None:
        """Override to recreate base collection if all collections are deleted."""
        super().remove_item(item)
        self.reassure_base()

    def add_item(self, name: str) -> None:
        """override to make the item object a `BoardGameCollection`"""
        super().add_item(BoardGameCollection(name))

    # -- extensions --

    def reassure_base(self) -> None:
        if not self.items:
            self.items.append(BoardGameCollection('base'))
        if not self.active:
            self.active = self.items[0]

    def select_active(self, item: BoardGameCollection) -> None:
        item = self.assert_item(item)
        if item:
            self.active = item

    # -- shortcuts / aliases --

    def change_collection_name(self, item: Union[str, BoardGameCollection], name: str) -> None:
        self.edit_item(item, 'name', name)
