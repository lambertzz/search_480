import sys
from heapq import heappush, heappop
from collections import namedtuple

GridPos = namedtuple('GridPos', ['y', 'x'])

class SearchState:
    
    def __init__(self, pos, dirty_spots, path=[], total_cost=0):
        self.pos = pos
        self.dirty_spots = frozenset(dirty_spots)
        self.path = path.copy()  
        self.total_cost = total_cost
    
    @property
    def is_solved(self):
        return len(self.dirty_spots) == 0
    
    def __lt__(self, other):
        return self.total_cost < other.total_cost
    
    def __eq__(self, other):
        if not isinstance(other, SearchState):
            return False
        return (self.pos == other.pos and 
                self.dirty_spots == other.dirty_spots)

    def __hash__(self):
        return hash((self.pos, self.dirty_spots))

def load_world_layout(filepath):
    with open(filepath) as f:
        width = int(f.readline())
        height = int(f.readline())
        grid_rows = [line.strip() for line in f.readlines()]
    
    robot_start = None
    dirty_cells = set()
    
    for y in range(height):
        for x in range(width):
            cell = grid_rows[y][x]
            if cell == '@':
                robot_start = GridPos(y, x)
            elif cell == '*':
                dirty_cells.add(GridPos(y, x))
    return grid_rows, robot_start, dirty_cells

def get_possible_moves(world, current_state):
    moves = []
    height = len(world)
    width = len(world[0]) if height > 0 else 0
    
    directions = [
        (-1, 0, 'N'), (1, 0, 'S'),
        (0, -1, 'W'), (0, 1, 'E')
    ]
    
    for dy, dx, action in directions:
        new_y, new_x = current_state.pos.y + dy, current_state.pos.x + dx
        
        if (0 <= new_y < height and 
            0 <= new_x < width and 
            world[new_y][new_x] != '#'):
            new_pos = GridPos(new_y, new_x)
            moves.append(SearchState(
                new_pos,
                current_state.dirty_spots,
                current_state.path + [action],
                current_state.total_cost + 1
            ))
    
    if current_state.pos in current_state.dirty_spots:
        updated_dirt = set(current_state.dirty_spots)
        updated_dirt.remove(current_state.pos)
        moves.append(SearchState(
            current_state.pos,
            updated_dirt,
            current_state.path + ['V'],
            current_state.total_cost + 1
        ))
    
    return moves

def run_uniform_cost_search(world_map, start_pos, dirt_locations):
    initial_state = SearchState(start_pos, dirt_locations)
    frontier = []
    heappush(frontier, initial_state)
    explored = set()
    stats = {'generated': 1, 'expanded': 0}
    
    while frontier:
        current = heappop(frontier)
        
        if current in explored:
            continue
        explored.add(current)
        stats['expanded'] += 1
        
        if current.is_solved:
            print('\n'.join(current.path))
            print(f"{stats['generated']} nodes generated")
            print(f"{stats['expanded']} nodes expanded")
            return
        
        for neighbor in get_possible_moves(world_map, current):
            if neighbor not in explored:
                heappush(frontier, neighbor)
                stats['generated'] += 1

def run_depth_first_search(world_map, start_pos, dirt_locations):
    initial_state = SearchState(start_pos, dirt_locations)
    stack = [initial_state]
    visited = set()
    
    stats = {'generated': 1, 'expanded': 0}
    
    while stack:
        current = stack.pop()
        
        if current in visited:
            continue
        visited.add(current)
        stats['expanded'] += 1
        
        if current.is_solved:
            print('\n'.join(current.path))
            print(f"{stats['generated']} nodes generated")
            print(f"{stats['expanded']} nodes expanded")
            return
        
        for neighbor in reversed(get_possible_moves(world_map, current)):
            if neighbor not in visited:
                stack.append(neighbor)
                stats['generated'] += 1

def main():
    if len(sys.argv) != 3:
        print("invalid entry")
        sys.exit(1)
    
    algorithm = sys.argv[1].lower()
    world_file = sys.argv[2]
    
    try:
        world, start, dirt = load_world_layout(world_file)
    except Exception as e:
        print(f"Error loading: {e}")
        sys.exit(1)
    
    if algorithm == "uniform-cost":
        run_uniform_cost_search(world, start, dirt)
    elif algorithm == "depth-first":
        run_depth_first_search(world, start, dirt)
    else:
        print(f"Unknown")
        sys.exit(1)

if __name__ == "__main__":
    main()