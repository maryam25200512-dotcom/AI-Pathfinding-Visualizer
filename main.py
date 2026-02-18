import time
import random
import heapq
from collections import deque
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

# ==========================================================
# GRID ENVIRONMENT
# ==========================================================

class GridEnvironment:
    def __init__(self, rows=8, cols=8, obstacle_prob=0.15):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)

       # Create one vertical obstacle wall in middle
        for i in range(1, 7):
              self.grid[i][3] = -1

        # Updated positions for 8x8
        self.start = (7, 0)
        self.goal = (0, 7)

        # Clear area around start and goal
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                for base in [self.start, self.goal]:
                    r = base[0] + dr
                    c = base[1] + dc
                    if 0 <= r < rows and 0 <= c < cols:
                        self.grid[r][c] = 0

    def is_valid(self, pos):
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] != -1

    def get_neighbors(self, pos):
        r, c = pos
        directions = [
  (-1, 0),  # Up
            (0, 1),   # Right
            (1, 0),   # Bottom
            (1, 1),   # Bottom-Right
            (0, -1),  # Left
            (-1, -1) 
        ]
        neighbors = []
        for dr, dc in directions:
            new_pos = (r + dr, c + dc)
            if self.is_valid(new_pos):
                neighbors.append(new_pos)
        return neighbors

# ==========================================================
# VISUALIZER
# ==========================================================

class PathfindingVisualizer:
    def __init__(self, env, algorithm_name):
        self.env = env
        self.algorithm_name = algorithm_name
        self.delay = 0.1
        self.exploration_order = {}
        self.step_counter = 0

        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(9, 9))
        self.fig.canvas.manager.set_window_title("AI PATHFINDER")
        self.draw(set(), set(), None, None)
        plt.show(block=False)
        plt.pause(0.5)

    def reset_steps(self):
        self.exploration_order = {}
        self.step_counter = 0

    def draw(self, frontier, explored, current=None, path=None):
        self.ax.clear()

        title = f"{self.algorithm_name}\n"
        title += f"Explored: {len(explored)}"
        self.ax.set_title(title, fontsize=14, fontweight='bold')

        if current and current not in self.exploration_order and current != self.env.start:
            self.step_counter += 1
            self.exploration_order[current] = self.step_counter

        cell_colors = []
        cell_text = []

        for i in range(self.env.rows):
            row_colors = []
            row_text = []

            for j in range(self.env.cols):
                pos = (i, j)
                color = "white"
                text = str(self.env.grid[i][j])

                if pos == self.env.start:
                    color = "#003366"
                    text = "S"

                elif pos == self.env.goal:
                    color = "#006400"
                    text = "T"

                elif self.env.grid[i][j] == -1:
                    color = "#8B0000"
                    text = "-1"

                elif path and pos in path:
                    color = "#00FF00"
                    text = str(self.exploration_order.get(pos, ""))

                elif pos in explored:
                    color = "#ADD8E6"
                    text = str(self.exploration_order.get(pos, ""))

                elif pos in frontier:
                    color = "#FFA500"
                    text = str(self.exploration_order.get(pos, ""))

                row_colors.append(color)
                row_text.append(text)

            cell_colors.append(row_colors)
            cell_text.append(row_text)

        table = self.ax.table(
            cellText=cell_text,
            cellColours=cell_colors,
            cellLoc='center',
            loc='center',
            bbox=[0, 0, 1, 1]
        )

        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1, 2)

        for i in range(self.env.rows):
            for j in range(self.env.cols):
                cell = table[(i, j)]
                cell.set_edgecolor('black')
                cell.set_linewidth(1)

        self.ax.axis('off')

        self.fig.canvas.draw_idle()
        self.fig.canvas.start_event_loop(0.001)
        plt.pause(self.delay)

    def show_final(self):
        plt.ioff()
        plt.show()

# ==========================================================
# SEARCH ALGORITHMS
# ==========================================================

class SearchAlgorithms:
    def __init__(self, env, viz):
        self.env = env
        self.viz = viz

    def reconstruct_path(self, parent, node):
        path = []
        while node in parent:
            path.append(node)
            node = parent[node]
        path.append(self.env.start)
        return path[::-1]

    # ------------------------------------------------------
    # BFS
    # ------------------------------------------------------
    def bfs(self):
        queue = deque([self.env.start])
        parent = {}
        explored = set()

        while queue:
            current = queue.popleft()
            explored.add(current)

            self.viz.draw(set(queue), explored, current)

            if current == self.env.goal:
                path = self.reconstruct_path(parent, current)
                self.viz.draw(set(), explored, None, path)
                return path

            for neighbor in self.env.get_neighbors(current):
                if neighbor not in explored and neighbor not in queue:
                    parent[neighbor] = current
                    queue.append(neighbor)

        return None

    # ------------------------------------------------------
    # DFS
    # ------------------------------------------------------
    def dfs(self):
        stack = [self.env.start]
        parent = {}
        explored = set()

        while stack:
            current = stack.pop()

            if current in explored:
                continue

            explored.add(current)
            self.viz.draw(set(stack), explored, current)

            if current == self.env.goal:
                path = self.reconstruct_path(parent, current)
                self.viz.draw(set(), explored, None, path)
                return path

            for neighbor in reversed(self.env.get_neighbors(current)):
                if neighbor not in explored:
                    parent[neighbor] = current
                    stack.append(neighbor)

        return None

    # ------------------------------------------------------
    # UCS
    # ------------------------------------------------------
    def ucs(self):
        pq = [(0, self.env.start)]
        parent = {}
        cost = {self.env.start: 0}
        explored = set()

        while pq:
            current_cost, current = heapq.heappop(pq)

            if current in explored:
                continue

            explored.add(current)
            frontier = {item[1] for item in pq}
            self.viz.draw(frontier, explored, current)

            if current == self.env.goal:
                path = self.reconstruct_path(parent, current)
                self.viz.draw(set(), explored, None, path)
                return path

            for neighbor in self.env.get_neighbors(current):
                move_cost = 1.414 if abs(neighbor[0]-current[0]) == 1 and abs(neighbor[1]-current[1]) == 1 else 1
                new_cost = current_cost + move_cost

                if neighbor not in cost or new_cost < cost[neighbor]:
                    cost[neighbor] = new_cost
                    parent[neighbor] = current
                    heapq.heappush(pq, (new_cost, neighbor))

        return None

    # ------------------------------------------------------
    # DLS
    # ------------------------------------------------------
    def dls(self, limit=15):
        def recursive(node, depth):
            explored.add(node)
            self.viz.draw(set(), explored, node)

            if node == self.env.goal:
                return True

            if depth == 0:
                return False

            for neighbor in self.env.get_neighbors(node):
                if neighbor not in explored:
                    parent[neighbor] = node
                    if recursive(neighbor, depth - 1):
                        return True
            return False

        parent = {}
        explored = set()

        found = recursive(self.env.start, limit)

        if found:
            path = self.reconstruct_path(parent, self.env.goal)
            self.viz.draw(set(), explored, None, path)
            return path

        return None

    # ------------------------------------------------------
    # IDDFS
    # ------------------------------------------------------
    def iddfs(self):
        for depth in range(30):
            self.viz.reset_steps()
            result = self.dls(depth)
            if result:
                return result
        return None

    # ------------------------------------------------------
    # BIDIRECTIONAL
    # ------------------------------------------------------
    def bidirectional_search(self):
        qf = deque([self.env.start])
        qb = deque([self.env.goal])

        pf = {}
        pb = {}

        explored_f = set()
        explored_b = set()

        while qf and qb:

            current_f = qf.popleft()
            explored_f.add(current_f)

            for neighbor in self.env.get_neighbors(current_f):
                if neighbor not in explored_f:
                    pf[neighbor] = current_f
                    qf.append(neighbor)

                if neighbor in explored_b:
                    path1 = self.reconstruct_path(pf, neighbor)
                    path2 = []
                    node = neighbor
                    while node in pb:
                        path2.append(node)
                        node = pb[node]
                    return path1 + path2[::-1]

            current_b = qb.popleft()
            explored_b.add(current_b)

            for neighbor in self.env.get_neighbors(current_b):
                if neighbor not in explored_b:
                    pb[neighbor] = current_b
                    qb.append(neighbor)

            self.viz.draw(set(qf) | set(qb), explored_f | explored_b, current_f)

        return None

# ==========================================================
# MAIN
# ==========================================================

def main():
    print("\nSelect Algorithm:")
    print("1. BFS")
    print("2. DFS")
    print("3. UCS")
    print("4. DLS")
    print("5. IDDFS")
    print("6. Bidirectional")

    choice = input("Enter choice from 1-6: ").strip()

    mapping = {
        "1": "bfs",
        "2": "dfs",
        "3": "ucs",
        "4": "dls",
        "5": "iddfs",
        "6": "bidirectional"
    }

    if choice not in mapping:
        print("Invalid choice!")
        return

    env = GridEnvironment()
    viz = PathfindingVisualizer(env, mapping[choice].upper())
    searcher = SearchAlgorithms(env, viz)

    start = time.time()
    path = getattr(searcher, mapping[choice])()
    end = time.time()

    if path:
        print(f"\nPath Found | Length: {len(path)}")
    else:
        print("\nNo Path Found")

    viz.show_final()

if __name__ == "__main__":
    main()    
