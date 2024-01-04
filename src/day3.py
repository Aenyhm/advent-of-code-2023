import re
from dataclasses import dataclass
from multiprocessing.pool import Pool

from src import get_file_content


@dataclass(slots=True)
class NumberMatch:
    start_pos: int
    end_pos: int
    value: int


def file_to_list(file_name: str) -> list[str]:
    return get_file_content(file_name).split("\n")


def get_line_numbers_matches(line: str) -> list[NumberMatch]:
    return [
        NumberMatch(match.start(), match.end(), int(match[0]))
        for match in re.finditer(r"\d+", string=line)
    ]


def has_relative_line_symbol(match: NumberMatch, relative_line: str) -> bool:
    chars = relative_line[
        max(match.start_pos - 1, 0) : min(match.end_pos + 1, len(relative_line))
    ]

    return bool(chars.replace(".", ""))


def find_adjacent_symbols(match: NumberMatch, index: int, lines: list[str]) -> bool:
    current_line = lines[index]

    return (
        # Previous character
        match.start_pos > 0
        and current_line[match.start_pos - 1] != "."
        or
        # Next character
        match.end_pos < len(current_line)
        and current_line[match.end_pos] != "."
        or
        # Previous line
        index > 0
        and has_relative_line_symbol(match, lines[index - 1])
        or
        # Next line
        index < len(lines) - 1
        and has_relative_line_symbol(match, lines[index + 1])
    )


def part1(lines: list[str], pool: Pool) -> int:
    number_matches = pool.map(get_line_numbers_matches, lines)

    return sum(
        match.value
        for index, line_number_matches in enumerate(number_matches)
        for match in line_number_matches
        if find_adjacent_symbols(match, index, lines)
    )


def day3() -> None:
    pool = Pool()

    input_content = file_to_list("input3")
    example_content = file_to_list("example3")

    assert part1(example_content, pool) == 4361
    assert part1(input_content, pool) == 544433
