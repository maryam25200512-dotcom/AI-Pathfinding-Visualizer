# AI Grid Pathfinding Visualizer

A simple Python program to visualize AI pathfinding (un-informed & blind search) algorithms on an **8x8 grid** with obstacles.

## Features
- Shows **explored nodes**
- Shows **frontier nodes**
- Shows the **final shortest path** (where applicable)
- Step-by-step visualization of the search process
- Clean grid animation using Matplotlib

## Algorithms Implemented
- Breadth First Search (**BFS**)
- Depth First Search (**DFS**)
- Uniform Cost Search (**UCS**)
- Depth Limited Search (**DLS**)
- Iterative Deepening DFS (**IDDFS**)
- Bidirectional Search

## Requirements
Install these Python libraries before running:


pip install numpy matplotlib

## How to Run

### **Via Terminal / Command Line**
- Install dependencies
  
  pip install numpy matplotlib

Run the programBashpython main.py

Choose an algorithm by entering a number (1–6)

## **Via Jupyter Notebook**

1. Install libraries (run once in a cell)Python!pip install numpy matplotli
2. Copy all your code into one cell
-Remove the line: if __name__ == "____main__"
3. Add main() at the end of the cell
(Optional) If plots don’t appear, add this at the very top:Python%matplotlib nonotebook
4. Run the cell (Shift + Enter)
5. Enter a number 1–6 to select the algorithm
6. A window will pop up showing the step-by-step search
7. Close the window when finished, or re-run the cell to try another algorithm


