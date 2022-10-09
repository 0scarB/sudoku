#!.venv/bin/python

from __future__ import annotations

import csv
import math
import time
from dataclasses import dataclass
import sys
from typing import TypeAlias, Iterable

from src import solve, to_display_str


def test() -> None:
    print_monitor_every_n_solves = 1000

    args = sys.argv
    if len(args) > 1:
        data_set_limit = int(args[1])
    else:
        data_set_limit = math.inf

    total_count: int = 0
    total_solve_duration = 0
    max_solve_duration = 0
    failed: list[DataSetEntry] = []

    def print_monitoring() -> None:
        avg_solve_duration = total_solve_duration / total_count
        print(f"Solved {total_count} sudoku.")
        print(f"Avg. solve time = {avg_solve_duration * 1000:.2f}ms")
        print(f"Worst solve time = {max_solve_duration * 1000:.2f}ms")

    try:
        for i, entry in enumerate(collect_data_set()):
            if i >= data_set_limit:
                break

            t0 = time.perf_counter()
            solution = solve(entry.unsolved)
            t1 = time.perf_counter()

            solve_duration = t1 - t0
            total_solve_duration += solve_duration
            if solve_duration > max_solve_duration:
                max_solve_duration = solve_duration

            if solution != entry.solution:
                failed.append(entry)

            total_count += 1

            if i % print_monitor_every_n_solves == print_monitor_every_n_solves - 1:
                print_monitoring()

        failed_count = len(failed)
        solved_count = total_count - failed_count

        if solved_count == total_count:
            print()
            print_monitoring()
            print(f"Total solve time = {total_solve_duration:.2f}s")
            print("Success!!!")
            return

        solved_percent = round(solved_count / total_count * 100, ndigits=2)
        failed_percent = round(failed_count / total_count * 100, ndigits=2)

        print(f"{solved_percent}% solved\n{failed_percent}% failed\n")
    except KeyboardInterrupt:
        print("\nTerminated before test could finish. Exiting!")
        return

    try:
        for failed_entry in failed:
            if input("Show next failure? [N/y] ") not in {"Y", "y"}:
                print("Exiting!")
                return

            print()
            print_data_set_entry(failed_entry)
            print()

        print("All failed entries have been viewed. Exiting!")
    except KeyboardInterrupt:
        print("\nExiting!")
        return


def print_data_set_entry(entry: DataSetEntry) -> None:
    gap = " " * 5

    unsolved_lines = to_display_str(entry.unsolved).split("\n")
    solution_lines = to_display_str(entry.solution).split("\n")

    left_width = max(len(line) for line in unsolved_lines)

    print(f"{'Unsolved':<{left_width}}{gap}Solution")
    for left, right in zip(unsolved_lines, solution_lines):
        print(f"{left:<{left_width}}{gap}{right}")


def collect_data_set() -> DataSet:
    with open("data_set.csv", newline="") as f:
        for row in csv.DictReader(f):
            yield DataSetEntry(
                unsolved=row["unsolved"],
                solution=row["solution"]
            )


@dataclass(frozen=True)
class DataSetEntry:
    unsolved: str
    solution: str


DataSet: TypeAlias = Iterable[DataSetEntry]


if __name__ == "__main__":
    test()
