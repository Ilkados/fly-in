from graph import Graph
from drone import Drone
from zone import Zone
from connection import Connection
class Simulator:
    def __init__(self, graph: Graph, drones: list[Drone]) -> None:
        self.graph: Graph = graph
        self.drones: list[Drone] = drones
        self.turn_count: int = 0

    def collect_wishes(self,landed_drones)-> dict[Zone,list[Drone]]:
        wishes: dict[Zone,list[Drone]]={}

        for drone in self.drones:
            
            if drone in landed_drones:
                continue
            if drone.has_arrived():
                continue

            next_zone = drone.get_next_zone()
            
            wishes.setdefault(next_zone,[]).append(drone)
        return wishes

    def normal_step(self,drone:Drone,target_zone:Zone):
        # Apply the physical move
        current_zone = drone.current_zone
        current_zone.current_drones -= 1
        target_zone.current_drones += 1
        drone.current_zone = target_zone
        drone.path.pop(0)


    def restricted_step(self, drone: Drone, target_zone: Zone) -> None:
        # 1. Free up the old parking spot
        drone.current_zone.current_drones -= 1
        
        # 2. Reserve the new parking spot
        target_zone.current_drones += 1
        
        # 3. Put the drone in the air (do NOT pop the path yet!)
        drone.transit_target = target_zone
    
    def land_transit_drones(self):
        landing_reports = []  # 1. Create an empty list for this turn's landings

        for drone in self.drones:
            if drone.transit_target is not None:
                # Remember where we came from before we move
                old_zone = drone.current_zone
                target_zone = drone.transit_target
                
                # Move the drone (your existing code)
                drone.current_zone = target_zone
                drone.path.pop(0)
                drone.transit_target = None
                
                # 2. Add the secret tag for landing!
                landing_reports.append((drone, old_zone, target_zone, "landing"))
                
        return landing_reports  # 3. Send the list back

    def resolve_and_move(self, wishes: dict[Zone, list[Drone]]) -> list[tuple[Drone, Zone, Zone]]:
        
        report: list[tuple[Drone,Zone,Zone,str]] = []
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

                            if target_zone.zone_type == "normal":
                                self.normal_step(drone,target_zone)
                                report.append((drone, current_zone, target_zone,"normal"))
                            elif target_zone.zone_type == "restricted":
                                self.restricted_step(drone,target_zone)
                                report.append((drone, current_zone, target_zone,"takeoff"))
                            # Log the receipt, remove from waiting list, ring the bell
                            candidate_drones.remove(drone)
                            moved_someone = True
            
            # This is OUTSIDE the for loops, but INSIDE the while loop
            if not moved_someone: 
                break
                
        # This is OUTSIDE the while loop completely
        return report

     # here our step  that return list of tuple of all drone want to make step from its current zone into target zone               
    def step(self):
        # 1. Get the landing list from the Air Traffic Controller
        landing_reports = self.land_transit_drones()
        
        # 2. Create the "Do Not Disturb" list! (Pull just the drone from the tuple)
        landed_drones = [report[0] for report in landing_reports]
        
        # 3. Hand the Do Not Disturb list to the Post Office
        wishes = self.collect_wishes(landed_drones)
        
        # 4. Ask the Bouncer to resolve the normal moves and takeoffs
        move_reports = self.resolve_and_move(wishes)
        
        # 5. Staple the lists together into the master basket
        master_report = landing_reports + move_reports
        
        self.turn_count += 1
        
        return master_report
     
    def check_simulation_result_and_return_stuck_drones(self)-> list[Drone]:
        result: list[Drone] = []
        for drone in self.drones:
            if not drone.has_arrived():
                result.append(drone)
        return result


                