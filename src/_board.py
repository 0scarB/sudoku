from __future__ import annotations

from typing import Iterable

from ._types import Cell


class Board:
    __slots__ = ("_cells_to_possibilities",)

    _cells_to_possibilities: dict[Cell, set[int]]

    @classmethod
    def from_str(cls, sudoku: str) -> Board:
        all_possibilities = set(range(1, 10))
        cells_to_possibilities = {
            (row, col): set(all_possibilities)
            for row in range(9)
            for col in range(9)
        }

        for line_start in range(0, 9*9, 9):
            line_end = line_start + 9
            line = [int(char) for char in sudoku[line_start:line_end]]

            row = line_start // 9
            for col, num in enumerate(line):
                if num != 0:
                    cells_to_possibilities[(row, col)] = {num}

        return cls(cells_to_possibilities)

    def __init__(self, cells_to_possibilities: dict[Cell, set[int]]) -> None:
        self._cells_to_possibilities = cells_to_possibilities

    def to_str(self) -> str:
        chars: list[str] = []
        for row in range(9):
            for col in range(9):
                cell = (row, col)
                char = (
                    str(self.cell_solution(cell))
                    if len(self._cells_to_possibilities[cell]) == 1
                    else "0"
                )
                chars.append(char)

        return "".join(chars)

    def remove_possibility(self, cell: Cell, possibility: int) -> int:
        possibilities = self._cells_to_possibilities[cell]

        try:
            possibilities.remove(possibility)
        except KeyError:
            return -1

        cell_is_solved = len(possibilities) == 1

        if not cell_is_solved:
            return -1

        return self.cell_solution(cell)

    def solved_cells(self) -> Iterable[Cell]:
        return (
            cell
            for cell, possibilities in self._cells_to_possibilities.items()
            if len(possibilities) == 1
        )

    def cell_solution(self, cell: Cell) -> int:
        possibilities = self._cells_to_possibilities[cell]
        solution = possibilities.pop()
        possibilities.add(solution)

        return solution

    def unsolved_cells_ordered_by_least_possibilities(self) -> Iterable[Cell]:
        return sorted(
            (
                cell
                for cell, possibilities in self._cells_to_possibilities.items()
                if len(possibilities) > 1
            ),
            key=lambda cell: len(self._cells_to_possibilities[cell])
        )

    def is_solved(self) -> bool:
        return all(
            len(possibilities) == 1
            for possibilities in self._cells_to_possibilities.values()
        )

    def copy(self) -> Board:
        return Board({
            cell: set(possibilities)
            for cell, possibilities in self._cells_to_possibilities.items()
        })

    def cell_possibilities(self, cell: Cell) -> set[int]:
        return self._cells_to_possibilities[cell]

    def set_sell_possibilities(self, cell: Cell, possibilities: set[int]) -> None:
        self._cells_to_possibilities[cell] = possibilities
