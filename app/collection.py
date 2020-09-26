from typing import List, Dict

from app.boardgame import BoardGame
from app.filters import stringify_filter_results, _filter, validate_filters


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
                 times_played: str = None, rating: str = None) -> None:
        check_args = [players, duration, age]
        if times_played:
            check_args.append(times_played)
        if rating:
            check_args.append(rating)

        if any(game.title == title for game in self.games):
            print('Error: This game already exists.')

        elif not all([arg.isdigit() for arg in check_args]):
            print(f'Error: {", ".join(arg for arg in check_args) } must be integers!')

        else:
            game = BoardGame(title, *check_args)
            self.games.append(game)
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
