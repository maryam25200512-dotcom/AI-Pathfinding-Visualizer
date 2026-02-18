AI Grid Pathfinding Visualizer
A Python-based AI Pathfinding Visualizer that demonstrates different search algorithms on an 8x8 grid environment with obstacles.
It visually shows:
Explored nodes
Frontier nodes
Final shortest path
Step-by-step exploration order
===>Implemented Algorithms
Breadth First Search (BFS)
Depth First Search (DFS)
Uniform Cost Search (UCS)
Depth Limited Search (DLS)
Iterative Deepening DFS (IDDFS)
Bidirectional Search
==> Requirements
Install these Python libraries before running:
pip install numpy matplotlib
Python version recommended: Python 3.8+
▶️ How to Run (VS Code / Terminal)
Save the file as:
pathfinder.py
Run:
python pathfinder.py
Select algorithm (1–6) from the menu.
▶️ How to Run in Jupyter Notebook
Step 1: Install requirements (if not installed)
!pip install numpy matplotlib
Step 2: Important (For GUI Support)
Before running the code cell, add this at the top:
%matplotlib tk
If %matplotlib tk does not work, try:
%matplotlib qt