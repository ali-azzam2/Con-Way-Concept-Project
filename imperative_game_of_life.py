"""
Imperative (mutable) implementation of Conway's Game of Life.

Grid representation:
- A grid is a list of lists of integers (0 = dead, 1 = alive).
- The step method mutates the grid in place for clarity on imperative style.
"""
from __future__ import annotations
from typing import Iterable, List


class GameOfLifeMutable:
    """Imperative implementation of Conway's Game of Life."""
    
    def __init__(self, grid: Iterable[Iterable[int]], wrap: bool = False):
        """
        Initialize the game with a grid.
        
        Args:
            grid: 2D iterable of integers (0 = dead, 1 = alive)
            wrap: If True, edges wrap around (toroidal topology)
        """
        snapshot = [list(row) for row in grid]
        if not snapshot:
            self.grid: List[List[int]] = []
            self.rows = self.cols = 0
            return

        cols = len(snapshot[0])
        for row in snapshot:
            if len(row) != cols:
                raise ValueError("All rows must have the same length")
            if any(cell not in (0, 1) for cell in row):
                raise ValueError("Cells must be 0 or 1")

        self.grid = snapshot
        self.rows = len(snapshot)
        self.cols = cols
        self.wrap = wrap

    def count_live_neighbors(self, row: int, col: int) -> int:
        """Count live neighbors around a cell using imperative approach."""
        total = 0
        for dr, dc in ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)):
            r, c = row + dr, col + dc
            if self.wrap:
                r %= self.rows
                c %= self.cols
                total += self.grid[r][c]
            elif 0 <= r < self.rows and 0 <= c < self.cols:
                total += self.grid[r][c]
        return total

    def step(self) -> None:
        """Advance one generation by mutating the internal grid."""
        if not self.grid:
            return
        next_grid = [[0] * self.cols for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                live_neighbors = self.count_live_neighbors(r, c)
                if self.grid[r][c] == 1:
                    next_grid[r][c] = 1 if live_neighbors in (2, 3) else 0
                else:
                    next_grid[r][c] = 1 if live_neighbors == 3 else 0
        self.grid = next_grid

    def clone_grid(self) -> List[List[int]]:
        """Return a deep copy of the current grid."""
        return [row[:] for row in self.grid]

    def display(self, alive: str = "█", dead: str = " ") -> None:
        """Display the grid to console."""
        for row in self.grid:
            print("".join(alive if c else dead for c in row))
        print()