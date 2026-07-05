from zone import Zone
from connection import Connection


class Graph:
    def __init__(self, zones: dict[str, Zone], connections: list[Connection]) -> None:
        self.zones: dict[str, Zone] = zones
        self.raw_connections: list[Connection] = connections
        
        # Pure Object-to-Object mapping
        self.adjacency_list: dict[Zone, list[Zone]] = {}
        
        self._build_adjacency_list()

    def _build_adjacency_list(self) -> None:
        for zone in self.zones.values():
            self.adjacency_list[zone] = []
            
        for conn in self.raw_connections:
            zone1 = conn.zone_a
            zone2 = conn.zone_b

            self.adjacency_list[zone1].append(zone2)
            self.adjacency_list[zone2].append(zone1)
    
    def get_neighbors(self, zone: Zone) -> list[Zone]:
        return self.adjacency_list.get(zone, [])