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

    # --- 2. START THE SIMULATOR ---
    simulator = Simulator(graph, my_drones)

    # 4. Print the Official Referee Report!
    print("\n--- STARTING SIMULATION ---")
    
    # THE GAME LOOP
    while True:
        # Run one step
        report = simulator.step()

        print(f"\nTurn {simulator.turn_count} Results:")
        
        # If the report is empty, nobody moved. The game is over!
        if len(report) == 0:
            print("  Simulation finished! (Everyone arrived or traffic jam)")
            break
            
        # If people moved, print out exactly what happened
        for moved_drone, old_zone, new_zone in report:
            print(f"  [SUCCESS] {moved_drone.drone_id} moved from {old_zone.name} to {new_zone.name}")

    print("\n--- END OF GAME ---")
