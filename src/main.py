from src.day1 import day1
from src.day2 import day2


def get_input(day: int) -> str:
    return open(f"data/2023/input{day}.txt", encoding="utf-8").read()[:-1]


def main():
    day1(get_input(1))
    day2(get_input(2))


if __name__ == '__main__':
    main()
