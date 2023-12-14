import copy
import operator
from pathlib import Path

"""
--- Day 10: Pipe Maze ---
You use the hang glider to ride the hot air from Desert Island all the way up to the floating metal island. This island is surprisingly cold and there definitely aren't any thermals to glide on, so you leave your hang glider behind.

You wander around for a while, but you don't find any people or animals. However, you do occasionally find signposts labeled "Hot Springs" pointing in a seemingly consistent direction; maybe you can find someone at the hot springs and ask them where the desert-machine parts are made.

The landscape here is alien; even the flowers and trees are made of metal. As you stop to admire some metal grass, you notice something metallic scurry away in your peripheral vision and jump into a big pipe! It didn't look like any animal you've ever seen; if you want a better look, you'll need to get ahead of it.

Scanning the area, you discover that the entire field you're standing on is densely packed with pipes; it was hard to tell at first because they're the same metallic silver color as the "ground". You make a quick sketch of all of the surface pipes you can see (your puzzle input).

The pipes are arranged in a two-dimensional grid of tiles:

| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
Based on the acoustics of the animal's scurrying, you're confident the pipe that contains the animal is one large, continuous loop.

For example, here is a square loop of pipe:

.....
.F-7.
.|.|.
.L-J.
.....
If the animal had entered this loop in the northwest corner, the sketch would instead look like this:

.....
.S-7.
.|.|.
.L-J.
.....
In the above diagram, the S tile is still a 90-degree F bend: you can tell because of how the adjacent pipes connect to it.

Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows the same loop as above:

-L|F7
7S-7|
L|7||
-L-J|
L|-JF
In the above diagram, you can still figure out which pipes form the main loop: they're the ones connected to S, pipes those pipes connect to, pipes those pipes connect to, and so on. Every pipe in the main loop connects to its two neighbors (including S, which will have exactly two pipes connecting to it, and which is assumed to connect back to those two pipes).

Here is a sketch that contains a slightly more complex main loop:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...
Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:

7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
If you want to get out ahead of the animal, you should find the tile in the loop that is farthest from the starting position. Because the animal is in the pipe, it doesn't make sense to measure this by direct distance. Instead, you need to find the tile that would take the longest number of steps along the loop to reach from the starting point - regardless of which way around the loop the animal went.

In the first example with the square loop:

.....
.S-7.
.|.|.
.L-J.
.....
You can count the distance each tile in the loop is from the starting point like this:

.....
.012.
.1.3.
.234.
.....
In this example, the farthest point from the start is 4 steps away.

Here's the more complex loop again:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...
Here are the distances for each tile on that loop:

..45.
.236.
01.78
14567
23...
Find the single giant loop starting at S. How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?

--- Part Two ---
You quickly reach the farthest point of the loop, but the animal never emerges. Maybe its nest is within the area enclosed by the loop?

To determine whether it's even worth taking the time to search for such a nest, you should calculate how many tiles are contained within the loop. For example:

...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
The above loop encloses merely four tiles - the two pairs of . in the southwest and southeast (marked I below). The middle . tiles (marked O below) are not in the loop. Here is the same loop again with those regions marked:

...........
.S-------7.
.|F-----7|.
.||OOOOO||.
.||OOOOO||.
.|L-7OF-J|.
.|II|O|II|.
.L--JOL--J.
.....O.....
In fact, there doesn't even need to be a full tile path to the outside for tiles to count as outside the loop - squeezing between pipes is also allowed! Here, I is still within the loop and O is still outside the loop:

..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........
In both of the above examples, 4 tiles are enclosed by the loop.

Here's a larger example:

.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
The above sketch has many random bits of ground, some of which are in the loop (I) and some of which are outside it (O):

OF----7F7F7F7F-7OOOO
O|F--7||||||||FJOOOO
O||OFJ||||||||L7OOOO
FJL7L7LJLJ||LJIL-7OO
L--JOL7IIILJS7F-7L7O
OOOOF-JIIF7FJ|L7L7L7
OOOOL7IF7||L7|IL7L7|
OOOOO|FJLJ|FJ|F7|OLJ
OOOOFJL-7O||O||||OOO
OOOOL---JOLJOLJLJOOO
In this larger example, 8 tiles are enclosed by the loop.

Any tile that isn't part of the main loop can count as being enclosed by the loop. Here's another example with many bits of junk pipe lying around that aren't connected to the main loop at all:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
Here are just the tiles that are enclosed by the loop marked with I:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
In this last example, 10 tiles are enclosed by the loop.

Figure out whether you have time to search for the nest by calculating the area within the loop. How many tiles are enclosed by the loop?
"""


def move(coords: tuple[int, int], direction: tuple[int, int]) -> tuple[int, int]:
    return tuple(map(operator.add, coords, direction))


def find_start_pipe(maze: list[str]) -> tuple[str, tuple[int, int]]:
    for y, line in enumerate(maze):
        if "S" in line:
            start_y = y
            start_x = line.index("S")
            for pipe in "|-LJ7F":
                next_moves = find_connections(pipe)
                sx, sy = move((start_x, start_y), next_moves[0])
                ex, ey = move((start_x, start_y), next_moves[1])
                if next_moves[0] in find_connections(maze[sy][sx]) and next_moves[1] in find_connections(maze[ey][ex]):
                    return pipe, (start_x, start_y)

    assert False, f"Could not find starting pipe at with exactly 2 adjacent connections"


def find_connections(pipe: str) -> list[tuple[int, int]]:
    connections = []
    if pipe in "|7F":
        connections.append((0, -1))
    if pipe in "-J7":
        connections.append((1, 0))
    if pipe in "|JL":
        connections.append((0, 1))
    if pipe in "-LF":
        connections.append((-1, 0))
    return connections


def next_move(maze: list[str], coords: tuple[int, int], prev_coords: tuple[int, int]) -> tuple[int, int]:
    x, y = coords
    s, t = prev_coords
    prev_move = (x - s, y - t)
    pipe = maze[y][x]
    if pipe == "|" and prev_move in {(0, 1), (0, -1)}:
        return prev_move
    elif pipe == "-" and prev_move in {(1, 0), (-1, 0)}:
        return prev_move
    elif pipe in "L7":
        return prev_move[1], prev_move[0]
    elif pipe in "JF":
        return -prev_move[1], -prev_move[0]
    else:
        assert False, f"Unexpected pipe {pipe} at {coords}, {prev_move}"


def find_loop(maze: list[str]) -> tuple[set[tuple[int, int]], int]:
    # Figure out what pipe S is
    start_pipe, (start_x, start_y) = find_start_pipe(maze)
    maze = copy.deepcopy(maze)
    maze[start_y] = maze[start_y].replace("S", start_pipe)

    # Make the first move from S
    coords = (start_x, start_y)
    connections = find_connections(start_pipe)
    assert len(connections) == 2, f"Expected exactly 2 connections from starting point S, got {len(connections)}"
    prev_start = prev_end = coords
    start = move(coords, connections[0])
    end = move(coords, connections[1])
    loop = {coords, start, end}
    steps = 1

    # Keep moving from each end of the start pipe until they meet
    while start != end:
        next_start = move(start, next_move(maze, start, prev_coords=prev_start))
        next_end = move(end, next_move(maze, end, prev_coords=prev_end))
        prev_start = start
        prev_end = end
        start = next_start
        end = next_end
        loop.add(start)
        loop.add(end)
        steps += 1

    return loop, steps


def part1(maze) -> int:
    return find_loop(maze)[1]


def part2(maze) -> int:
    loop = find_loop(maze)[0]
    total = 0
    for y, line in enumerate(maze):
        is_inside = False
        for x, tile in enumerate(line):
            if (x, y) in loop:
                if tile in "|F7":
                    is_inside = not is_inside
            elif is_inside is True:
                total += 1

    return total


if __name__ == '__main__':
    lines = Path("../inputs/10.txt").read_text().splitlines()
    print(part1(lines))
    print(part2(lines))
