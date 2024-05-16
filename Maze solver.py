from pyamaze import maze, agent, COLOR, textLabel
from queue import PriorityQueue

# Heuristic function: Manhattan distance between the current cell and the goal cell:(1,1)
def h(cell):
    x, y = cell
    return (x - 1) + (y - 1)

def aStar(m):
    # Start cell is the bottom-right corner of the maze
    start = (m.rows, m.cols)

    # Initialize g_score and f_score for each cell in the maze
    g_score = {cell:float('inf') for cell in m.grid}
    g_score[start] = 0
    f_score = {cell:float('inf') for cell in m.grid}
    f_score[start] = h(start)

    # Priority queue to store open cells, ordered by f_score
    open = PriorityQueue()
    open.put((f_score[start], h(start), start))
    aPath = {}

    while not open.empty():
        currCell = open.get()[2]
        if currCell == (1,1):
            break

        # Check adjacent cells
        for d in "ESNW":
            if m.maze_map[currCell][d] == True:
                if d == 'E':
                    childCell = (currCell[0], currCell[1] + 1)
                elif d == 'W':
                    childCell = (currCell[0], currCell[1] - 1)
                elif d == 'N':
                    childCell = (currCell[0] - 1, currCell[1])
                elif d == 'S':
                    childCell = (currCell[0] + 1, currCell[1])
        
                temp_g_score = g_score[currCell] + 1
                temp_f_score = temp_g_score + h(childCell)

                # Check if the new path of the adjacent cell is better
                if temp_f_score < f_score[childCell]:
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_f_score
                    open.put((temp_f_score, h(childCell), childCell))
                    aPath[childCell] = currCell
    
    # Reconstruct the forward path from start to target
    fwdPath = {}
    cell = (1,1)
    while cell != start:
        fwdPath[aPath[cell]] = cell
        cell = aPath[cell]

    return fwdPath

m = maze(5,5)
m.CreateMaze()
path = aStar(m)
a = agent(m, footprints=True, color=COLOR.blue, filled=True)
m.tracePath({a:path})
l = textLabel(m, "A* path length", len(path)+1)

m.run()