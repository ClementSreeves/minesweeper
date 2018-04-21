#usr/bin/env python3

import numpy as np
from itertools import product 
from functools import partial
from tkinter import *
from tkinter import ttk

length = 10
width = 10
mines = 20

def neighbours(index):
    "Given an (x,y) position, returns neigbours on a grid"
    x, y = index
    return ((x + 1, y),
            (x + 1, y + 1),
            (x + 1, y - 1),
            (x, y + 1),
            (x, y - 1),
            (x - 1, y),
            (x - 1, y + 1),
            (x - 1, y - 1))

def border(fill, grid):
    "Surround a grid with a border of fill. Idea from Peter Norvig!"
    new_cols = np.vstack(np.array([fill] * grid.shape[0]))
    grid = np.hstack([new_cols, grid, new_cols])
    new_rows = np.array([fill] * grid.shape[1])
    return np.vstack([new_rows, grid, new_rows])

assert((border(0, np.array([[1, 2], [3, 4]])) == np.array(
    [[0, 0, 0, 0],
     [0, 1, 2, 0], 
     [0, 3, 4, 0], 
     [0, 0, 0, 0]])).all())

#We will go for -1 where there is a mine, and the number that shows up in
#gameplay otherwise. (0 for blank)
num_cells = width * length
mine_loc = np.random.choice(range(num_cells), size=mines, replace=False)
cells = np.zeros(num_cells, dtype=int)
cells[mine_loc] = -1
#using a border prevents both IndexError and negative indexing bugs
grid = border(-2, cells.reshape((width, length)))

board_cells = list(product(range(1, length + 1), range(1, width + 1)))
for cell in board_cells:
    if grid[cell] < 0:
        continue
    grid[cell] = sum([(grid[nbr] == -1) for nbr in neighbours(cell)])

print(grid)

root = Tk()
root.title('Minesweeper')

grid_frame = ttk.Frame(root, padding='5')
grid_frame.grid()

def reveal(index, revealed=set()):
    revealed.add(index)
    value = grid[index]
    if value == -2: return
    button_grid[index].configure(text=value, state='disabled')
    if value == 0:
        [reveal(nbr) for nbr in neighbours(index) if nbr not in revealed] 

button_grid = []
for i, j in board_cells:
    #use partial to pass the index at definition time, rather than runtime
    button = ttk.Button(grid_frame, command=partial(reveal, (i, j)))
    button_grid.append(button)
    button.grid(row=i, column=j)

button_grid = border(object(), np.array(button_grid).reshape((length, width)))

root.mainloop()
