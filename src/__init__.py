from __future__ import annotations

from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import TypeAlias, NoReturn, Iterable

from ._board import Board as _Board
from ._groups import get_cells_sharing_possibilities
from ._types import Cell as _Cell


def solve(sudoku: Sudoku) -> Sudoku:
    sudoku = normalize(sudoku)

    unsolved_board = _Board.from_str(sudoku)
    solved_board = _solve_board(unsolved_board)

    return solved_board.to_str()


def _solve_board(board: _Board) -> _Board | NoReturn:
    initial_solved_cells: list[tuple[_Cell, int]] = []
    for solved_cell in board.solved_cells():
        initial_solved_cells.append((solved_cell, board.cell_solution(solved_cell)))
    initial_solved_cells_count = len(initial_solved_cells)
    board_states: PriorityQueue[tuple[int, _BoardState]] = PriorityQueue()
    board_states.put((
        -initial_solved_cells_count,
        _BoardState(
            board=board,
            solved_cells_from_last_iter=initial_solved_cells,
        )
    ))

    while board_states:
        _, board_state = board_states.get()
        board = board_state.board
        solved_cells: list[tuple[_Cell, int]] = []
        for solved_cell, cell_solution in board_state.solved_cells_from_last_iter:
            sharing_cells = get_cells_sharing_possibilities(solved_cell)
            for sharing_cell in sharing_cells:
                sharing_cell_solution = board.remove_possibility(sharing_cell, cell_solution)

                if sharing_cell_solution != -1:
                    solved_cells.append((sharing_cell, sharing_cell_solution))

        if solved_cells:
            if board.is_solved():
                return board

            board_state.solved_cells_from_last_iter = solved_cells
            board_states.put((-len(solved_cells), board_state))
        else:
            for cell in board.unsolved_cells_ordered_by_least_possibilities():
                for possibility in board.cell_possibilities(cell):
                    new_board = board.copy()
                    new_board.set_sell_possibilities(cell, {possibility})

                    board_states.put((
                        -1,
                        _BoardState(
                            board=new_board,
                            solved_cells_from_last_iter=[(cell, possibility)]
                        )
                    ))

    raise ValueError("Sudoku is not solvable!")


@dataclass(order=True)
class _BoardState:
    board: _Board = field(compare=False)
    solved_cells_from_last_iter: list[tuple[_Cell, int]] = field(compare=False)


def to_display_str(sudoku: Sudoku) -> str:
    sudoku = normalize(sudoku)

    rows: list[str] = []
    for row_start in range(0, 9*9, 9):
        row_end = row_start + 9
        row = sudoku[row_start:row_end]
        rows.append(_row_to_display_str(row))

    hr_row = "------+-------+------"
    return "\n".join(
        rows[0:3]
        + [hr_row]
        + rows[3:6]
        + [hr_row]
        + rows[6:9]
    )


def to_side_by_side_display_str(
        *sudokus: Sudoku,
        labels: Iterable[str] | None = None,
        gap_size: int = 5
) -> str:
    assert gap_size > 0, "Gap size must be greater than zero!"

    gap = " " * gap_size
    display_strs = [
        to_display_str(sudoku)
        for sudoku in sudokus
    ]
    sudoku_width = display_strs[0].find("\n")

    lines: list[str] = []

    if labels is not None:
        labels = list(labels)

        assert len(labels) <= len(display_strs), \
            "There can at most be as many labels as sudokus!"

        lines.append(
            gap.join(f"{label:<{sudoku_width}}" for label in labels)
        )

    for line_segments in zip(*[s.split("\n") for s in display_strs]):
        lines.append(gap.join(line_segments))

    return "\n".join(lines)
        
        
def _row_to_display_str(row: str) -> str:
    row = row.replace("0", " ")
    return f"{' '.join(row[0:3])} | {' '.join(row[3:6])} | {' '.join(row[6:9])}"


def normalize(sudoku: Sudoku) -> str:
    if not isinstance(sudoku, str):
        s = ""

        for row in sudoku:
            if isinstance(row, str):
                s += row
            elif isinstance(row, Iterable):
                s += "".join(str(num) for num in row)

        sudoku = s

    sudoku = sudoku.replace(" ", "0")

    assert all(char.isdigit() for char in sudoku), \
        "Sudoku must only contain digits and whitespace!"

    assert len(sudoku) == 81, \
        "Sudoku has incorrect length!"

    return sudoku


Sudoku: TypeAlias = str | Iterable[str | Iterable[int | str]]
