from parser import Parser
from graph import Graph
from simulator import Simulator
from drone import Drone
if __name__ == "__main__":
    parser = Parser("map.txt")
    parser.parse()
    
    graph = Graph(parser.zones,parser.connections)

# --- 1. SPAWN THE DRONES ---
    # --- 1. SPAWN THE DRONES ---
    my_drones: list[Drone] = []
    for i in range(parser.nb_drones):
        d_id = f"Drone_{i+1}"
        
        # Build the fake Phase 4 path FIRST
        # Grab the exact zone named 'waypoint1' from the dictionary
        # The full route from start to finish!
        mock_path = [
            parser.zones["waypoint1"], 
            parser.zones["waypoint2"], 
            parser.zones["goal"]
        ]
        # Hand it to the drone exactly the way the constructor demands
        new_drone = Drone(d_id, parser.start_zone, mock_path)
        
        
        my_drones.append(new_drone)
    

    print(parser.start_zone.current_drones)
    # --- 2. START THE SIMULATOR ---
    simulator = Simulator(graph, my_drones)

    # 4. Print the Official Referee Report!
    print("\n--- STARTING SIMULATION ---")
    
    # THE GAME LOOP
    # THE GAME LOOP
    while True:
        report = simulator.step()
        
        if len(report) == 0:
            print("\n--- END OF GAME ---")
            
            # Use your function to check if we won!
            if simulator.check_simulation_result(my_drones):
                print(f"✅ VICTORY! All drones arrived safely in {simulator.turn_count} turns.")
            else:
                print(f"❌ DEADLOCK ERROR! Not all drones reached the goal.")
            break
            
        print(f"\nTurn {simulator.turn_count} Results:")
        for moved_drone, old_zone, new_zone in report:
            print(f"  [SUCCESS] {moved_drone.drone_id} moved from {old_zone.name} to {new_zone.name}")