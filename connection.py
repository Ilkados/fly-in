from zone import Zone
from zone import HubType
class Connection:
    def __init__(self, zone_a: Zone, zone_b: Zone, max_link_capacity: int = 1) -> None:    # Pointers to the actual Zone objects
        self.zone_a = zone_a
        self.zone_b = zone_b

        # Built from the two zone names, e.g. "corridorA-tunnelB"
        self.name: str = f"{self.zone_a.name}-{self.zone_b.name}"

        # The physical limit of this specific path
        self.max_link_capacity = max_link_capacity

        # State tracking: how many drones are currently traversing this connection
        self.current_drones: int = 0
if __name__ == "__main__":
    print("---Starting Manual Test---")

    zone1 = Zone("spawn",0,1,HubType.START)
    zone2 = Zone("roof1",0,2,HubType.REGULAR)
    connect = Connection(zone1,zone2,2)
    
    print(connect.name)
    print(zone1.max_drones)
    print(zone2.max_drones)
    print(type(zone1.max_drones))
    