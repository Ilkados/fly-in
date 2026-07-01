
from zone import Zone, HubType

from connection import Connection
from typing import Optional
from collections import defaultdict


class Parser:

    def __init__(self, filepath: str) -> None:

        self.filepath: str = filepath

        self.nb_drones: int = 0

        self.zones: dict[str, Zone] = {}

        self.connections: list[Connection] = []

        self.start_zone: Optional[Zone] = None

        self.end_zone: Optional[Zone] = None

        self.seen_coords: dict[tuple[int,int],HubType] = {}



    def _clean_line(self, line: str) -> str:

        return line.split('#')[0].strip()


    def _extract_metadata(self,line: str,line_num: int)->dict[str,str]:
        metadata_dic: dict[str,str]={}

        start_idx = line.find('[')
        end_idx = line.find(']')

        # Case 1: Both brackets are missing entirelyint
        if start_idx == -1 and end_idx == -1:
            return metadata_dic
            
        # Case 2: One bracket is missing, but the other exists
        elif start_idx == -1 or end_idx == -1:
            raise ValueError(f"Parsing error on line {line_num}: Mismatched metadata brackets.")
        metadata_str = line[start_idx+1:end_idx]
        
        pairs = metadata_str.split()
        
        for pair in pairs:
            try:
                key,value = pair.split("=",1)
            except:
                raise ValueError(f"Parsing error on line {line_num}: Invalid metadata syntax '{pair}'")
            metadata_dic[key] = value
        
        return metadata_dic
    
    def _parse_nb_drones(self, line: str, line_num: int) -> None:

        parts_list = line.split(':')

        try:

            self.nb_drones = int(parts_list[1])

        except ValueError:

            raise ValueError(f"Parsing error on line {line_num}: Number of drones must be an integer.")

        

    def _parse_hub(self, line: str, line_num: int) -> None:
        parts = line.split()

        if parts[0] == "start_hub:":

            hub_type = HubType.START

        elif parts[0] == "end_hub:":

            hub_type = HubType.END

        elif parts[0] == "hub:":

            hub_type = HubType.REGULAR

        else:

            return

        name = parts[1]
        if name in self.zones:
            raise ValueError (f"Parsing error on line {line_num}: names duplicates")
        try:

            x = int(parts[2])

            y = int(parts[3])

        except ValueError:

            raise ValueError(f"Parsing error on line {line_num}: Coordinates must be integers.")
        
        my_tuple = (x,y)
        if my_tuple in self.seen_coords.keys():
            
            existing_type = self.seen_coords[my_tuple]
    
            if existing_type == HubType.START and hub_type == HubType.END:
                self.seen_coords[my_tuple] = HubType.BOTH
            
            elif existing_type == HubType.END and hub_type == HubType.START:
                self.seen_coords[my_tuple] = HubType.BOTH
            else:
                raise ValueError (f"Parsing error on line {line_num} Coordinates must be unique")
        else:
            self.seen_coords[my_tuple]=hub_type
        
    
        metadata = self._extract_metadata(line, line_num)
        
    
        color = metadata.get("color", "none")
        
        zone_type = metadata.get("zone", "normal")
        if zone_type not in ("normal", "blocked", "restricted", "priority"):
            raise ValueError(f"Parsing error on line {line_num}: invalid zone type.")

    
        raw_capacity = metadata.get("max_drones", None)
        max_drones = None
        
        if raw_capacity is not None:
            try:
                max_drones = int(raw_capacity)
            except ValueError:
                raise ValueError(f"Parsing error on line {line_num}: max_drones must be an integer.")
            
            if max_drones <= 0:
                raise ValueError(f"Parsing error on line {line_num}: max_drones must be a positive integer.")
        
        # Object Instantiation
        new_zone = Zone(name, x, y, hub_type, zone_type, color, max_drones)

        if hub_type == HubType.START:
            if self.start_zone is not None:
                raise ValueError(f"Parsing error on line {line_num}: Multiple start hubs defined.")
            self.start_zone = new_zone

        elif hub_type == HubType.END:
            if self.end_zone is not None:
                raise ValueError(f"Parsing error on line {line_num}: Multiple end hubs defined.")
            self.end_zone = new_zone
        self.zones[name] = new_zone


    def _parse_connection(self, line: str, line_num: int) -> None:
        parts = line.split()
        if len(parts) < 2:
            raise ValueError(f"Parsing error on line {line_num}: Connection missing hubs.")
        two_names = parts[1].split('-')
        if len(two_names) != 2:
            raise ValueError(f"Parsing error on line {line_num}: Connection must be formatted as HubA-HubB.")
        
        hub_a = two_names[0]
        hub_b = two_names[1]
        
        if hub_a not in self.zones or hub_b not in self.zones:
            raise ValueError(f"Parsing error on line {line_num}: Unknown hub in connection.")
    
        
        metadata = self._extract_metadata(line,line_num)

        raw_max_link_capacity = metadata.get("max_link_capacity","1")
        
        try:
            max_link_capacity = int(raw_max_link_capacity)
            if max_link_capacity <= 0:
                raise ValueError(f"Parsing error on line {line_num}: Capacity must be > 0.")
        except ValueError:
            raise ValueError(f"Parsing error on line {line_num}: Capacity must be an integer.")

        zone_a = self.zones[hub_a]
        zone_b = self.zones[hub_b]

        new_connection = Connection(zone_a, zone_b,max_link_capacity)
        self.connections.append(new_connection)
        
    def parse(self) -> None:

        has_nb_drones: bool = False
        try:
            with open(self.filepath, 'r') as file:
                for line_num, line in enumerate(file, start=1):

                    cleaned_line = self._clean_line(line)

                    if cleaned_line == "":
                        continue

                    if cleaned_line.startswith("nb_drones:"):

                        has_nb_drones = True   
                        self._parse_nb_drones(cleaned_line, line_num)
                        continue

                    if not has_nb_drones:
                        raise ValueError(f"Parsing error on line {line_num}: The first valid line must define 'nb_drones:'")
                    
                    if cleaned_line.startswith(("start_hub:", "end_hub:", "hub:")):
                        self._parse_hub(cleaned_line, line_num)
                        continue

                    if cleaned_line.startswith(("connection")):
                        self._parse_connection(cleaned_line,line_num)
        except FileNotFoundError as e:
            system_message = str(e)
            raise ValueError(f"Parsing error: Could not load map. {system_message}") from None
        if not has_nb_drones:
            raise ValueError("Parsing error: File is empty or missing 'nb_drones:'.")
        
        start_count  = 0
        end_count = 0
        for zone in self.zones.values():
            if zone.hub_type == HubType.START:
                start_count+=1
            elif zone.hub_type == HubType.END:
                end_count +=1

        
        if start_count !=1 or end_count !=1:
            raise ValueError("Parsing error: Map must have exactly ONE Start_hub and End_hub.")