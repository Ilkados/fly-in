*This project has been created as part of the 42 curriculum by [mohamed ilyas bouliri / moboulir].*

# Fly-In 🚁

## Description

**Fly-In** is a complex pathfinding and traffic simulation engine. The primary goal of the project is to safely and efficiently route a fleet of drones from a starting hub to an ending hub across a customized network of nodes, avoiding mid-air collisions and respecting link capacities.

The project features a highly resilient parsing engine that reads custom map files, a graph-theory-based pathfinding system to calculate non-intersecting routes, and a turn-by-turn "Air Traffic Controller" simulation that orchestrates the movement of the drones until they all successfully reach their destination.

## Algorithm & Implementation Strategy

To ensure optimal routing without collisions, the project relies on several key algorithmic choices:

* **Dijkstra's & Yen's Algorithms:** The engine uses Dijkstra’s algorithm to calculate the absolute shortest path. It then utilizes Yen’s k-shortest paths algorithm to generate a comprehensive list of alternative detours through the graph.
* **Greedy "Safe Highway" Filtering:** Because Yen's algorithm generates overlapping paths, a custom greedy algorithm filters the results. It automatically approves the shortest path, then iteratively checks remaining paths against the approved group, discarding any that share nodes (conflict). This results in a final set of completely independent "highways."
* **Queue-Based Simulation:** The `Simulator` acts as an Air Traffic Controller. It assigns drones to the safe highways, slicing the start node from the paths so drones process a pure queue of upcoming destinations. The simulation runs a `step()` function iteratively, moving drones turn-by-turn while strictly enforcing graph constraints.
* **Defensive Parsing:** The program implements strict input validation and `try...except` chaining to handle untrusted user data (map files). It catches formatting errors, topological impossibilities (phantom connections), and missing metadata efficiently.

## Visual Representation

To enhance the user experience (UX), the terminal output has been highly optimized:

* **Color-Coded Feedback:** ANSI escape codes are used to colorize the terminal output (e.g., Cyan for simulation start, Yellow for turn indicators and non-fatal warnings, Green for success messages).
* **Traceback Suppression:** When a user provides an invalid map file, the program gracefully catches the custom `ValueError` using `from None` and a main `try...except` block. Instead of crashing with an ugly Python traceback, it prints a clean, human-readable error specifying the exact line and cause of the formatting mistake.
* **Turn-by-Turn Telemetry:** The terminal clearly displays the step-by-step state of the drones, allowing the user to easily visualize the flow of traffic across the graph without feeling overwhelmed by raw data.

## Instructions

This project requires Python 3. It utilizes a `Makefile` for streamlined execution.

**To run the simulation with the default map:**

```bash
make run

```

**To run the simulation with a specific custom map:**

```bash
make run MAP=maps/hard/03_ultimate_challenge.txt

```

**To clean up Python cache files (`__pycache__`, `.mypy_cache`):**

```bash
make clean

```

## Resources

* **Graph Theory & Pathfinding:** https://youtu.be/bQCewgMFaYQ?si=-ejYqyFU72U8ZcNW / 

* **AI Usage:** Artificial Intelligence (LLMs) was used during this project primarily for code review and for visualization techniques, conceptualizing the boundary between untrusted data parsing and the algorithms (defensive programming), optimizing the `Makefile` with Unix `find` commands, and structuring Python exception chaining (`from None`) to improve error UX.