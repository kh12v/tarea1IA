import numpy as np
import heapq
from collections import deque
from config import *

def get_cell_cost(val):
    if val in ['1', '2', '3']:
        return 1 + int(val)
    return 1

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
                    # The person steps to (r, c), so they pay the cost of entering (r, c)
                    cost_to_enter = get_cell_cost(mapToUse[r, c])
                    new_dist = dist + cost_to_enter
                    if new_dist < distances[nr, nc]:
                        distances[nr, nc] = new_dist
                        heapq.heappush(pq, (new_dist, nr, nc))
                        
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

    # Distances map from exit using BFS (steps, weight) tie-breaker
    distances = {}
    distances[(exit_pos[0], exit_pos[1])] = (0, 0)
    pq = [(0, 0, exit_pos[0], exit_pos[1])]
    
    while pq:
        steps, weight, r, c = heapq.heappop(pq)
        
        curr_steps, curr_weight = distances.get((r, c), (np.inf, np.inf))
        if steps > curr_steps or (steps == curr_steps and weight > curr_weight):
            continue
            
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if mapToUse[nr, nc] not in ['#', '*']: # valid cell
                    cost_to_enter = get_cell_cost(mapToUse[r, c])
                    new_steps = steps + 1
                    new_weight = weight + cost_to_enter
                    
                    old_steps, old_weight = distances.get((nr, nc), (np.inf, np.inf))
                    
                    if new_steps < old_steps or (new_steps == old_steps and new_weight < old_weight):
                        distances[(nr, nc)] = (new_steps, new_weight)
                        heapq.heappush(pq, (new_steps, new_weight, nr, nc))
                        
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
            
        # Find best neighbor (comparing tuples: steps first, weight second)
        best_dist = distances.get((pr, pc), (np.inf, np.inf))
        best_pos = (pr, pc)
        
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = pr + dr, pc + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                target_val = new_map[nr, nc]
                if target_val not in ['#', '*']:
                    # Check capacity constraint
                    if target_val == 'E' or target_val == ' ' or (target_val in ['1', '2', '3'] and int(target_val) < MAX_PEOPLE_PER_CELL):
                        n_dist = distances.get((nr, nc), (np.inf, np.inf))
                        if n_dist < best_dist:
                            best_dist = n_dist
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

def a_star(mapToUse: np.ndarray, stats: dict):
    rows, cols = mapToUse.shape
    people = []
    exit_pos = None
    
    # Find all people and the exit
    for r in range(rows):
        for c in range(cols):
            val = mapToUse[r, c]
            if val == 'E':
                exit_pos = (r, c)
            elif val in ['1', '2', '3']:
                for _ in range(int(val)):
                    people.append((r, c))
                    
    if not exit_pos or not people:
        return mapToUse

    new_map = np.copy(mapToUse)
    
    for pr, pc in people:
        val = new_map[pr, pc]
        if val in ['1', '2', '3']:
            new_val = str(int(val) - 1)
            new_map[pr, pc] = new_val if new_val != '0' else ' '
        else:
            continue
            
        # Manhattan distance heuristic
        def h(r, c):
            return abs(r - exit_pos[0]) + abs(c - exit_pos[1])
            
        pq = [(h(pr, pc), 0, pr, pc)]
        distances = { (pr, pc): 0 }
        came_from = {}
        
        found = False
        while pq:
            f, g, r, c = heapq.heappop(pq)
            
            if (r, c) == exit_pos:
                found = True
                break
                
            if g > distances.get((r, c), np.inf):
                continue
                
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if mapToUse[nr, nc] not in ['#', '*'] or (nr, nc) == exit_pos:
                        cost_to_enter = get_cell_cost(mapToUse[nr, nc]) if (nr, nc) != exit_pos else 1
                        new_g = g + cost_to_enter
                        if new_g < distances.get((nr, nc), np.inf):
                            distances[(nr, nc)] = new_g
                            came_from[(nr, nc)] = (r, c)
                            heapq.heappush(pq, (new_g + h(nr, nc), new_g, nr, nc))
                            
        best_pos = (pr, pc)
        if found:
            # Reconstruct the path to find the first step
            curr = exit_pos
            path = []
            while curr != (pr, pc):
                path.append(curr)
                curr = came_from.get(curr)
            if path:
                next_step = path[-1] # the first step to take from (pr, pc)
                target_val = new_map[next_step[0], next_step[1]]
                
                # Check capacity constraint
                if target_val == 'E' or target_val == ' ' or (target_val in ['1', '2', '3'] and int(target_val) < MAX_PEOPLE_PER_CELL):
                    best_pos = next_step

        # Move the person
        if best_pos == exit_pos:
            stats["escaped"] += 1
        else:
            target_val = new_map[best_pos[0], best_pos[1]]
            if target_val == ' ':
                new_map[best_pos[0], best_pos[1]] = '1'
            elif target_val in ['1', '2', '3']:
                new_map[best_pos[0], best_pos[1]] = str(int(target_val) + 1)
                
    return new_map

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