from graph import Graph
from drone import Drone
from zone import Zone

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
    
    def resolve_and_move(self, wishes: dict[Zone, list[Drone]],snapshot: dict[Zone,int]) -> list[tuple[Drone, Zone, Zone]]:
        report: list[tuple[Drone, Zone, Zone]] = []

        for target_zone, candidate_drones in wishes.items():
            free_slots = target_zone.max_drones - snapshot[target_zone]
            winners = candidate_drones[:free_slots]

            for drone in winners:
                old_zone = drone.current_zone

                # Apply the move physically
                old_zone.current_drones -= 1
                target_zone.current_drones += 1
                drone.current_zone = target_zone
                drone.path.pop(0)

                # Append as ONE tuple (double parentheses)
                report.append((drone, old_zone, target_zone))

        return report 
    
    def take_snapshot(self)->dict[Zone,int]:
        snapshot: dict[Zone,int] = {}
        for zone in self.graph.zones.values():
            snapshot[zone] = zone.current_drones
        return snapshot
    
    def step(self) -> list[tuple[Drone, Zone, Zone]]:
        """Runs one simultaneous turn: collects intentions, resolves traffic, applies moves."""
        self.turn_count += 1
        
        snapshot = self.take_snapshot()
       
        wishes = self.collect_wishes()
        
        report = self.resolve_and_move(wishes,snapshot)
        
        return report

