from enum import Enum
from typing import Optional, Union


class HubType(Enum):
    START = 1
    END = 2
    REGULAR = 3
    BOTH = 4


class Zone:
    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        hub_type: HubType,
        zone_type: str = "normal",
        color: str = "none",
        max_drones: Optional[int] = None,
    ) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.hub_type = hub_type
        self.color = color

        self.max_drones: Union[int, float]

        if max_drones is not None:
            self.max_drones = max_drones
        else:
            if self.hub_type in (HubType.START, HubType.END):
                self.max_drones = float('inf')
            else:
                self.max_drones = 1

        self.current_drones: int = 0
    def __str__(self):
        return f"zone {self.name} , {self.color}, {self.x, self.y}"


if __name__ == "__main__":
    print("---Starting Manual Test---")

    zone1 = Zone("spawn", 0, 1, HubType.START)
    zone2 = Zone("roof1", 0, 2, HubType.REGULAR)

    print(zone1.max_drones)
    print(zone2.max_drones)
    print(type(zone1.max_drones))