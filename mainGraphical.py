import random
import time
import numpy as np
import sys
import pygame
from pygame.locals import *
import os
# variables
gridSize = 5
mines = 4
coord = [-1, -1]
gameState = True
w, h = 500, 500

# set up pygame

WHITE=(255,255,255)
BLACK=(0,0,0)
GREY=(128,128,128)
BLUE=(0,0,255)
RED=(255,0,0)

class square():
    def __init__(self, x, y, width, height, color, text=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text

    def draw(self, screen):
        #draw square with black outline and padding
        self.rect=pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 1)
        if self.text != "":
            font = pygame.font.SysFont('comicsans', 40)
            text = font.render(self.text, 1, BLACK)
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))


def outPut(outGrid):
    global  boxes
    boxes=[]
    for i in range(0,gridSize):
        for j in range(0,gridSize):
            text=""
            xPos=i*(w/gridSize)
            yPos=j*(h/gridSize)
            width=w/gridSize
            height=h/gridSize


            if outGrid[i, j] == "-":
                color = GREY
            elif outGrid[i, j] == "X":
                color=RED
            else:
                color=WHITE
                text = outGrid[i, j]
            boxes.append(square(xPos, yPos, width, height, color, text))
            boxes[-1].draw(screen)

def inBox(coord: list, box) -> bool:
    if coord[0] in range(box.x, box.x+box.width) and coord[-1] in range(box.y, box.y+box.height):
        return True
    return False

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
    global gameState, screen, clock, hiddenGrid
    coord = [-1, -1]
    while not inGrid(coord, gridSize):
        print(
            f"Please enter coordinates in the format of y, x in the ranges of {gridSize,gridSize}\n")
        try:
            coord = eval('['+input("Enter coordinate\n>")+']')
        except:
            pass
    generate(gridSize, coord)
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()


    pygame.display.set_caption("Minesweeper")
    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()

    
    run = True
    clock = pygame.time.Clock()
    while run:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if events.type == pygame.MOUSEBUTTONDOWN:
                coord = pygame.mouse.get_pos()
                for ind, box in enumerate(boxes):
                    if box.rect.collidepoint(coord[1], coord[0]):
                        x, y = ind % gridSize, ind//gridSize
                        run = coordChecker([x, y])
                        if np.array_equal(grid, hiddenGrid2):
                            print("You win!")
                            run = False
            


        outPut(hiddenGrid)
        
        pygame.display.update()
    
    outPut(hiddenGrid2)
    pygame.display.update()
    time.sleep(5)
    pygame.quit()


if __name__ == '__main__':
    main()
