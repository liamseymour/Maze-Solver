# Maze-Solver
Simple python program that solve mazes.

# Usage
Maze-Solver looks for a red (0xff0000) pixel representing the end and a green (0x00ff00) pixel representing the start. Walls and borders are black (0x000000), paths are white (0xffffff).
The path to the maze image can be passed as an argument or will be prompted by the program.
--show-trim Option will remove the dead ends from the output.

Undefined behavior: Impossible mazes, mazes that do not have 1 start and 1 end. Mazes that do not use 1 pixel wide paths and walls.

Planned features: Output options (name, filetype). Arbitrary wall, start, and end thickness.
