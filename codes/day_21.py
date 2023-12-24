# https://adventofcode.com/2023/day/21

from io import StringIO
from collections import Counter
import pandas as pd
import time

example = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""


def get_test_file() -> str:
    # URL of the text file
    file_path = "inputs/day_21_input.txt"
    with open(file_path, "r") as file:
        # Read the entire content of the file into a string
        file_content = file.read()
        return file_content


def replace_near_position(df: pd.DataFrame, row: int, col: int):
    cell_value = df.iloc[row, col]
    # if we hit a wall, or already expanded to this position, do nothing
    if not cell_value in ["S", "O"]:
        return

    # Define the radius around the position to replace values
    radius = 1

    # Get the row and column indices within the radius
    rows_to_replace = list(
        range(max(0, row - radius), min(df.shape[0], row + radius + 1))
    )
    cols_to_replace = list(
        range(max(0, col - radius), min(df.shape[1], col + radius + 1))
    )

    # Replace values in the selected positions
    for r in rows_to_replace:
        for c in cols_to_replace:
            # we can only move vertically or horizontally
            if r == row or c == col:
                if cell_value == "-":
                    print(f"{row=} {col=} - {r=} {c=}")
                    print(df.to_string(index=False, header=False))
                if not df.iloc[r, c] in ["#", "-"]:
                    df.iloc[r, c] = "-"
    df.iloc[row, col] = "."


def replace_neighbors(current_df: pd.DataFrame) -> pd.DataFrame:
    for row_idx in range(current_df.shape[0]):
        for col_idx in range(current_df.shape[1]):
            replace_near_position(current_df, row_idx, col_idx)

    current_df.replace(to_replace="-", value="O", inplace=True)

    return current_df


def get_next_iteration(current_iteration: str) -> str:
    lines = current_iteration.strip().splitlines()
    matrix_data = [list(line) for line in lines]
    df = pd.DataFrame(matrix_data)

    df = replace_neighbors(df)
    result = df.to_string(index=False, header=False)
    return result.replace(" ", "")


start_time = time.time()
iteration = example
for i in range(6):
    print(i, " ", end="")
    iteration = get_next_iteration(iteration)
char_counts = Counter(iteration)
elapsed_time = time.time() - start_time
print()
print(f"Elapsed time: {elapsed_time} seconds")
print(char_counts["O"])


start_time = time.time()
iteration = get_test_file()
for i in range(64):
    print(i, " ", end="")
    iteration = get_next_iteration(iteration)
char_counts = Counter(iteration)
elapsed_time = time.time() - start_time
print()
print(f"Elapsed time: {elapsed_time} seconds")
print(char_counts["O"])
