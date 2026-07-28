import sys

from drone import Drone
from graph import Graph
from parser import Parser
from simulator import Simulator
from yens_algorithm import yens_all_paths
from zone import Zone


# --- ANSI Color Codes ---
GREEN = "\033[92m"
BLUE = "\033[94m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
PURPLE = "\033[38;5;129m"

# --- ANSI Text Styles ---
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
RESET = "\033[0m"

# --- ANSI Translator Dictionary ---
COLOR_MAP = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "cyan": "\033[96m",
    "orange": "\033[38;5;208m",
    "none": "\033[0m"
}


def print_zone_states(graph: Graph) -> None:
    print(f"\n{CYAN}--- ZONE STATES ---{RESET}")

    for zone_name, zone in graph.zones.items():
        if zone.current_drones > 0:
            # Get the color and apply it to the printed string
            z_color = COLOR_MAP[zone.color]
            print(
                f"  {z_color}{zone.name}{RESET}: "
                f"[{zone.current_drones} / {zone.max_drones}] drones"
            )


def print_connection_states(graph: Graph) -> None:
    print(f"\n{MAGENTA}--- CONNECTION STATES ---{RESET}")

    for connection in graph.raw_connections:
        if connection.current_drones > 0:
            print(
                f"  {connection.name}: "
                f"[{connection.current_drones}/ "
                f"{connection.max_link_capacity}]drones"
            )


def paths_conflict(path1: list[Zone], path2: list[Zone]) -> bool:
    middle_zones1 = path1[1:-1]
    middle_zones2 = path2[1:-1]

    shared_zones = set(middle_zones1) & set(middle_zones2)

    for zone in shared_zones:
        if zone.max_drones == 1:
            return True

    return False


def build_highway_group(all_paths: list[list[Zone]]) -> list[list[Zone]]:
    safe_group = [all_paths[0]]

    for new_path in all_paths[1:]:
        is_safe = True

        for existing_path in safe_group:
            if paths_conflict(new_path, existing_path):
                is_safe = False
                break

        if is_safe:
            safe_group.append(new_path)

    return safe_group


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python main.py <map_file.txt>")
        sys.exit(1)

    parser = Parser(sys.argv[1])
    parser.parse()

    graph = Graph(parser.zones, parser.connections)

    # --- 1. ASK YEN'S FOR EVERY PATH ---
    print("\n--- COLOR MENU ---")
    print(f"  {BLUE}Blue{RESET}   = Drone ID")
    print(f"  {GREEN}Green{RESET}  = Normal Movement")
    print(f"  {YELLOW}Yellow{RESET} = Takeoff")
    print(f"  {CYAN}Cyan{RESET}   = Landing / Goal Reached")
    print("------------------\n")
    print("Calculating all possible routes...")

    start_z = parser.start_zone
    goal_z = parser.zones["goal"]

    yens_results = yens_all_paths(graph, start_z, goal_z)

    all_paths = []
    for cost, path in yens_results:
        all_paths.append(path)

    print(f"Found {len(all_paths)} different safe routes to the goal!")

    # --- NEW CODE: Filter for the safe highway group ---
    safe_paths = build_highway_group(all_paths)
    print(
        f"Filtered down to {len(safe_paths)} non-overlapping highway paths!"
    )

    # --- 2. SPAWN THE DRONES & MANAGE TRAFFIC ---
    my_drones = []
    # TELL MYPY : i guarantee the parser found a start zone
    assert parser.start_zone is not None
    for i in range(parser.nb_drones):
        d_id = f"Drone_{i + 1}"
        assigned_path = safe_paths[i % len(safe_paths)]
        final_path_for_drone = assigned_path[1:]

        new_drone = Drone(d_id, parser.start_zone, final_path_for_drone)
        my_drones.append(new_drone)

    # --- 3. START THE SIMULATOR ---
    simulator = Simulator(graph, my_drones)

    print("\n--- STARTING SIMULATION ---")

    # --- 4. THE GAME LOOP ---
    while True:
        report = simulator.step()

        if len(report) == 0:
            print("\n--- END OF GAME ---")

            result = simulator.get_stuck_drones()
            if not result:
                print(
                    f"✅ {GREEN}VICTORY! All drones arrived safely in "
                    f"{simulator.turn_count} turns.{RESET}"
                )
            else:
                print("❌ DEADLOCK ERROR! Not all drones reached the goal.\n")
                for stuck_drone in result:
                    print(
                        f"drone {stuck_drone.drone_id} at zone "
                        f"{stuck_drone.current_zone.name}"
                    )
            break

        # Formatting the turn header
        print(
            f"\n{BOLD}{UNDERLINE}Turn"
            f"{simulator.turn_count} Results:{RESET}"
        )

        # Printing system states
        print_zone_states(graph)
        print_connection_states(graph)

        # Printing movement logs
        print(f"\n{PURPLE}-- MOVING_STATE --{RESET}")
        for moved_drone, old_zone, new_zone, action_type in report:
            zone_O_c = COLOR_MAP[old_zone.color]
            zone_N_c = COLOR_MAP[new_zone.color]

            if action_type == "normal":
                print(
                    f"  {GREEN}[SUCCESS]{RESET} {BLUE}{moved_drone.drone_id}"
                    f"{RESET} moved from {zone_O_c}{old_zone.name}{RESET} to "
                    f"{zone_N_c}{new_zone.name}{RESET}"
                )

            elif action_type == "takeoff":
                print(
                    f"  {YELLOW}[SUCCESS]{RESET} {BLUE}{moved_drone.drone_id}"
                    f"{RESET} moved to connection {zone_O_c}{old_zone.name}"
                    f"{RESET}-{zone_N_c}{new_zone.name}{RESET}"
                )

            elif action_type == "landing":
                print(
                    f"  {CYAN}[SUCCESS]{RESET} {BLUE}{moved_drone.drone_id}"
                    f"{RESET} arrived at {zone_N_c}{new_zone.name}{RESET}"
                )
