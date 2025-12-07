from __future__ import annotations

"""
Pure functional implementation of Conway's Game of Life.

Grid representation:
- A grid is a tuple of tuple integers (0 = dead, 1 = alive).
- No mutation is performed; every step returns a new grid.
"""

from typing import Iterable, Tuple

Grid = Tuple[Tuple[int, ...], ...]


def count_live_neighbors(grid: Grid, row: int, col: int) -> int:
    """Count live neighbors for cell (row, col) without mutating state."""
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    offsets = (
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    )

    # Avoid walrus side effects for clarity. Pure computation.
    total = 0
    for dr, dc in offsets:
        rr, cc = row + dr, col + dc
        if 0 <= rr < rows and 0 <= cc < cols:
            total += grid[rr][cc]
    return total


def step(grid: Grid) -> Grid:
    """Compute the next generation without mutating the original grid."""
    if not grid:
        return ()
    rows, cols = len(grid), len(grid[0])

    def next_cell(r: int, c: int) -> int:
        live_neighbors = count_live_neighbors(grid, r, c)
        if grid[r][c] == 1:
            return 1 if live_neighbors in (2, 3) else 0
        return 1 if live_neighbors == 3 else 0

    # Return a brand new immutable grid
    return tuple(
        tuple(next_cell(r, c) for c in range(cols)) for r in range(rows)
    )


def from_strings(lines: Iterable[str]) -> Grid:
    """
    Build an immutable grid from an iterable of strings.

    Accepted alive markers: "1", "#", "*", "X".
    Anything else is treated as dead.
    """
    mapping = {"1", "#", "*", "X"}

    # Convert each row into immutable tuple of 0/1
    grid = tuple(
        tuple(1 if ch in mapping else 0 for ch in line.strip())
        for line in lines
        if line.strip()  # ignore empty lines completely
    )

    # Validate structure: non-empty and equally sized rows
    if not grid:
        raise ValueError("Grid cannot be empty.")
    if any(len(row) != len(grid[0]) for row in grid):
        raise ValueError("All input rows must have the same length.")

    return grid


def to_strings(grid: Grid) -> Tuple[str, ...]:
    """Convert a grid back to strings of 0/1 for easy display."""
    return tuple("".join("1" if cell else "0" for cell in row) for row in grid)

