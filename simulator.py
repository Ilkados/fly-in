from graph import Graph
from drone import Drone
from zone import Zone
from connection import Connection
class Simulator:
    def __init__(self, graph: Graph, drones: list[Drone]) -> None:
        self.graph: Graph = graph
        self.drones: list[Drone] = drones
        self.turn_count: int = 0

    def collect_wishes(self)-> dict[Zone,list[Drone]]:
        wishes: dict[Zone,list[Drone]]={}

        for drone in self.drones:

            if drone.has_arrived():
                continue

            next_zone = drone.get_next_zone()
            
            wishes.setdefault(next_zone,[]).append(drone)
        
        return wishes

    def take_snapshot(self)->dict[Zone,int]:
        snapshot: dict[Zone,int] = {}
        for zone in self.graph.zones.values():
            snapshot[zone] = zone.current_drones
        return snapshot

    def resolve_and_move(self, wishes: dict[Zone, list[Drone]], snapshot: dict[Zone, int]) -> list[tuple[Drone, Zone, Zone]]:
        report: list[tuple[Drone, Zone, Zone]] = []

        # THE BOUNCER'S CLICKER: Tracks how many drones use each tunnel during this single step
        link_usage: dict[Connection, int] = {} 

        for target_zone, candidate_drones in wishes.items():
            # Calculate exactly how many spots are open right now
            free_slots = target_zone.max_drones - snapshot[target_zone]

            # If the zone is already full, skip it completely
            if free_slots <= 0:
                continue

            parked_drones = 0 

            # Loop through every candidate so we don't waste empty slots
            for drone in candidate_drones:
                current_zone = drone.current_zone

                # 1. Grab the Connection object in O(1) time
                # (Adjust this line to match how your Graph class is built!)
                connection = self.graph.get_connection(current_zone, target_zone)

                # 2. Get the road's capacity. If it doesn't have one, default to 1 (Safe/Strict mode)
                max_capacity = connection.max_link_capacity

                # 3. Check the Bouncer's clicker for this specific connection
                current_traffic = link_usage.get(connection, 0)

                # THE TUNNEL CHECK (Edge Capacity)
                if current_traffic + 1 > max_capacity:
                    # The tunnel is physically full for this turn! Block the drone.
                    continue 

                # Safe to cross! Click the counter up by 1.
                link_usage[connection] = current_traffic + 1

                # Apply the physical move
                current_zone.current_drones -= 1
                target_zone.current_drones += 1
                drone.current_zone = target_zone
                drone.path.pop(0)

                # Log the receipt and count the successful park
                report.append((drone, current_zone, target_zone))
                parked_drones += 1

                # THE PARKING LOT CHECK (Vertex Capacity)
                if parked_drones == free_slots:
                    # The zone is now completely full. Stop letting drones in.
                    break

        return report
    
   
    
    def step(self) -> list[tuple[Drone, Zone, Zone]]:
        """Runs one simultaneous turn: collects intentions, resolves traffic, applies moves."""
        self.turn_count += 1
        
        snapshot = self.take_snapshot()
       
        wishes = self.collect_wishes()
        
        report = self.resolve_and_move(wishes,snapshot)
        
        return report 

