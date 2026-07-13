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

    def resolve_and_move(self, wishes: dict[Zone, list[Drone]]) -> list[tuple[Drone, Zone, Zone]]:
        
        report: list[tuple[Drone,Zone,Zone]] = []
        link_usage: dict[Connection,int] = {}

        while True:
            # We use this to track if we need to run another pass
            moved_someone: bool = False
            
            for target_zone, candidate_drones in wishes.items():
                
                for drone in candidate_drones.copy():

                    current_zone = drone.current_zone
                    connection = self.graph.get_connection(current_zone, target_zone)

                    # 1. Check the Bridge
                    current_traffic = link_usage.get(connection, 0)
                    bridge_has_space = (current_traffic + 1) <= connection.max_link_capacity

                    # 2. Check the live Zone (NO len() here!)
                    current_parked = target_zone.current_drones
                    zone_has_space = (current_parked < target_zone.max_drones)

                    # 3. IF both are true, do the actions
                    if bridge_has_space and zone_has_space: 
                        
                        # --- EVERYTHING BELOW IS INDENTED TOGETHER ---
                        link_usage[connection] = current_traffic + 1 

                        # Apply the physical move
                        current_zone.current_drones -= 1
                        target_zone.current_drones += 1
                        drone.current_zone = target_zone
                        drone.path.pop(0)

                        # Log the receipt, remove from waiting list, ring the bell
                        report.append((drone, current_zone, target_zone))
                        candidate_drones.remove(drone)
                        moved_someone = True
                        # ---------------------------------------------
            
            # This is OUTSIDE the for loops, but INSIDE the while loop
            if not moved_someone: 
                break
                
        # This is OUTSIDE the while loop completely
        return report
                    
    def step(self) -> list[tuple[Drone, Zone, Zone]]:
        """Runs one simultaneous turn: collects intentions, resolves traffic, applies moves."""
        
        wishes = self.collect_wishes()
        
        report = self.resolve_and_move(wishes)
        
        if len(report) > 0: 
            self.turn_count += 1
        return report 
    
    def check_simulation_result(self,drones:list[Drone])-> bool:
        we_won = True
        for drone in drones: 
            if not drone.has_arrived():
                we_won = False
                break
        return we_won

                