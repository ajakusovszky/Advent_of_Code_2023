# https://adventofcode.com/2023/day/2

from pprint import pprint
import re

pool = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

example = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""


def get_test_file() -> str:
    # URL of the text file
    file_path = "inputs/day_2_input.txt"
    with open(file_path, "r") as file:
        # Read the entire content of the file into a string
        file_content = file.read()
        return file_content


def extract_game_data(text):
    # Regular expression pattern to match game number, color, and quantity pairs
    pattern = re.compile(r"Game (\d+):")
    matches = pattern.findall(text)
    game_number = int(matches[0])

    pattern = re.compile(r"(\d+)\s*([a-zA-Z]+)")
    matches = pattern.findall(text)

    # Initialize variables to store game number and color-quantity pairs
    game_data_list = []
    color_quantity_pairs = []
    game_data_list.append({game_number: color_quantity_pairs})

    # Process matches
    for quantity, color in matches:
        color_quantity_pairs.append((color, int(quantity)))

    return game_data_list


def get_items(items: str):
    result = []
    for line in items.splitlines():
        if line:
            result.extend(extract_game_data(line))
    return result


def get_2_iter(pool, items):
    for item in items:
        for game_number, color_quantity_pairs in item.items():
            possible: bool = True
            for key, value in color_quantity_pairs:
                if pool[key] < value:
                    # print(f"{key}: {pool[key]=} > {value=}")
                    # print(game_number, color_quantity_pairs)
                    possible = False
                    break
            if possible:
                yield game_number


def get_2() -> int:
    possible_sum = 0
    for i in get_2_iter(pool=pool, items=get_items(get_test_file())):
        possible_sum += i
    return possible_sum


def get_2_2():
    game_data_list = []

    # for item in get_items(example):
    for item in get_items(get_test_file()):
        for game_number, colors in item.items():
            color_quantity_pairs = {}
            game_data_list.append({game_number: color_quantity_pairs})
            for key, value in colors:
                color_quantity_pairs[key] = max(
                    color_quantity_pairs.get(key, 0), int(value)
                )
    pprint(game_data_list)
    powers = [
        product
        for item in game_data_list
        for _, color_dict in item.items()
        for product in [eval("*".join(map(str, color_dict.values())))]
    ]
    print(powers)
    return sum(powers)


print(get_2())
print(get_2_2())
