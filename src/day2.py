from dataclasses import dataclass
from functools import reduce
from multiprocessing.pool import Pool
from typing import TYPE_CHECKING, Self

from src import get_file_content

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator


@dataclass
class Turn:
    red: int = 0
    green: int = 0
    blue: int = 0

    def __iter__(self: Self) -> "Iterator[str, int]":
        yield from self.__dict__.items()

    def __getitem__(self: Self, color: str) -> int:
        return getattr(self, color)


@dataclass(slots=True)
class Game:
    gid: int
    turns: "Iterable[Turn]"


MAX_COLORS_TURN = Turn(12, 13, 14)


def iter_turn_info(turn_info: str) -> "Iterator[str, int]":
    for cube_info in turn_info.split(", "):
        number, color = cube_info.split(" ")
        yield color, int(number)


def parse_turn(turn_info: str) -> Turn:
    return Turn(**dict(iter_turn_info(turn_info)))


def parse_game(game_info: str) -> Game:
    id_part, info_part = game_info.split(": ")

    return Game(
        int(id_part[5:]),
        map(parse_turn, info_part.split("; ")),
    )


def file_to_games(file_name: str, pool: Pool) -> list[Game]:
    content = get_file_content(file_name)

    return list(pool.map(parse_game, content.split("\n")))


def get_max_game_id(game: Game) -> int:
    success = all(
        MAX_COLORS_TURN[color] >= number
        for turn in game.turns
        for color, number in turn
    )

    return game.gid if success else 0


def get_min_turn(t1: Turn, t2: Turn) -> Turn:
    return Turn(**{color: max(n1, t2[color]) for color, n1 in t1})


def get_cubes_power(game: Game) -> int:
    min_turn = reduce(get_min_turn, game.turns, Turn())

    return min_turn.red * min_turn.green * min_turn.blue


def part1(games: "Iterable[Game]", pool: Pool) -> int:
    return sum(pool.map(get_max_game_id, games))


def part2(games: "Iterable[Game]", pool: Pool) -> int:
    return sum(pool.map(get_cubes_power, games))


def day2() -> None:
    pool = Pool()

    games = file_to_games("input2", pool)
    example_games = file_to_games("example2", pool)

    assert part1(example_games, pool) == 8
    assert part1(games, pool) == 2285

    assert part2(example_games, pool) == 2286
    assert part2(games, pool) == 77021
