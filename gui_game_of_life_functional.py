from __future__ import annotations

"""
Tkinter GUI for Conway's Game of Life using the pure functional engine.

State is immutable: every generation produces a brand-new grid (tuple of tuples).
Controls mirror the imperative GUI:
- Start / Pause loop
- Step once
- Randomize
- Clear
- Speed slider (milliseconds)
- Click cells to toggle
"""

import random
import tkinter as tk
from typing import List, Optional, Tuple

import functional_game_of_life as functional

Grid = Tuple[Tuple[int, ...], ...]


def empty_grid(rows: int, cols: int) -> Grid:
    return tuple(tuple(0 for _ in range(cols)) for _ in range(rows))


def set_cell(grid: Grid, row: int, col: int, value: int) -> Grid:
    """Return a new grid with a single cell changed."""
    return tuple(
        tuple(
            value if (r == row and c == col) else grid[r][c]
            for c in range(len(grid[0]))
        )
        for r in range(len(grid))
    )


def random_grid(rows: int, cols: int) -> Grid:
    return tuple(
        tuple(random.randint(0, 1) for _ in range(cols)) for _ in range(rows)
    )


class GameOfLifeFunctionalGUI:
    def __init__(self, rows: int = 25, cols: int = 35, cell_size: int = 20):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.running = False
        self.after_id: Optional[str] = None
        self.generation = 0
        self.grid: Grid = empty_grid(rows, cols)

        self.root = tk.Tk()
        self.root.title("Conway's Game of Life (Functional GUI)")

        width = cols * cell_size
        height = rows * cell_size
        self.canvas = tk.Canvas(
            self.root, width=width, height=height, bg="white", highlightthickness=0
        )
        self.canvas.pack(side=tk.TOP, padx=10, pady=10)

        controls = tk.Frame(self.root)
        controls.pack(side=tk.TOP, pady=5)

        tk.Button(controls, text="Start", command=self.start).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="Pause", command=self.pause).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="Step", command=self.step_once).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="Randomize", command=self.randomize).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="Clear", command=self.clear).pack(side=tk.LEFT, padx=5)

        tk.Label(controls, text="Speed (ms)").pack(side=tk.LEFT, padx=5)
        self.speed_scale = tk.Scale(
            controls, from_=50, to=1000, orient=tk.HORIZONTAL, length=200
        )
        self.speed_scale.set(200)
        self.speed_scale.pack(side=tk.LEFT)

        self.status_var = tk.StringVar(value="Generation: 0")
        tk.Label(self.root, textvariable=self.status_var).pack(side=tk.TOP, pady=5)

        self.rects = self._create_rectangles()
        self.canvas.bind("<Button-1>", self.toggle_cell)
        self._refresh_canvas()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _create_rectangles(self) -> List[List[int]]:
        rects: List[List[int]] = []
        for r in range(self.rows):
            row_rects = []
            for c in range(self.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                rect = self.canvas.create_rectangle(
                    x1, y1, x2, y2, outline="#ddd", fill="white"
                )
                row_rects.append(rect)
            rects.append(row_rects)
        return rects

    def _refresh_canvas(self):
        for r in range(self.rows):
            for c in range(self.cols):
                color = "#111" if self.grid[r][c] else "white"
                self.canvas.itemconfig(self.rects[r][c], fill=color)
        self.status_var.set(f"Generation: {self.generation}")

    def toggle_cell(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            value = 0 if self.grid[row][col] else 1
            self.grid = set_cell(self.grid, row, col, value)
            self._refresh_canvas()

    def start(self):
        if self.running:
            return
        self.running = True
        self._loop()

    def pause(self):
        if not self.running:
            return
        self.running = False
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def step_once(self):
        self.pause()
        self._advance()

    def _loop(self):
        if not self.running:
            return
        self._advance()
        delay = int(self.speed_scale.get())
        self.after_id = self.root.after(delay, self._loop)

    def _advance(self):
        self.grid = functional.step(self.grid)
        self.generation += 1
        self._refresh_canvas()

    def randomize(self):
        self.pause()
        self.grid = random_grid(self.rows, self.cols)
        self.generation = 0
        self._refresh_canvas()

    def clear(self):
        self.pause()
        self.grid = empty_grid(self.rows, self.cols)
        self.generation = 0
        self._refresh_canvas()

    def _on_close(self):
        self.pause()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    GameOfLifeFunctionalGUI().run()

