import random
import numpy as np
import sys

# variables
gridSize = 5
mines = 4
coord = [-1, -1]
gameState = True

def outPut():
    global hiddenGrid
    print(" ", np.array([str(x) for x in range(gridSize)]),"\n")
    for ind, row in enumerate(hiddenGrid):
        print(ind,row)

def bfs(coord):
    global grid, hiddenGrid, visitedGrid, hiddenGrid2
    queue = [coord]
    while queue:
        x, y = queue.pop(0)
        if visitedGrid[x, y] == -1:
            hiddenGrid[x, y] = str(grid[x, y])
            hiddenGrid2[x, y] = grid[x, y]
            visitedGrid[x, y] = 1
            if grid[x, y] == 0:
                if inGrid([x-1, y], gridSize):
                    queue.append([x-1, y])
                if inGrid([x+1, y], gridSize):
                    queue.append([x+1, y])
                if inGrid([x, y-1], gridSize):
                    queue.append([x, y-1])
                if inGrid([x, y+1], gridSize):
                    queue.append([x, y+1])
                if inGrid([x-1, y-1], gridSize):
                    queue.append([x-1, y-1])
                if inGrid([x+1, y+1], gridSize):
                    queue.append([x+1, y+1])
                if inGrid([x-1, y+1], gridSize):
                    queue.append([x-1, y+1])
                if inGrid([x+1, y-1], gridSize):
                    queue.append([x+1, y-1])


def inGrid(coord: list, gridSize: int) -> bool:
    if coord[0] <= gridSize-1 and coord[0] > -1 and coord[-1] <= gridSize-1 and coord[-1] > -1:
        return True
    return False

# gets number of mines surrounding coord
def getSurroundings(x: int, y: int) -> int:
    global grid
    tot = 0
    if inGrid([x-1, y], gridSize) and grid[x-1, y] == -1:
        tot += 1
    if inGrid([x+1, y], gridSize) and grid[x+1, y] == -1:
        tot += 1
    if inGrid([x, y-1], gridSize) and grid[x, y-1] == -1:
        tot += 1
    if inGrid([x, y+1], gridSize) and grid[x, y+1] == -1:
        tot += 1
    if inGrid([x-1, y-1], gridSize) and grid[x-1, y-1] == -1:
        tot += 1
    if inGrid([x+1, y+1], gridSize) and grid[x+1, y+1] == -1:
        tot += 1
    if inGrid([x-1, y+1], gridSize) and grid[x-1, y+1] == -1:
        tot += 1
    if inGrid([x+1, y-1], gridSize) and grid[x+1, y-1] == -1:
        tot += 1

    return tot


def inSurroundingCoords(coord: list, centreCoord: list) -> bool:
    if coord[0] in range(centreCoord[0]-2, centreCoord[0]+2) and coord[-1] in range(centreCoord[-1]-2, centreCoord[-1]+2):
        return True
    return False


# checks users coord if it is not mine, if not reveals it, if equal to 0 reqeals surrounding coords
def coordChecker(coord) -> bool:
    global grid, hiddenGrid, visitedGrid, hiddenGrid2
    x, y = coord
    if grid[x, y] == -1:
        hiddenGrid[x, y] = "X"
        return False
    if grid[x, y] != 0 and visitedGrid[x, y] == -1:
        hiddenGrid[x, y] = grid[x, y]
        hiddenGrid2[x, y] = grid[x, y]
        visitedGrid[x, y] = 1
        return True
    else:
        # point must be 0, do depth first search to reveal rest
        bfs(coord)
        return True


def generate(n: int, startCoord: list) -> None:
    global grid, hiddenGrid, visitedGrid, hiddenGrid2
    grid = np.zeros([gridSize, gridSize], dtype=np.int32)
    visitedGrid = np.full([gridSize, gridSize], -1, dtype=np.int32)

    # place mines
    tot = 0
    while tot < mines:
        coord = [random.randint(0, gridSize), random.randint(0, gridSize)]
        if inGrid(coord, n) and grid[coord[0], coord[1]] != -1 and not inSurroundingCoords(coord, startCoord):
            tot += 1
            grid[coord[0], coord[1]] = -1

    for i in range(gridSize):
        for j in range(gridSize):
            if grid[i, j] != -1:
                grid[i, j] = getSurroundings(i, j)

    hiddenGrid = np.full([gridSize, gridSize], "-", dtype=str)
    hiddenGrid2 = np.full([gridSize, gridSize], -1, dtype=np.int8)
    t = coordChecker(startCoord)


def main():
    global gameState
    # clear terminal
    print("\033c", end="")
    coord = [-1, -1]
    while not inGrid(coord, gridSize):
        print(
            f"Please enter coordinates in the format of y, x in the ranges of {gridSize,gridSize}\n")
        try:
            coord = eval('['+input("Enter coordinate\n>")+']')
        except:
            pass
    generate(gridSize, coord)
    outPut()

    while gameState:
        coord = [-1, -1]
        while not inGrid(coord, gridSize):
            print(
                f"Please enter coordinates in the format of x, y in the ranges of {gridSize,gridSize}\n")
            try:
                coord = eval('['+input("Enter coordinate\n>")+']')
            except:
                pass
        gameState = coordChecker(coord)
        print("\033c", end="")
        outPut()
        # check if all non mines are revealed
        if np.array_equal(grid, hiddenGrid2):
            print("You win!")
            gameState = False
        


    print("get good")


if __name__ == '__main__':
    main()
