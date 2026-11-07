*This project has been created as part of the 42 curriculum by [mohamed ilyas bouliri / moboulir].*

# Fly-In 🚁

## Run the first map

From the repository root, run `make run` with Python 3 and Make installed. On the bundled linear map, two drones travel from `start` through two waypoints to `goal`. The final line reads:

```text
✅ VICTORY! All drones arrived safely in 4 turns.
```

## How routing works

The parser builds a graph from the map file. The route search uses Dijkstra’s algorithm and Yen’s algorithm to find candidate paths, then filters paths that share intermediate nodes. The simulator advances one turn at a time and tracks capacity at zones and connections.

Start with the [linear map](maps/easy/01_linear_path.txt), follow the [route search](yens_algorithm.py), then read the [simulator](simulator.py).

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