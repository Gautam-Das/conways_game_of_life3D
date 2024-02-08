import time
import tkinter as tk

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Part of matplotlib
import numpy as np


class GameOfLife:
    """The main game class.
    Takes in the starting game grid as a 3D NumPy of booleans.
    """

    def __init__(self, grid):
        self.grid = grid
        self.prev_generations = []
        self.calculation_time = 0
        self.ax = self.make_ax()

    def make_ax(self):
        """Creates the 3d grid using the mplot3d library for displaying."""
        ax = plt.axes(projection='3d')
        ax.grid(True)
        return ax

    def display(self, grid, color_map):
        """Displays the 3D grid."""
        plt.cla()
        self.ax.voxels(grid, facecolors=color_map, edgecolors='gray', shade=False)
        plt.draw()
        plt.pause(0.01)

    def simulate(self):
        """Displays all the generations."""
        color_map = np.zeros([10, 10, 10, 3])
        for generation in self.prev_generations:
            for z, y, x in np.ndindex(self.grid.shape):
                if generation[z, y, x] == 0:
                    color_map[z, y, x] = (1, 1, 0)
                else:
                    color_map[z, y, x] = (1, max(color_map[z, y, x][1] - 0.1, 0), 0)

            self.display(generation, color_map)

    def n_surrounding_cells(self, z, y, x):
        """Calculates the number of neighbours of a given cell."""

        # Clip the bounds so that all cells are in range
        z_bounds = np.clip([z - 1, z + 2], a_min=0, a_max=self.grid.shape[0])
        y_bounds = np.clip([y - 1, y + 2], a_min=0, a_max=self.grid.shape[1])
        x_bounds = np.clip([x - 1, x + 2], a_min=0, a_max=self.grid.shape[2])

        total = np.sum(
            self.grid[
                z_bounds[0] : z_bounds[1],
                y_bounds[0] : y_bounds[1],
                x_bounds[0] : x_bounds[1],
            ]
        )
        # A cell can't be its own neighbour, so remove it
        return total - 1 if self.grid[z, y, x] == 1 else total

    def step(self):
        """Calculates the next generation of the simulation.
        This will update the grid attribute to the next generation.
        """
        start_time = time.monotonic()
        next_generation = np.zeros(self.grid.shape, dtype='bool')

        for z, y, x in np.ndindex(self.grid.shape):
            if self.grid[z, y, x] == 1 and self.n_surrounding_cells(z, y, x) == 9:
                next_generation[z, y, x] = 1
            elif self.grid[z, y, x] == 0 and self.n_surrounding_cells(z, y, x) == 4:
                next_generation[z, y, x] = 1
            # Any other cells are dead
            else:
                next_generation[z, y, x] = 0

        self.grid = next_generation
        self.prev_generations.append(next_generation)
        self.calculation_time += time.monotonic() - start_time


class InputWindow(tk.Frame):
    """A simple Tkinter window for retrieving required user input."""

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.width = 400
        self.height = 300

        self.seed_entry = tk.Entry(self.parent, width=30)
        self.generations_entry = tk.Entry(self.parent, width=30)
        self.progress_label = tk.Label(self.parent, text='', font=('Arial', 12))
        self.create_gui()

    def random_seed(self):
        self.seed_entry.delete(0, tk.END)
        self.seed_entry.insert(0,
            ''.join([np.random.choice(['1', '2', '3', '4', '5', '6', '7', '8', '9']) for _ in range(8)]))

    def execute(self):
        """Retrives all the inputs and runs the simulation."""
        np.random.seed(int(self.seed_entry.get()))
        generate_grid(10)
        game = GameOfLife(generate_grid(10))
        n_generations = int(self.generations_entry.get())

        for i in range(n_generations):
            self.progress_label.config(text=f'{i+1}/{n_generations} completed.')
            self.parent.update()
            game.step()

        print(f'Total time for calculations: {game.calculation_time}s')
        game.simulate()

    def create_gui(self):
        """Sets up all the required GUI components."""
        title_label = tk.Label(
            self.parent, text='3D Conway\'s Game of Life', font=('Arial', 20)
        )
        seed_label = tk.Label(self.parent, text='Seed', font=('Arial', 12))
        random_button = tk.Button(
            self.parent,
            text='Create random seed',
            width=22,
            font=('Arial', 10),
            command=self.random_seed,
        )
        generations_label = tk.Label(
            self.parent, text='Number of Generations', font=('Arial', 12)
        )
        execute_button = tk.Button(
            self.parent,
            text='Execute',
            width=20,
            font=('Arial', 12),
            bg='#5cb85c',
            command=self.execute,
        )

        title_label.pack(pady=(5, 15))
        seed_label.pack()
        self.seed_entry.pack(pady=5)
        random_button.pack(pady=(5, 15))
        generations_label.pack()
        self.generations_entry.pack(pady=(5, 15))
        execute_button.pack()
        self.progress_label.pack()


def generate_grid(size):
    return np.random.randint(2, size=[size, size, size], dtype='bool')


def main():
    root = tk.Tk()
    root.geometry('500x300')
    root.title('3D Conway\'s Game of Life')
    InputWindow(root).pack(side='top', fill='both', expand=True)
    root.mainloop()


if __name__ == '__main__':
    main()