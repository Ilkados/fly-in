from collections import deque 
from grapth import Graph
from zone import Zone

def bfs(graph: Graph, start: Zone, end: Zone) -> list[Zone]:
    queue = deque([start])   # Create queue and put 'start' inside
    visited = {start}        # Create set and put 'start' inside
    parent = {start: None}   # Create dict and map 'start' to None
    
    # What comes next?
    #the loop  for queue

    while queue:
        current  = queue.popleft()
        neighbors = graph.get_neighbors(current)
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.append(current)
                parent[neighbor]= current
                queue.add(neighbor)

The Loop: While the queue is not empty, popleft() the current zone.

The Goal Check: If the current zone is the end zone, you found the shortest path! (For now, you can just pass or write a comment here—we can build the path-reconstruction step afterward).

The Neighbors: Loop through the neighbors of the current zone. Apply the Golden Rule: If a neighbor is not in visited, mark it visited, record its parent, and append it to the queue.