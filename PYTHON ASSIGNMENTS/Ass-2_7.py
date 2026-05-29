def maze_runner(maze, start_pos, end_pos):
    if start_pos == end_pos:
        return [start_pos]
    rows = len(maze)
    cols = len(maze[0]) if rows > 0 else 0
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    path = [start_pos]
    current = start_pos
    max_steps = rows * cols * 2
    steps = 0
    while current != end_pos and steps < max_steps:
        r, c = current
        moved = False
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                cell = maze[nr][nc]
                if cell == ' ' or cell == 'E':
                    path.append((nr, nc))
                    current = (nr, nc)
                    moved = True
                    break
        if not moved:
            return None
        steps += 1
    if current != end_pos:
        return None
    return path
maze = [
    "S  #",
    "#  E",
    "   #"
]
start = (0, 0)
end = (1, 3)
path = maze_runner(maze, start, end)
print(path)  