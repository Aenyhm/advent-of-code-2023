from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from functools import reduce
from multiprocessing.pool import Pool

EXAMPLE = (
    "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
    "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
    "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
    "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
    "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
)


@dataclass
class Turn:
    red: int = 0
    green: int = 0
    blue: int = 0

    def __iter__(self) -> Iterator[str, int]:
        for color, number in self.__dict__.items():
            yield color, number

    def __getitem__(self, color: str) -> int:
        return getattr(self, color)


@dataclass(slots=True)
class Game:
    id: int
    turns: Iterable[Turn]


MAX_COLORS_TURN = Turn(12, 13, 14)


def iter_turn_info(turn_info: str) -> Iterator[str, int]:
    for cube_info in turn_info.split(', '):
        number, color = cube_info.split(' ')
        yield color, int(number)


def parse_turn(turn_info: str) -> Turn:
    return Turn(**dict(iter_turn_info(turn_info)))


def parse_game(game_info: str) -> Game:
    id_part, info_part = game_info.split(': ')

    return Game(
        int(id_part[5:]),
        map(parse_turn, info_part.split('; '))
    )


def get_max_game_id(game: Game) -> int:
    success = all(
        MAX_COLORS_TURN[color] >= number
        for turn in game.turns
        for color, number in turn
    )

    return game.id if success else 0


def part1(games: Iterable[Game], pool: Pool) -> int:
    return sum(pool.map(get_max_game_id, games))


def get_min_turn(t1: Turn, t2: Turn) -> Turn:
    return Turn(**{
        color: max(n1, t2[color])
        for color, n1 in t1
    })


def get_cubes_power(game: Game) -> int:
    min_turn = reduce(get_min_turn, game.turns, Turn())

    return min_turn.red * min_turn.green * min_turn.blue


def part2(games: Iterable[Game], pool: Pool) -> int:
    return sum(pool.map(get_cubes_power, games))


def day2(text: str):
    pool = Pool()

    lines = text.split('\n')
    games = list(pool.map(parse_game, lines))
    example_games = list(pool.map(parse_game, EXAMPLE))

    assert part1(example_games, pool) == 8
    assert part1(games, pool) == 2285

    assert part2(example_games, pool) == 2286
    assert part2(games, pool) == 77021
