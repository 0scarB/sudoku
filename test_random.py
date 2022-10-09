#!.venv/bin/python

from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from typing import TypeAlias, Iterable

from src import solve, to_side_by_side_display_str


def test() -> None:
    data_set = list(collect_data_set())
    entry = data_set[random.randint(0, len(data_set) - 1)]
    unsolved = entry.unsolved
    expected = entry.solution

    actual = solve(unsolved)

    assert expected == actual

    print("Success!!!")
    print(
        to_side_by_side_display_str(
            unsolved,
            expected,
            actual,
            labels=["Unsolved Solution", "Expected Solution", "Actual Solution"]
        )
    )


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
