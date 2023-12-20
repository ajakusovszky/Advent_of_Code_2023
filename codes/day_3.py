# https://adventofcode.com/2023/day/3

from dataclasses import dataclass
import re

example = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


def get_test_file() -> str:
    # URL of the text file
    file_path = "inputs/day_3_input.txt"
    with open(file_path, "r") as file:
        # Read the entire content of the file into a string
        file_content = file.read()
        return file_content


def check_line_for_symbol(
    lines: list[str], index: int, check_start: int, check_end: int
) -> bool:
    """Checks if the line has any symbol between start-1 and end+1"""
    pattern = re.compile(r"[^\d\.]+")
    matches = pattern.finditer(lines[index])
    # Extract start and end positions for each match
    symbol_positions = [
        (match.start(), match.end(), match.group()) for match in matches
    ]
    for start, end, _ in symbol_positions:
        if start >= check_start - 1 and end <= check_end + 1:
            return True
    return False


def check_line_for_number(lines: list[str], index: int) -> int:
    """Gets a line index, where it checks that are there any symbols near the group of numbers in it.
    Adds them together"""
    result = 0
    pattern = re.compile(r"\d+")
    matches = pattern.finditer(lines[index])
    # Extract start and end positions for each match
    number_positions = [
        (match.start(), match.end(), match.group()) for match in matches
    ]
    for start, end, number in number_positions:
        if (
            check_line_for_symbol(lines, index, start, end)
            or (index > 0 and check_line_for_symbol(lines, index - 1, start, end))
            or (
                index < len(lines) - 1
                and check_line_for_symbol(lines, index + 1, start, end)
            )
        ):
            result += int(number)
    return result


def first_task(input: list[str]) -> int:
    result = 0
    lines = input.splitlines()

    for index, _ in enumerate(lines):
        result += check_line_for_number(lines, index)
    return result


print(first_task(example))
print(first_task(get_test_file()))


# part 2
# Find the * characters near the numbers. I will make a collection of numbers and the neighbour * characters with coordinates.


@dataclass(frozen=True)
class star_position:
    x: int
    y: int
    star: str


def scan_for_stars(input: str) -> list[star_position]:
    result = []
    lines = input.splitlines()
    pattern = re.compile(r"\*+")
    for index, line in enumerate(lines):
        matches = pattern.finditer(line)
        # Extract start and end positions for each match
        number_positions = [
            (match.start(), match.end(), match.group()) for match in matches
        ]
        for start, end, symbols in number_positions:
            if start != end - 1:
                print(index, start, symbols)
            result.append(star_position(index, start, symbols))
    return result


def get_numbers_around_star(star: star_position, input: str) -> list[int]:
    result = []
    lines = input.splitlines()
    # just need the previous, the line where the * is and the next line
    lines = lines[star.x - 1 : star.x + 2]
    # print(star)
    # print(lines)
    pattern = re.compile(r"\d+")
    for line in lines:
        matches = pattern.finditer(line)
        # Extract start and end positions for each match
        number_positions = [
            (match.start(), match.end(), match.group()) for match in matches
        ]
        for start, end, numbers in number_positions:
            # the trick here was to finetune the limits
            if star.y >= start - 1 and star.y <= end:
                result.append(int(numbers))
    return result


def second_task(input: str) -> int:
    result = 0
    stars = scan_for_stars(input)
    # lets check that how many numbers are near these stars
    for star in stars:
        numbers_list = get_numbers_around_star(star, input)
        print(star, len(numbers_list), numbers_list)
        if len(numbers_list) == 2:
            result += numbers_list[0] * numbers_list[1]
    return result


print(second_task(example))
print(second_task(get_test_file()))
