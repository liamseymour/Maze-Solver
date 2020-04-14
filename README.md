# Maze-Solver
Simple python program that solve mazes.

![Basic Maze](/examples/maze-1.png=200x)
![Basic Maze Solution](/examples/solution-1.png=200x)

![Non-Ideal Maze](/examples/maze-2.png=200x)
![Non-Ideal Maze Solution](/examples/solution-2.png=200x)

# Usage
Maze-Solver looks for a red (0xff0000) pixel representing the end and a green (0x00ff00) pixel representing the start. Walls and borders are black (0x000000), paths are white (0xffffff).
The path to the maze image can be passed as an argument or will be prompted by the program.

# CLI Options
* [path to image]

# Undefined behavior
Impossible mazes, mazes that do not have 1 start and 1 end. Mazes that do not use 1 pixel wide paths and walls.

# Planned Features
Output options (name, filetype). Arbitrary start, and end thickness.
