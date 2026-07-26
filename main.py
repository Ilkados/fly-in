import sys

from drone import Drone
from graph import Graph
from parser import Parser
from simulator import Simulator
from yens_algorithm import yens_all_paths  # <-- IMPORT YOUR NEW ENGINE!

if __name__ == "__main__":
    # 1. Flip the map to the real one!
    if len(sys.argv) != 2:
        print("usage: python main.py <map_file.txt")
        sys.exit(1)
    parser = Parser(sys.argv[1])
    parser.parse()

    graph = Graph(parser.zones, parser.connections)

    # --- 1. ASK YEN'S FOR EVERY PATH ---
    print("Calculating all possible routes...")
    start_z = parser.start_zone
    goal_z = parser.zones["goal"] 
    
    # Yen's returns a list of tuples: [ (cost1, path1), (cost2, path2)... ]
    yens_results = yens_all_paths(graph, start_z, goal_z)
    
    # We only care about the paths, so let's extract them into a clean list
    all_paths = []
    for cost, path in yens_results:
        all_paths.append(path)
        
    print(f"Found {len(all_paths)} different safe routes to the goal!")

    # --- 2. SPAWN THE DRONES & MANAGE TRAFFIC ---
    my_drones: list[Drone] = []
    for i in range(parser.nb_drones):
        d_id = f"Drone_{i + 1}"

        # THE DEALER: Round-Robin Distribution
        # The modulo operator (%) perfectly deals out paths 1, 2, 3, 1, 2, 3...
        assigned_path = all_paths[i % len(all_paths)]

        # SLICE OFF THE START NODE!
        # Your Yen's algorithm returns the full path: [Start, ZoneA, Goal]
        # But your Drone class expects the path of *future* steps: [ZoneA, Goal]
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
                    f"✅ VICTORY! All drones arrived safely in "
                    f"{simulator.turn_count} turns."
                )
            else:
                print("❌ DEADLOCK ERROR! Not all drones reached the goal.\n")
                for stuck_drone in result:
                    print(
                        f"drone {stuck_drone.drone_id} at zone "
                        f"{stuck_drone.current_zone.name}"
                    )
            break

        print(f"\nTurn {simulator.turn_count} Results:")
        for moved_drone, old_zone, new_zone, action_type in report:

            if action_type == "normal":
                print(
                    f"  [SUCCESS] {moved_drone.drone_id} moved from "
                    f"{old_zone.name} to {new_zone.name}"
                )

            elif action_type == "takeoff":
                print(
                    f"  [SUCCESS] {moved_drone.drone_id} moved to "
                    f"connection {old_zone.name}-{new_zone.name}"
                )

            elif action_type == "landing":
                print(
                    f"  [SUCCESS] {moved_drone.drone_id} arrived at "
                    f"{new_zone.name}"
                )