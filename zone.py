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

    def __repr__(self) -> str:
        return f"{self.name}"
