import re
from collections import OrderedDict

EXAMPLES = [
    (["1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet"], False, 142),
    (["two1nine", "eightwothree", "abcone2threexyz", "xtwone3four", "4nineeightseven2", "zoneight234", "7pqrstsixteen"], True, 281)
]

SPELLED_NUMBERS = (
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
)


def spelled_number_to_digit(s: str) -> int:
    return SPELLED_NUMBERS.index(s) + 1


def get_spelled_indices(line: str) -> dict[int, int]:
    return {
        index.start(): spelled_number_to_digit(spelled_number)
        for spelled_number in SPELLED_NUMBERS
        for index in re.finditer(pattern=spelled_number, string=line)
    }


def get_digits_indices(line: str) -> dict[int, int]:
    return {index: int(char) for index, char in enumerate(line) if char.isdigit()}


def line_to_calibration(line: str, spelled: bool) -> int:
    number_indices = get_digits_indices(line)
    if spelled:
        number_indices |= get_spelled_indices(line)

    numbers = list(OrderedDict(sorted(number_indices.items())).values())

    return int(f"{numbers[0]}{numbers[-1]}")


def run(lines: list[str], spelled: bool) -> int:
    calibrations = map(lambda line: line_to_calibration(line, spelled), lines)

    return sum(calibrations)


def day1(text: str):
    for ex in EXAMPLES:
        assert run(ex[0], ex[1]) == ex[2]

    lines = text.split('\n')

    r1 = run(lines, False)
    assert r1 == 55816

    test = run(["twone"], True)
    assert test == 21

    r2 = run(lines, True)
    assert r2 == 54980
