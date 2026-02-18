"""
===========================================
  ROBOT PATH PLANNING ON A 2D GRID
===========================================

Problem:
  - We have a 4x4 grid (like a small chessboard)
  - The robot starts at position (0, 0) — bottom-left corner
  - The robot needs to reach position (3, 3) — top-right corner
  - There are obstacles at (1,1), (1,2), and (2,2)
  - The robot can move 1 step in any direction (up, down, left, right, or diagonal)
  - The robot must avoid obstacles and stay inside the grid

Solution:
  - We use BFS (Breadth-First Search) to find the shortest safe path
  - BFS works like exploring in waves — it checks all nearby cells first,
    then moves outward, guaranteeing the shortest path
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import deque


# =============================================
# STEP 1: DEFINE THE GRID AND SETTINGS
# =============================================

grid_size = 4                              # 4x4 grid (cells go from 0 to 3)
start = (0, 0)                             # robot starts here
goal = (3, 3)                              # robot needs to reach here
obstacles = [(1, 1), (1, 2), (2, 2)]       # cells the robot cannot enter

# All 8 possible directions the robot can move
# (change in x, change in y)
directions = [
    (0, 1),    # up
    (0, -1),   # down
    (-1, 0),   # left
    (1, 0),    # right
    (-1, -1),  # down-left  (diagonal)
    (-1, 1),   # up-left    (diagonal)
    (1, -1),   # down-right (diagonal)
    (1, 1),    # up-right   (diagonal)
]


# =============================================
# STEP 2: HELPER FUNCTION — IS A CELL SAFE?
# =============================================

def is_safe(x, y):
    """Check if a cell is inside the grid AND not an obstacle."""

    # Check if inside grid boundaries
    inside_grid = (0 <= x < grid_size) and (0 <= y < grid_size)

    # Check if NOT an obstacle
    not_obstacle = (x, y) not in obstacles

    # Cell is safe only if BOTH conditions are true
    return inside_grid and not_obstacle


# =============================================
# STEP 3: FIND THE SHORTEST PATH USING BFS
# =============================================

def find_path(start, goal):
    """
    Use BFS to find the shortest path from start to goal.

    How BFS works (simple explanation):
    1. Start at the beginning cell
    2. Look at ALL neighbours (8 directions)
    3. Add safe, unvisited neighbours to a queue
    4. Pick the next cell from the front of the queue
    5. Repeat until we reach the goal
    6. Trace back to get the full path
    """

    # Queue holds cells we still need to explore
    # We start by adding our starting position
    queue = deque()
    queue.append(start)

    # Keep track of cells we already visited (so we don't revisit them)
    visited = set()
    visited.add(start)

    # For each cell, remember which cell we came from
    # This helps us trace the path backwards at the end
    came_from = {}
    came_from[start] = None  # start has no parent

    # Keep searching until we run out of cells or find the goal
    while len(queue) > 0:

        # Take the next cell from the front of the queue
        current = queue.popleft()
        current_x, current_y = current

        # Check: did we reach the goal?
        if current == goal:
            print("Goal reached! Now tracing the path back...\n")

            # Trace the path backwards from goal to start
            path = []
            cell = goal
            while cell is not None:
                path.append(cell)
                cell = came_from[cell]

            # Reverse it so it goes from start to goal
            path.reverse()
            return path

        # Explore all 8 neighbours around the current cell
        for dx, dy in directions:
            next_x = current_x + dx
            next_y = current_y + dy
            next_cell = (next_x, next_y)

            # Only visit this neighbour if it's safe and not yet visited
            if is_safe(next_x, next_y) and next_cell not in visited:
                visited.add(next_cell)
                came_from[next_cell] = current
                queue.append(next_cell)

    # If we get here, there is no possible path
    print("No path found!")
    return None


# =============================================
# STEP 4: RUN THE PATHFINDING
# =============================================

print("=" * 50)
print("   ROBOT PATH PLANNING")
print("=" * 50)
print(f"   Grid size  : {grid_size} x {grid_size}")
print(f"   Start      : {start}")
print(f"   Goal       : {goal}")
print(f"   Obstacles  : {obstacles}")
print("=" * 50)
print()

# Find the path
path = find_path(start, goal)

if path is None:
    print("The robot cannot reach the goal!")
else:
    # ----- Print the path -----
    print("Shortest path found!")
    print(f"Number of moves: {len(path) - 1}\n")

    for i in range(len(path)):
        x, y = path[i]
        if (x, y) == start:
            label = " <-- START"
        elif (x, y) == goal:
            label = " <-- GOAL"
        else:
            label = ""
        print(f"   Step {i}: ({x}, {y}){label}")

    # ----- Print the movement log -----
    print("\n" + "-" * 50)
    print("   MOVEMENT LOG (what the robot does each step)")
    print("-" * 50)

    for i in range(len(path) - 1):
        cx, cy = path[i]           # current position
        nx, ny = path[i + 1]       # next position

        # Check all 8 neighbours from current position
        free_cells = []
        blocked_cells = []

        for dx, dy in directions:
            check_x = cx + dx
            check_y = cy + dy

            if is_safe(check_x, check_y):
                free_cells.append((check_x, check_y))
            elif (check_x, check_y) in obstacles:
                blocked_cells.append((check_x, check_y))

        print(f"\n   Iteration {i + 1}:")
        print(f"     Robot is at       : ({cx}, {cy})")
        print(f"     Free neighbours   : {free_cells}")
        print(f"     Blocked neighbours: {blocked_cells}")
        print(f"     Robot moves to    : ({nx}, {ny})")

    print(f"\n   Robot arrived at the GOAL {goal}!")


    # =============================================
    # STEP 5: DRAW THE GRID AND PATH (PLOT)
    # =============================================

    # Create a figure (the window) and axes (the drawing area)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_title("Robot Path Planning (BFS)", fontsize=16, fontweight="bold")

    # --- Draw each cell of the grid ---
    for x in range(grid_size):
        for y in range(grid_size):

            # Pick color: dark for obstacles, light for free cells
            if (x, y) in obstacles:
                color = "#1B2A4A"           # dark blue
                text_color = "white"
            else:
                color = "#F0F0F0"           # light grey
                text_color = "#444444"

            # Draw a rounded square for this cell
            square = mpatches.FancyBboxPatch(
                (x - 0.45, y - 0.45),       # bottom-left corner of square
                0.9, 0.9,                    # width and height
                boxstyle="round,pad=0.05",
                facecolor=color,
                edgecolor="grey",
                linewidth=1.2
            )
            ax.add_patch(square)

            # Write the coordinate label inside each cell
            ax.text(x, y - 0.32, f"({x},{y})",
                    ha="center", va="center",
                    fontsize=8, color=text_color)

    # --- Mark obstacles with a red X ---
    for ox, oy in obstacles:
        ax.text(ox, oy + 0.08, "X",
                ha="center", va="center",
                fontsize=20, color="#E74C3C", fontweight="bold")

    # --- Draw the path as a red line with dots ---
    path_x = [p[0] for p in path]      # all x-coordinates of the path
    path_y = [p[1] for p in path]      # all y-coordinates of the path

    ax.plot(path_x, path_y, "-o",
            color="#E74C3C",             # red
            linewidth=2.5,
            markersize=12,
            markerfacecolor="#E74C3C",
            markeredgecolor="white",
            markeredgewidth=1.5,
            zorder=5)                    # zorder = draw on top

    # --- Add step numbers on each path point ---
    for i in range(len(path)):
        x, y = path[i]
        ax.text(x, y + 0.18, str(i),
                ha="center", va="center",
                fontsize=9, fontweight="bold", color="white",
                bbox=dict(boxstyle="round,pad=0.15",
                          facecolor="#E74C3C", edgecolor="none"),
                zorder=6)

    # --- Draw arrows showing direction of movement ---
    for i in range(len(path) - 1):
        ax.annotate(
            "",                                           # no text
            xy=(path[i+1][0], path[i+1][1]),              # arrow tip (destination)
            xytext=(path[i][0], path[i][1]),               # arrow base (origin)
            arrowprops=dict(
                arrowstyle="->,head_width=0.3,head_length=0.2",
                color="#C0392B", lw=2
            ),
            zorder=4
        )

    # --- Mark the START with a green square ---
    ax.plot(start[0], start[1], "s",
            color="#27AE60", markersize=20,
            markeredgecolor="white", markeredgewidth=2, zorder=7)
    ax.text(start[0], start[1] + 0.40, "START",
            ha="center", fontsize=10, fontweight="bold", color="#27AE60")

    # --- Mark the GOAL with a gold star ---
    ax.plot(goal[0], goal[1], "*",
            color="#F1C40F", markersize=26,
            markeredgecolor="white", markeredgewidth=1.5, zorder=7)
    ax.text(goal[0], goal[1] + 0.40, "GOAL",
            ha="center", fontsize=10, fontweight="bold", color="#DAA520")

    # --- Add a legend (key) ---
    legend_items = [
        mpatches.Patch(facecolor="#1B2A4A", edgecolor="grey", label="Obstacle"),
        mpatches.Patch(facecolor="#F0F0F0", edgecolor="grey", label="Free Cell"),
        plt.Line2D([0], [0], marker="o", color="#E74C3C", lw=2,
                   markerfacecolor="#E74C3C", markeredgecolor="white",
                   markersize=8, label="Robot Path"),
        plt.Line2D([0], [0], marker="s", color="w",
                   markerfacecolor="#27AE60", markersize=10, label="Start (0,0)"),
        plt.Line2D([0], [0], marker="*", color="w",
                   markerfacecolor="#F1C40F", markersize=14, label="Goal (3,3)"),
    ]
    ax.legend(handles=legend_items, loc="upper left", fontsize=9)

    # --- Set up the axes ---
    ax.set_xlim(-0.6, grid_size - 0.4)
    ax.set_ylim(-0.6, grid_size - 0.4)
    ax.set_xticks(range(grid_size))
    ax.set_yticks(range(grid_size))
    ax.set_xlabel("X", fontsize=12)
    ax.set_ylabel("Y", fontsize=12)
    ax.set_aspect("equal")              # keep squares looking square
    ax.grid(True, linestyle="--", alpha=0.3)

    # --- Save the plot as an image ---
    plt.tight_layout()
    plt.savefig("robot_path_plot.png", dpi=150)
    plt.close()

    print("\nPlot saved as robot_path_plot.png")