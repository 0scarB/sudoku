from __future__ import annotations

from ._types import Cell


_cells_to_cells_sharing_possibilities: dict[Cell, set[Cell]] = {}
def get_cells_sharing_possibilities(cell: Cell) -> set[Cell]:
    global _cells_to_cells_sharing_possibilities

    try:
        return _cells_to_cells_sharing_possibilities[cell]
    except KeyError:
        sharing_cells: set[Cell] = set()
        for group in get_groups(cell):
            for cell_in_group in get_cells_by_group(group):
                if cell_in_group != cell:
                    sharing_cells.add(cell_in_group)

        _cells_to_cells_sharing_possibilities[cell] = sharing_cells

        return sharing_cells


def get_groups(cell: Cell) -> set[int]:
    return _get_cells_to_groups()[cell]


def get_cells_by_group(group: int) -> set[Cell]:
    return _get_groups_to_cells()[group]


_groups_to_cells: dict[int, set[Cell]] | None = None
def _get_groups_to_cells() -> dict[int, set[Cell]]:
    global _groups_to_cells

    if _groups_to_cells is None:
        _groups_to_cells = {}

        for cell, groups in _get_cells_to_groups().items():
            for group in groups:
                if group not in _groups_to_cells:
                    _groups_to_cells[group] = {cell}
                else:
                    _groups_to_cells[group].add(cell)

    return _groups_to_cells


_cells_to_groups: dict[Cell, set[int]] | None = None
def _get_cells_to_groups() -> dict[Cell, set[int]]:
    global _cells_to_groups

    if _cells_to_groups is None:
        _cells_to_groups = {
            (row, col): set()
            for row in range(9)
            for col in range(9)
        }
        group_offset = 0
        for layout in _LAYOUTS:
            for row_cell, row in enumerate(layout):
                for col_cell, group_str in enumerate(row):
                    cell = (row_cell, col_cell)
                    group = group_offset + int(group_str)
                    _cells_to_groups[cell].add(group)

            group_offset += 9

    return _cells_to_groups


_LAYOUTS: list[tuple[str, ...]] = [
    (
        "000000000",
        "111111111",
        "222222222",
        "333333333",
        "444444444",
        "555555555",
        "666666666",
        "777777777",
        "888888888"
    ),
    (
        "012345678",
        "012345678",
        "012345678",
        "012345678",
        "012345678",
        "012345678",
        "012345678",
        "012345678",
        "012345678"
    ),
    (
        "000111222",
        "000111222",
        "000111222",
        "333444555",
        "333444555",
        "333444555",
        "666777888",
        "666777888",
        "666777888"
    )
]
