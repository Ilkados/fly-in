import heapq
from graph import Graph
from zone import Zone

def zone_cost(zone: Zone) -> int:
    result = 100
    if zone.zone_type == "priority":
        result = 99
    elif zone.zone_type == "restricted":
        result = 200
    return result

def dijkstra(graph: Graph, start: Zone, end: Zone) -> list[Zone]:
    # 1. SETUP
    pq = [(0, start)]
    distance = {start: 0}
    parent = {start: None}

    # 2. THE ENGINE
    while pq:
        current_cost, current = heapq.heappop(pq)
        
        # The Trash Can: skip stale tickets with old, bad costs
        if current_cost > distance.get(current, float('inf')):
            continue

        # If we hit the goal, stop spreading!
        if current == end:
            break

        neighbors_zones = graph.get_neighbors(current)

        # Check all neighbors
        for neighbor in neighbors_zones:
            old_cost = distance.get(neighbor, float('inf'))
            new_cost = current_cost + zone_cost(neighbor)

            # If we found a cheaper route, update everything
            if new_cost < old_cost:
                distance[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(pq, (new_cost, neighbor))

    # 3. PATH RECONSTRUCTION
    # Protect against KeyError if the end zone is unreachable
    if end not in parent:
        return []

    # Walk backward from the end to the start
    path = []
    step = end
    while step is not None:
        path.append(step)
        step = parent[step]
    
    # Flip it so it goes Start -> End
    path.reverse()
    
    return path