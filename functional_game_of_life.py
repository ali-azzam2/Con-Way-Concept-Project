from __future__ import annotations
"""
Recursive functional implementation of Conway's Game of Life.

- Uses recursion to build the next grid
- Higher-order functions for neighbor counting
- Pattern matching for rules
- Immutable tuples
"""

from typing import Tuple, Callable

Grid = Tuple[Tuple[int, ...], ...]


# -------------------------
# Neighbor counter HOF
# -------------------------
def make_neighbor_counter(grid: Grid) -> Callable[[int, int], int]:
    offsets = [(-1,-1),(-1,0),(-1,1), (0,-1),(0,1), (1,-1),(1,0),(1,1)]
    rows, cols = len(grid), len(grid[0])

    def count(r: int, c: int) -> int:
        return sum(
            grid[r+dr][c+dc]
            for dr, dc in offsets
            if 0 <= r+dr < rows and 0 <= c+dc < cols
        )

    return count


# -------------------------
# Next-cell HOF
# -------------------------
def make_next_cell(grid: Grid) -> Callable[[int, int], int]:
    count_neighbors = make_neighbor_counter(grid)

    def next_cell(r: int, c: int) -> int:
        cell = grid[r][c]
        live_neighbors = count_neighbors(r, c)
        match (cell, live_neighbors):
            case (1, n) if n in (2, 3):
                return 1
            case (1, _):
                return 0
            case (0, 3):
                return 1
            case _:
                return 0

    return next_cell


# -------------------------
# Recursive step helpers
# -------------------------
def step_row(next_cell: Callable[[int,int],int], r: int, c: int, cols: int) -> Tuple[int, ...]:
    """Recursively build one row."""
    if c >= cols:
        return ()
    return (next_cell(r, c),) + step_row(next_cell, r, c+1, cols)


def step_grid(next_cell: Callable[[int,int],int], r: int, rows: int, cols: int) -> Grid:
    """Recursively build the whole grid."""
    if r >= rows:
        return ()
    return (step_row(next_cell, r, 0, cols),) + step_grid(next_cell, r+1, rows, cols)


# -------------------------
# Step function (recursive)
# -------------------------
def step(grid: Grid) -> Grid:
    """Return next generation recursively."""
    if not grid:
        return ()
    rows, cols = len(grid), len(grid[0])
    next_cell = make_next_cell(grid)
    return step_grid(next_cell, 0, rows, cols)
