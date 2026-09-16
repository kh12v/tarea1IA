import numpy as np

# Considerations:
# 1. The maps are designed to be 10x10 grids
# 2. There can only be one exit point in the map.
# 3. There are exactly 3 people per map.
# 4. The fire spreads with a probability of 0.3 per time step, and it can spread to adjacent cells (up, down, left, right).

# Terminology:
# '#' represents walls or obstacles.
# '1' Represents a person or an agent.
# '2' Represents two people or agents.
# '3' Represents three people or agents.
# 'E' represents the exit point.
# '*' represents a fire obstacle.

# Number of turns the fire spreads
NUM_FIRE_TURNS = 2

# Maximum number of people allowed on a single cell at once
MAX_PEOPLE_PER_CELL = 2

if (MAX_PEOPLE_PER_CELL < 1 or MAX_PEOPLE_PER_CELL > 3):
    print("Error: Maximum number of people per cell is not between 1 and 3")
    exit(1)

map1_high_density = np.array([
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', '*', '1', ' ', '#', '#', '#', '#', '#', '#'],
    ['#', '1', '#', ' ', '#', '#', '#', '#', '#', '#'],
    ['#', '1', '#', ' ', ' ', ' ', ' ', ' ', '#', '#'],
    ['#', ' ', '#', '#', '#', '#', ' ', ' ', '#', '#'],
    ['#', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', '#'],
    ['#', ' ', '#', ' ', ' ', '#', ' ', ' ', '#', '#'],
    ['#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', '#', '#', '#', ' ', ' ', 'E', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
])

map2_medium_density = np.array([
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', '*', '1', '#', ' ', '#', ' ', '1', '#', '#'],
    ['#', ' ', ' ', '#', ' ', '#', ' ', ' ', '#', '#'],
    ['#', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#', '#'],
    ['#', ' ', '#', '#', ' ', '#', '#', '#', '#', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', '#', ' ', '#', '#', '#', ' ', '#'],
    ['#', ' ', ' ', '#', ' ', '#', ' ', ' ', ' ', '#'],
    ['#', ' ', '1', '#', ' ', '#', ' ', ' ', 'E', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
])

map3_low_density = np.array([
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', '*', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', '1', ' ', '#', ' ', '#', '#', '#', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#'],
    ['#', ' ', '#', '#', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', '1', '#', ' ', ' ', ' ', ' ', ' ', '#', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', ' ', ' ', '#'],
    ['#', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#'],
    ['#', '1', ' ', ' ', '#', ' ', ' ', ' ', 'E', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
])

DIJKSTRA = 1
BFS = 2
A_STAR = 3
GREEDY_BEST_FIRST_SEARCH = 4
GENETIC_ALGORITHM = 5

algorithms = [
    DIJKSTRA,
    BFS,
    A_STAR,
    GREEDY_BEST_FIRST_SEARCH,
    GENETIC_ALGORITHM
]

maps = [
    map1_high_density,
    map2_medium_density,
    map3_low_density
]