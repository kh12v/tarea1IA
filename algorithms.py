import numpy as np
import heapq
from config import *

def dijkstra(mapToUse: np.ndarray, stats: dict):
    # Find all people and the exit
    rows, cols = mapToUse.shape
    people = [] # list of (r, c)
    exit_pos = None
    
    for r in range(rows):
        for c in range(cols):
            val = mapToUse[r, c]
            if val == 'E':
                exit_pos = (r, c)
            elif val in ['1', '2', '3']:
                # store the position multiple times if there are multiple people
                for _ in range(int(val)):
                    people.append((r, c))
                    
    if not exit_pos or not people:
        return mapToUse

    # Distances map from exit
    distances = np.full((rows, cols), np.inf)
    distances[exit_pos[0], exit_pos[1]] = 0
    pq = [(0, exit_pos[0], exit_pos[1])]
    
    while pq:
        dist, r, c = heapq.heappop(pq)
        
        if dist > distances[r, c]:
            continue
            
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if mapToUse[nr, nc] not in ['#', '*']: # valid cell
                    if distances[nr, nc] > dist + 1:
                        distances[nr, nc] = dist + 1
                        heapq.heappush(pq, (dist + 1, nr, nc))
                        
    # Now we move people sequentially
    new_map = np.copy(mapToUse)
    
    for pr, pc in people:
        # Check if the person is still at (pr, pc) in new_map
        val = new_map[pr, pc]
        if val in ['1', '2', '3']:
            new_val = str(int(val) - 1)
            new_map[pr, pc] = new_val if new_val != '0' else ' '
        else:
            continue
            
        # Find best neighbor
        best_dist = distances[pr, pc]
        best_pos = (pr, pc)
        
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = pr + dr, pc + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                target_val = new_map[nr, nc]
                if target_val not in ['#', '*']:
                    # Check capacity constraint
                    if target_val == 'E' or target_val == ' ' or (target_val in ['1', '2', '3'] and int(target_val) < MAX_PEOPLE_PER_CELL):
                        if distances[nr, nc] < best_dist:
                            best_dist = distances[nr, nc]
                            best_pos = (nr, nc)
                            
        # Move the person
        if best_pos == exit_pos:
            stats["escaped"] += 1
            # They exit, do not add them back to the grid
        else:
            target_val = new_map[best_pos[0], best_pos[1]]
            if target_val == ' ':
                new_map[best_pos[0], best_pos[1]] = '1'
            elif target_val in ['1', '2', '3']:
                new_map[best_pos[0], best_pos[1]] = str(int(target_val) + 1)
                
    return new_map

def bfs(mapToUse: np.ndarray, stats: dict):
    return mapToUse

def a_star(mapToUse: np.ndarray, stats: dict):
    return mapToUse

def greedy_best_first_search(mapToUse: np.ndarray, stats: dict):
    return mapToUse

def genetic_algorithm(mapToUse: np.ndarray, stats: dict):
    return mapToUse

def algoIteration(algo: int, mapToUse: np.ndarray, stats: dict):
    if algo == DIJKSTRA:
        return dijkstra(mapToUse, stats)
    elif algo == BFS:
        return bfs(mapToUse, stats)
    elif algo == A_STAR:
        return a_star(mapToUse, stats)
    elif algo == GREEDY_BEST_FIRST_SEARCH:
        return greedy_best_first_search(mapToUse, stats)
    elif algo == GENETIC_ALGORITHM:
        return genetic_algorithm(mapToUse, stats)
    else:
        return mapToUse