from connection import Connection
from zone import Zone


class Graph:
    def __init__(
        self, zones: dict[str, Zone], connections: list[Connection]
    ) -> None:
        # ROLE: Stores all the zones (cities) parsed from the file.
        self.zones: dict[str, Zone] = zones

        # ROLE: Stores the raw list of roads. We only use this list ONCE
        # to build the dictionaries below.
        self.raw_connections: list[Connection] = connections

        # ROLE: The Pathfinder's Map. Connects a Zone to a list of its
        # neighbors.
        self.adjacency_list: dict[Zone, list[Zone]] = {}

        # ROLE: The Simulator's Fast-Lookup. Connects a tuple of
        # (Zone, Zone) directly to the road object.
        self.connection_map: dict[tuple[Zone, Zone], Connection] = {}

        # ROLE: Automatically triggers the function below to fill up the
        # dictionaries.
        self._build_adjacency_list()

    def _build_adjacency_list(self) -> None:
        # STEP 1: Prepare an empty list of neighbors for every single zone
        # on the map.
        for zone in self.zones.values():
            self.adjacency_list[zone] = []

        # STEP 2: Loop through the raw list of connections one by one.
        for conn in self.raw_connections:
            zone1 = conn.zone_a
            zone2 = conn.zone_b

            # --- FILLING THE PATHFINDER'S MAP ---
            # ROLE: Tell Zone 1 that Zone 2 is a neighbor.
            self.adjacency_list[zone1].append(zone2)
            # ROLE: Tell Zone 2 that Zone 1 is a neighbor (because roads
            # are two-way).
            self.adjacency_list[zone2].append(zone1)

            # --- FILLING THE SIMULATOR'S FAST-LOOKUP ---
            # ROLE: Save the Connection object so it can be found instantly
            # from either direction. If a drone flies A->B or B->A, they
            # both hit the exact same road object!
            self.connection_map[(zone1, zone2)] = conn
            self.connection_map[(zone2, zone1)] = conn

    def get_neighbors(self, zone: Zone) -> list[Zone]:
        # ROLE: Hand this to your Pathfinding Algorithm so it can explore
        # the map.
        return self.adjacency_list.get(zone, [])

    def get_connection(self, zone1: Zone, zone2: Zone) -> Connection:
        # ROLE: Hand this to your Simulator. The Simulator passes in two
        # zones, and this function instantly returns the exact Connection
        # object in O(1) time.
        # Direct access — if the road doesn't exist, this is a bug and
        # should crash loudly (fail-fast).
        return self.connection_map[(zone1, zone2)]
