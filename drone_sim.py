import pygame
import sys
import math

# --- CONFIGURATION ---
WIDTH, HEIGHT = 1200, 600
FPS = 60
TURN_DURATION = 1.5 # Seconds per turn animation

# --- COLOR MENU ---
BLUE = (50, 150, 255)    # Drone ID Text
GREEN = (46, 204, 113)   # Normal Movement
YELLOW = (241, 196, 15)  # Takeoff / Start
CYAN = (0, 255, 255)     # Landing / Goal Reached
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)

# --- MAP DATA ---
# (x, y) coordinates for each zone
NODES = {
    "start": (100, 300),
    "maze_a1": (250, 300),
    "maze_a2": (400, 150),
    "maze_b1": (400, 450),
    "maze_c2": (550, 150),
    "maze_b2": (550, 450),
    "bottleneck": (750, 300),
    "final_stretch1": (900, 150),
    "final_stretch2": (900, 450),
    "goal": (1100, 300)
}

CAPACITIES = {
    "start": "inf", "maze_a1": "2", "maze_a2": "1", "maze_b1": "1",
    "maze_b2": "2", "maze_c2": "2", "bottleneck": "2", 
    "final_stretch1": "1", "final_stretch2": "1", "goal": "inf"
}

# Derived from the successful movements in the logs
CONNECTIONS = [
    ("start", "maze_a1"),
    ("maze_a1", "maze_a2"),
    ("maze_a1", "maze_b1"),
    ("maze_a2", "maze_c2"),
    ("maze_b1", "maze_b2"),
    ("maze_b2", "maze_c2"),
    ("maze_c2", "bottleneck"),
    ("bottleneck", "final_stretch1"),
    ("bottleneck", "final_stretch2"),
    ("final_stretch1", "goal"),
    ("final_stretch2", "goal")
]

# --- TURN DATA PARSED FROM LOGS ---
TURNS = [
    # Turn 1
    [("Drone_1", "start", "maze_a1"), ("Drone_2", "start", "maze_a1")],
    # Turn 2
    [("Drone_1", "maze_a1", "maze_a2"), ("Drone_2", "maze_a1", "maze_b1"), ("Drone_3", "start", "maze_a1"), ("Drone_4", "start", "maze_a1")],
    # Turn 3
    [("Drone_1", "maze_a2", "maze_c2"), ("Drone_2", "maze_b1", "maze_b2"), ("Drone_3", "maze_a1", "maze_a2"), ("Drone_4", "maze_a1", "maze_b1"), ("Drone_5", "start", "maze_a1"), ("Drone_6", "start", "maze_a1")],
    # Turn 4
    [("Drone_1", "maze_c2", "bottleneck"), ("Drone_2", "maze_b2", "maze_c2"), ("Drone_3", "maze_a2", "maze_c2"), ("Drone_4", "maze_b1", "maze_b2"), ("Drone_5", "maze_a1", "maze_a2"), ("Drone_6", "maze_a1", "maze_b1"), ("Drone_7", "start", "maze_a1"), ("Drone_8", "start", "maze_a1")],
    # Turn 5
    [("Drone_1", "bottleneck", "final_stretch1"), ("Drone_2", "maze_c2", "bottleneck"), ("Drone_4", "maze_b2", "maze_c2"), ("Drone_6", "maze_b1", "maze_b2"), ("Drone_8", "maze_a1", "maze_b1")],
    # Turn 6
    [("Drone_1", "final_stretch1", "goal"), ("Drone_2", "bottleneck", "final_stretch2"), ("Drone_3", "maze_c2", "bottleneck"), ("Drone_5", "maze_a2", "maze_c2"), ("Drone_7", "maze_a1", "maze_a2"), ("Drone_8", "maze_b1", "maze_b2")],
    # Turn 7
    [("Drone_2", "final_stretch2", "goal"), ("Drone_3", "bottleneck", "final_stretch1"), ("Drone_4", "maze_c2", "bottleneck"), ("Drone_6", "maze_b2", "maze_c2")],
    # Turn 8
    [("Drone_3", "final_stretch1", "goal"), ("Drone_4", "bottleneck", "final_stretch2"), ("Drone_5", "maze_c2", "bottleneck"), ("Drone_7", "maze_a2", "maze_c2")],
    # Turn 9
    [("Drone_4", "final_stretch2", "goal"), ("Drone_5", "bottleneck", "final_stretch1"), ("Drone_6", "maze_c2", "bottleneck"), ("Drone_8", "maze_b2", "maze_c2")],
    # Turn 10
    [("Drone_5", "final_stretch1", "goal"), ("Drone_6", "bottleneck", "final_stretch2"), ("Drone_7", "maze_c2", "bottleneck")],
    # Turn 11
    [("Drone_6", "final_stretch2", "goal"), ("Drone_7", "bottleneck", "final_stretch1"), ("Drone_8", "maze_c2", "bottleneck")],
    # Turn 12
    [("Drone_7", "final_stretch1", "goal"), ("Drone_8", "bottleneck", "final_stretch2")],
    # Turn 13
    [("Drone_8", "final_stretch2", "goal")]
]

class Drone:
    def __init__(self, id_str):
        self.id_str = id_str
        self.display_id = id_str.replace("Drone_", "D")
        self.current_node = "start"
        self.target_node = "start"
        self.progress = 0.0

    def get_color(self):
        if self.current_node == "start" and self.target_node != "goal":
            return YELLOW # Takeoff / At start
        elif self.target_node == "goal" or self.current_node == "goal":
            return CYAN   # Landing / Goal Reached
        return GREEN      # Normal Movement

    def draw(self, screen, font, offset_x=0, offset_y=0):
        start_pos = NODES[self.current_node]
        target_pos = NODES[self.target_node]

        # Linear interpolation for smooth movement
        x = start_pos[0] + (target_pos[0] - start_pos[0]) * self.progress
        y = start_pos[1] + (target_pos[1] - start_pos[1]) * self.progress

        # Draw Drone Circle
        pygame.draw.circle(screen, self.get_color(), (int(x + offset_x), int(y + offset_y)), 12)
        pygame.draw.circle(screen, BLACK, (int(x + offset_x), int(y + offset_y)), 12, 2)

        # Draw Drone ID in Blue
        text_surface = font.render(self.display_id, True, BLUE)
        text_rect = text_surface.get_rect(center=(int(x + offset_x), int(y - 22 + offset_y)))
        
        # Adding a slight background to text so it's readable over lines
        bg_rect = text_rect.copy()
        bg_rect.inflate_ip(4, 4)
        pygame.draw.rect(screen, BLACK, bg_rect)
        screen.blit(text_surface, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Drone Routing Simulation")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Consolas", 14, bold=True)
    title_font = pygame.font.SysFont("Consolas", 24, bold=True)

    # Initialize all 8 drones at start
    drones = {f"Drone_{i}": Drone(f"Drone_{i}") for i in range(1, 9)}
    
    current_turn_index = 0
    animating = True
    progress = 0.0

    # Load initial moves for turn 1
    def load_turn(turn_idx):
        if turn_idx >= len(TURNS):
            return False
        
        # Reset targets to current (if a drone doesn't move, it stays put)
        for d in drones.values():
            d.target_node = d.current_node
            d.progress = 0.0

        # Apply movements for this turn
        for move in TURNS[turn_idx]:
            drone_id, start, end = move
            drones[drone_id].current_node = start
            drones[drone_id].target_node = end
        
        return True

    animating = load_turn(current_turn_index)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0 # Delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if animating:
            progress += dt / TURN_DURATION
            if progress >= 1.0:
                progress = 1.0
                
                # Finalize turn
                for d in drones.values():
                    d.current_node = d.target_node
                    
                # Load next turn
                current_turn_index += 1
                progress = 0.0
                animating = load_turn(current_turn_index)
            
            # Update drone objects
            for d in drones.values():
                d.progress = progress

        # --- DRAWING ---
        screen.fill(BLACK)

        # Draw Legend
        legend = [
            ("Blue", "Drone ID", BLUE),
            ("Green", "Normal Movement", GREEN),
            ("Yellow", "Takeoff", YELLOW),
            ("Cyan", "Landing / Goal", CYAN)
        ]
        for i, (color_name, desc, color) in enumerate(legend):
            pygame.draw.circle(screen, color, (30, 30 + i * 25), 8)
            label = font.render(f"{color_name} = {desc}", True, WHITE)
            screen.blit(label, (50, 22 + i * 25))

        # Draw Turn Tracker
        status_text = f"Turn: {current_turn_index + 1} / {len(TURNS)}" if animating else "VICTORY! Simulation Complete."
        status_surf = title_font.render(status_text, True, WHITE)
        screen.blit(status_surf, (WIDTH // 2 - status_surf.get_width() // 2, 30))

        # Draw Connections
        for start, end in CONNECTIONS:
            pygame.draw.line(screen, GRAY, NODES[start], NODES[end], 3)

        # Draw Nodes
        for name, pos in NODES.items():
            pygame.draw.circle(screen, LIGHT_GRAY, pos, 25)
            pygame.draw.circle(screen, WHITE, pos, 25, 3)
            
            # Node Name
            name_surf = font.render(name, True, WHITE)
            screen.blit(name_surf, (pos[0] - name_surf.get_width()//2, pos[1] - 45))
            
            # Capacity Label
            cap_surf = font.render(f"Cap: {CAPACITIES[name]}", True, LIGHT_GRAY)
            screen.blit(cap_surf, (pos[0] - cap_surf.get_width()//2, pos[1] + 30))

        # Draw Drones (Calculate overlap offsets so they don't hide each other)
        node_counts = {}
        for d in drones.values():
            key = (d.current_node, d.target_node)
            node_counts[key] = node_counts.get(key, 0) + 1
            
        current_counts = {}
        for d in drones.values():
            key = (d.current_node, d.target_node)
            idx = current_counts.get(key, 0)
            current_counts[key] = idx + 1
            
            total = node_counts[key]
            
            # If multiple drones are on the exact same path/node, spread them out slightly
            offset_x, offset_y = 0, 0
            if total > 1:
                angle = (idx / total) * 2 * math.pi
                offset_x = math.cos(angle) * 15
                offset_y = math.sin(angle) * 15
                
            d.draw(screen, font, offset_x, offset_y)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()