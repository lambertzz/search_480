import sys
import heapq

class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __eq__(self, other):
        return isinstance(other, Position) and self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))

class State:
    def __init__(self, position, dirt, actions, cost):
        self.position = position
        self.dirt = frozenset(dirt)
        self.actions = actions
        self.cost = cost

    def is_goal(self):
        return not self.dirt

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.position == other.position and self.dirt == other.dirt

    def __hash__(self):
        return hash((self.position, self.dirt))

def parse_world(file_path):
    with open(file_path, 'r') as f:
        cols = int(f.readline())
        rows = int(f.readline())
        grid = [list(f.readline().strip()) for _ in range(rows)]

    dirt = set()
    start = None

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '*':
                dirt.add(Position(i, j))
            elif grid[i][j] == '@':
                start = Position(i, j)

    return grid, start, dirt

def get_neighbors(grid, state):
    directions = [(-1, 0, 'N'), (1, 0, 'S'), (0, -1, 'W'), (0, 1, 'E')]
    neighbors = []
    rows = len(grid)
    cols = len(grid[0])

    for dr, dc, action in directions:
        nr, nc = state.position.row + dr, state.position.col + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
            new_pos = Position(nr, nc)
            neighbors.append((State(new_pos, state.dirt, state.actions + [action], state.cost + 1)))

    # Vacuum action
    if state.position in state.dirt:
        new_dirt = set(state.dirt)
        new_dirt.remove(state.position)
        neighbors.append(State(state.position, new_dirt, state.actions + ['V'], state.cost + 1))

    return neighbors

def uniform_cost_search(grid, start, dirt):
    start_state = State(start, dirt, [], 0)
    frontier = []
    heapq.heappush(frontier, start_state)
    visited = set()

    nodes_generated = 1
    nodes_expanded = 0

    while frontier:
        current = heapq.heappop(frontier)

        if current in visited:
            continue
        visited.add(current)
        nodes_expanded += 1

        if current.is_goal():
            for action in current.actions:
                print(action)
            print(f"{nodes_generated} nodes generated")
            print(f"{nodes_expanded} nodes expanded")
            return

        for neighbor in get_neighbors(grid, current):
            if neighbor not in visited:
                heapq.heappush(frontier, neighbor)
                nodes_generated += 1

def depth_first_search(grid, start, dirt):
    start_state = State(start, dirt, [], 0)
    stack = [start_state]
    visited = set()

    nodes_generated = 1
    nodes_expanded = 0

    while stack:
        current = stack.pop()

        if current in visited:
            continue
        visited.add(current)
        nodes_expanded += 1

        if current.is_goal():
            for action in current.actions:
                print(action)
            print(f"{nodes_generated} nodes generated")
            print(f"{nodes_expanded} nodes expanded")
            return

        for neighbor in reversed(get_neighbors(grid, current)):
            if neighbor not in visited:
                stack.append(neighbor)
                nodes_generated += 1

def main():
    if len(sys.argv) != 3:
        print("3 input required")
        return

    a_name = sys.argv[1]
    world_file = sys.argv[2]
    grid, start, dirt = parse_world(world_file)

    if a_name == "uniform-cost":
        uniform_cost_search(grid, start, dirt)
    elif a_name == "depth-first":
        depth_first_search(grid, start, dirt)
    else:
        print("not definded")

if __name__ == "__main__":
    main()
