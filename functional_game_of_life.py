from __future__ import annotations
"""
Pure functional implementation of Conway's Game of Life
using:
- Higher-order functions
- Pattern matching
- Immutability
- Declarative transformations
- No side effects
- No mutation
- Functional composition

Grid representation:
A grid is a tuple of tuple integers (0=dead, 1=alive).
Each step returns a NEW grid.
"""

from typing import Iterable, Tuple, Callable

Grid = Tuple[Tuple[int, ...], ...]


# -----------------------------------------------------
# Higher-order neighbor counter: injects grid, returns function
# -----------------------------------------------------
def make_neighbor_counter(grid: Grid) -> Callable[[int, int], int]:
    offsets = [(-1,-1),(-1,0),(-1,1), (0,-1),(0,1), (1,-1),(1,0),(1,1)]
    rows, cols = len(grid), len(grid[0])

    # HOF: returns a function that counts neighbors for (r, c)
    def count(r: int, c: int) -> int:
        return sum(
            grid[r+dr][c+dc]
            for dr, dc in offsets
            if 0 <= r+dr < rows and 0 <= c+dc < cols
        )

    return count


# -----------------------------------------------------
# Higher-order next-cell rule generator
# -----------------------------------------------------
def make_next_cell(grid: Grid) -> Callable[[int, int], int]:
    count_neighbors = make_neighbor_counter(grid)

    # HOF: next_cell is returned and used functionally
    def next_cell(r: int, c: int) -> int:
        live_neighbors = count_neighbors(r, c)
        cell = grid[r][c]

        # Pattern matching rules
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


# -----------------------------------------------------
# Step using PURE higher-order functional mapping
# -----------------------------------------------------
def step(grid: Grid) -> Grid:
    """Return next generation using higher-order functional mapping."""
    if not grid:
        return ()

    rows, cols = len(grid), len(grid[0])
    next_cell = make_next_cell(grid)

    # NO loops -> map-of-map functional construction
    return tuple(
        tuple(next_cell(r, c) for c in range(cols))
        for r in range(rows)
    )


# -----------------------------------------------------
# Parsing from strings using higher-order functional mapping
# -----------------------------------------------------
def from_strings(lines: Iterable[str]) -> Grid:

    def char_to_cell(ch: str) -> int:
        match ch:
            case "1" | "#" | "*" | "X":
                return 1
            case _:
                return 0

    # Functional mapping of lines → rows → ints
    grid = tuple(
        tuple(map(char_to_cell, line.strip()))
        for line in lines
        if line.strip()
    )

    match grid:
        case ():
            raise ValueError("Grid cannot be empty.")
        case (first, *rest):
            if any(len(row) != len(first) for row in rest):
                raise ValueError("All rows must have same length.")

    return grid


# -----------------------------------------------------
# Convert back to strings
# -----------------------------------------------------
def to_strings(grid: Grid) -> Tuple[str, ...]:
    return tuple(
        "".join("1" if cell else "0" for cell in row)
        for row in grid
    )
