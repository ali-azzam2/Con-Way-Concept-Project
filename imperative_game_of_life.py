from __future__ import annotations

"""
Imperative implementation of Conway's Game of Life.

Features:
- Uses normal Python lists (mutable)
- Uses loops (no map/filter)
- Direct mutation of grid state
- Straightforward imperative control flow
"""

from typing import List


Grid = List[List[int]]


def count_live_neighbors(grid: Grid, r: int, c: int) -> int:
    """Count live neighbors around (r, c) using loops."""
    rows = len(grid)
    cols = len(grid[0])
    count = 0

    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue  # skip itself

            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                count += grid[nr][nc]

    return count


def step(grid: Grid) -> Grid:
    """Compute next generation (modifies a copy)."""
    rows = len(grid)
    cols = len(grid[0])

    new_grid = [[0]*cols for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            live_neighbors = count_live_neighbors(grid, r, c)
            cell = grid[r][c]

            if cell == 1 and live_neighbors in (2, 3):
                new_grid[r][c] = 1
            elif cell == 0 and live_neighbors == 3:
                new_grid[r][c] = 1
            else:
                new_grid[r][c] = 0

    return new_grid
