import heapq
import itertools
from graph import Graph
from zone import Zone


def zone_cost(zone: Zone) -> int:
    result = 100
    if zone.zone_type == "priority":
        result = 99
    elif zone.zone_type == "restricted":
        result = 200
    return result

def get_path_cost(path: list[Zone]) -> int:
    """Helper to calculate the exact gas cost of a fully glued path."""
    if not path:
        return 0
    total = 0
    # We skip index 0 because Dijkstra treats the start node as cost 0
    for i in range(1, len(path)):
        total += zone_cost(path[i])
    return total

def dijkstra(graph: Graph, start: Zone, end: Zone, ignored_nodes: list[Zone] | None = None, ignored_edges: list[tuple[Zone, Zone]] | None = None) -> tuple[float, list[Zone]]:
    if ignored_nodes is None:
        ignored_nodes = []
    if ignored_edges is None:
        ignored_edges = []

    # 1. SETUP
    counter = itertools.count()
    pq: list[tuple[float, int, Zone]] = [(0, next(counter), start)]
    distance: dict[Zone, float] = {start: 0}
    parent: dict[Zone, Zone | None] = {start: None}

    # 2. THE ENGINE
    while pq:
        current_cost, _, current = heapq.heappop(pq)

        if current_cost > distance.get(current, float('inf')):
            continue

        if current == end:
            break

        neighbors_zones = graph.get_neighbors(current)

        for neighbor in neighbors_zones:
            if neighbor.zone_type == "blocked":
                continue
            
            if neighbor in ignored_nodes:
                continue
                
            if (current, neighbor) in ignored_edges:
                continue

            old_cost = distance.get(neighbor, float('inf'))
            new_cost = current_cost + zone_cost(neighbor)

            if new_cost < old_cost:
                distance[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(pq, (new_cost, next(counter), neighbor))

    # 3. PATH RECONSTRUCTION
    if end not in parent:
        return float('inf'), []

    path: list[Zone] = []
    step: Zone | None = end
    while step is not None:
        path.append(step)
        step = parent[step]

    path.reverse()

    return distance[end], path

def yens_all_paths(graph, start, end)->list[list[Zone]]:
    The_Winner = []
    The_Waiting_Room = []

    # 1. Get the absolute best path
    first_cost, first_path = dijkstra(graph, start, end)
    if not first_path: 
        return []
        
    The_Winner.append((first_cost, first_path))
    
    # 2. THE MASTER LOOP (Find all paths)
    while True:
        last_winner_cost, last_winner_path = The_Winner[-1]
        
        for i in range(len(last_winner_path) - 1):
            spur_node = last_winner_path[i]
            
            root_path = last_winner_path[:i + 1] 
            
            ignored_nodes = last_winner_path[:i]
            
            ignored_edges = []
            for w_cost, w_path in The_Winner:
                if w_path[:i + 1] == root_path:
                    next_node = w_path[i + 1]
                    ignored_edges.append((spur_node, next_node))
            
            # CALL DIJKSTRA
            spur_cost, spur_path = dijkstra(graph, spur_node, end, ignored_nodes, ignored_edges)

            if spur_path: # If Dijkstra actually found a way out
                
                # GLUE THEM TOGETHER (skipping the duplicate spur_node)
                total_path = root_path + spur_path[1:]

                # USE THE HELPER TO GET THE EXACT COST
                total_cost = get_path_cost(total_path)

                # PREVENT DUPLICATES: Only add if it's not already in the waiting room
                new_candidate = (total_cost, total_path)
                if new_candidate not in The_Waiting_Room and new_candidate not in The_Winner:
                    The_Waiting_Room.append(new_candidate)
        
        # --- THE BOSS PICKS THE NEXT WINNER ---
        # 1. Check if the Waiting Room is empty (if so, break!)
        if not The_Waiting_Room:
            break
            
        # 2. Sort the Waiting Room (Puts the lowest cost at index 0)
        The_Waiting_Room.sort(key = lambda item : item[0])
        
        # 3. Pop the cheapest path and append it to The_Winner
        best_detour = The_Waiting_Room.pop(0)
        The_Winner.append(best_detour)

    # Return the final list of every possible path!
    return The_Winner