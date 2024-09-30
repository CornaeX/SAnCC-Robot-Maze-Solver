import os
import time

# Define the maze
maze = [
    "############",
    "#.......#.+.",
    "#.##.##.##.#",
    "#.#####.####",
    "#.#.....##.#",
    "#.##.#######",
    "#.##.##.##.#",
    "#.#.........",
    "#.##.##.##.#",
    "#.##.#####.#",
    "#.##G##B....",
    "#S##########"
]

# Maze dimensions
rows = len(maze)
cols = len(maze[0])

# Directions for moving up, down, left, right
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Clear terminal based on the platform
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to print the maze with a given path
def print_maze_with_path(maze, path, current_position=None, label='P'):
    maze_copy = [list(row) for row in maze]
    
    # Mark the path taken so far
    for r, c in path:
        maze_copy[r][c] = label
    
    # Highlight the current position in the maze
    if current_position:
        r, c = current_position
        maze_copy[r][c] = 'X'
    
    # Print the updated maze
    for row in maze_copy:
        print("".join(row))
    print("\n")

# DFS to find the path from start to target
def dfs_with_animation(maze, start, target, animation_delay=0.4):
    stack = [(start, [])]  # Stack contains tuples of (position, path)
    visited = set([start])
    
    while stack:
        (r, c), path = stack.pop()
        path = path + [(r, c)]
        
        # Animation: Clear screen and print maze with path
        clear_screen()
        print_maze_with_path(maze, path, current_position=(r, c))
        time.sleep(animation_delay)  # Delay to simulate walking
        
        # Check if we've reached the target
        if maze[r][c] == target:
            return path
        
        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != '#' and (nr, nc) not in visited:
                visited.add((nr, nc))
                stack.append(((nr, nc), path))  # Push the new position and path onto the stack
    
    return None  # No path found

# Find the starting point (+), G (goal), and B (second goal)
def find_char(maze, char):
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == char:
                return r, c
    return None

# Get start, G, and B positions
start = find_char(maze, 'S')
goal_G = find_char(maze, 'G')
goal_B = find_char(maze, 'B')

# Ensure start, G, and B are found
if not start:
    print("Error: Start point (S) not found.")
elif not goal_G:
    print("Error: Goal (G) not found.")
elif not goal_B:
    print("Error: Second goal (B) not found.")
else:
    # Find the path from start to G with animation using DFS
    path_to_G = dfs_with_animation(maze, start, 'G')
    if path_to_G:
        print("Path from S to G found!")
    else:
        print("No path found from S to G.")
    
    # Find the path from G to B with animation using DFS
    path_to_B = dfs_with_animation(maze, goal_G, 'B')
    if path_to_B:
        print("Path from G to B found!")
    else:
        print("No path found from G to B.")
    
    # Combine both paths if they exist
    if path_to_G and path_to_B:
        combined_path = path_to_G + path_to_B
        print("Final Path from S to G, then to B:")
        print_maze_with_path(maze, combined_path, label='*')
    else:
        print("Unable to combine paths. One or both paths were not found.")
