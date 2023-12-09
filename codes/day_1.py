# https://adventofcode.com/2023/day/1

# The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

# For example:

# 1abc2
# pqr3stu8vwx
# a1b2c3d4e5f
# treb7uchet
# In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

import re


def get_test_file() -> str:
    # URL of the text file
    file_path = "inputs/day_1_input.txt"
    with open(file_path, "r") as file:
        # Read the entire content of the file into a string
        file_content = file.read()
        return file_content


def get_example() -> str:
    return """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""


word_to_number = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def get_number(word: str) -> int:
    if word is None or word == "":
        raise ValueError
    if word.isdigit():
        return int(word)
    else:
        return word_to_number[word]


def get_1():
    content = get_test_file()
    rolling_sum = 0
    for line in content.splitlines():
        # Use regular expressions to find all numbers in the string
        numbers = re.findall(r"\d", line)
        # print(f"{line:<50} {int(numbers[0])} {int(numbers[-1])}")
        rolling_sum += int(numbers[0]) * 10 + int(numbers[-1])
    return rolling_sum


def get_1_2():
    content = get_test_file()
    rolling_sum = 0
    with open("inputs/day_1_2_output.csv", "w") as file:
        file.write(f"line;word_0;word_1;num_0;num_1;sum;rolling_sum\n")
        for line in content.splitlines():
            first_word = ""
            last_word = ""
            # Create a regular expression pattern that matches any of the words
            word_pattern = (
                r"(?:\d|"
                + "|".join(re.escape(word) for word in word_to_number.keys())
                + r")"
            )
            words = re.findall(word_pattern, line)
            if words:
                first_word = words[0]

            # start from backward
            word_pattern = (
                r"(?:\d|"
                + "|".join(re.escape(word[::-1]) for word in word_to_number.keys())
                + r")"
            )
            newvals: dict = {}
            # update the dictonary too
            for key in word_to_number.keys():
                newvals[key[::-1]] = word_to_number[key]
            word_to_number.update(newvals)

            words = re.findall(word_pattern, line[::-1])
            last_word = words[0]

            # # Use re.finditer() with reverse search to find all words that represent numbers in the string
            # words = [match.group() for match in re.finditer(word_pattern, line)]
            # last_word = words[-1]

            # if line == "8seventwooneightfcj":
            print(line, first_word, last_word)

            rolling_sum += get_number(first_word) * 10 + get_number(last_word)
            file.write(
                f"{line};{first_word};{last_word};{get_number(first_word)};{get_number(last_word)};{get_number(first_word) * 10 + get_number(last_word)};{rolling_sum}\n"
            )
    return rolling_sum


print(f"1. {get_1()}")
print(f"2. {get_1_2()}")
