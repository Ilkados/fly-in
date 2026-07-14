from zone import Zone


class Drone:
    def __init__(self, drone_id: str, current_zone: Zone, path: list[Zone]) -> None:
        self.drone_id: str = drone_id
        self.current_zone: Zone = current_zone
        
        # Give the drone its own independent copy of the master flight plan
        self.path: list[Zone] = path.copy()

        self.current_zone.current_drones +=1
        self.transit_target = None

    def __repr__(self) -> str:
        return f"Drone({self.id} @ {self.current_zone.name})"
    
    def get_next_zone(self) -> Zone:
        if not self.path:
            return None
        else:
            return self.path[0]
    def has_arrived(self) -> bool:
        return (len(self.path)==0)
    
  