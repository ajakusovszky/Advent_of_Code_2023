# https://adventofcode.com/2023/day/4

from dataclasses import dataclass
import re

example = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


def get_test_file() -> str:
    # URL of the text file
    file_path = "inputs/day_4_input.txt"
    with open(file_path, "r") as file:
        # Read the entire content of the file into a string
        file_content = file.read()
        return file_content


def get_line_value(line: str) -> int:
    result = 0

    pattern = re.compile(r"Card *(\d+):([\s\d]+) *\|([\s\d]+)")
    matches = pattern.findall(line)
    # print(len(matches), line, matches)
    card_no, winning_numbers, numbers_you_have = matches[0]
    win_set = [int(i) for i in winning_numbers.split()]
    number_set = [int(i) for i in numbers_you_have.split()]

    common_elements = set(win_set).intersection(set(number_set))
    # Count the number of common elements
    count_common_elements = len(common_elements)
    if count_common_elements > 0:
        result = 1 << (count_common_elements - 1)

    # print(common_elements, count_common_elements, result)
    return result


def first_task(input: str) -> int:
    result = 0
    lines = input.splitlines()
    for line in lines:
        result += get_line_value(line)
    return result


print(first_task(example))
print(first_task(get_test_file()))


#                                 Total
#         1	2	4	8	14	1	30
#         1	1+1	1+2+1	1+2+4+1	1+4+8+1
# Matches	Cards	1	2	3	4	5	6
# 4	1	*	1	1	1	1
# 2	2		*	2	2
# 2	3			*	4	4
# 1	4				*	8
# 0	5					*
# 0	6						*


def get_line_scratchcards(line: str, scratchcards: dict[int, int]) -> int:
    result = 0

    pattern = re.compile(r"Card *(\d+):([\s\d]+) *\|([\s\d]+)")
    matches = pattern.findall(line)
    # print(len(matches), line, matches)
    card_no, winning_numbers, numbers_you_have = matches[0]
    card_no = int(card_no)
    win_set = [int(i) for i in winning_numbers.split()]
    number_set = [int(i) for i in numbers_you_have.split()]

    common_elements = set(win_set).intersection(set(number_set))
    # Count the number of common elements
    count_common_elements = len(common_elements)

    scratchcards[card_no] = scratchcards.get(card_no, 0) + 1
    for i in range(count_common_elements):
        scratchcards[card_no + 1 + i] = scratchcards[card_no] + scratchcards.get(
            card_no + 1 + i, 0
        )

    # print(card_no, ":", count_common_elements, scratchcards)
    return result


def second_task(input: str) -> int:
    result = 0
    scratchcards = {}
    for line in input.splitlines():
        result += get_line_scratchcards(line, scratchcards)
    for y in scratchcards.values():
        result += y
    return result


print(second_task(example))
print(second_task(get_test_file()))
