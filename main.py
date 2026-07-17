from parser import Parser
from graph import Graph
from simulator import Simulator
from drone import Drone

if __name__ == "__main__":
    # 1. Flip the map to the real one!
    parser = Parser("map.txt")
    parser.parse()
    
    graph = Graph(parser.zones, parser.connections)

    # --- 1. SPAWN THE DRONES ---
    my_drones: list[Drone] = []
    for i in range(parser.nb_drones):
        d_id = f"Drone_{i+1}"
        
        mock_path = [
            parser.zones["bottleneck"], 
            parser.zones["wide_area"], 
            parser.zones["goal"]
        ]
        
        new_drone = Drone(d_id, parser.start_zone, mock_path)
        my_drones.append(new_drone)
        
    # --- 2. START THE SIMULATOR ---
    # (Notice this is outside the for-loop now!)
    simulator = Simulator(graph, my_drones)

    print("\n--- STARTING SIMULATION ---")
    
    # --- 3. THE GAME LOOP ---
    while True:
        report = simulator.step()
        
        if len(report) == 0:
            print("\n--- END OF GAME ---")
            
            result = simulator.check_simulation_result_and_return_stuck_drones()
            if not result:
                print(f"✅ VICTORY! All drones arrived safely in {simulator.turn_count} turns.")
            else:
                print(f"❌ DEADLOCK ERROR! Not all drones reached the goal.\n")
                for stuck_drone in result:
                    print(f"drone {stuck_drone.drone_id} at zone {stuck_drone.current_zone.name}")
            break
            
        print(f"\nTurn {simulator.turn_count} Results:")
        # Notice the new 'action_type' variable here!
        for moved_drone, old_zone, new_zone, action_type in report:
            
            if action_type == "normal":
                print(f"  [SUCCESS] {moved_drone.drone_id} moved from {old_zone.name} to {new_zone.name}")
                
            elif action_type == "takeoff":
                # Print the connection instead of the zone
                print(f"  [SUCCESS] {moved_drone.drone_id} moved to connection {old_zone.name}-{new_zone.name}")
                
            elif action_type == "landing":
                # Print the arrival
                print(f"  [SUCCESS] {moved_drone.drone_id} arrived at {new_zone.name}")