import random, math, time

class cellClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = False
        self.rectangle = 0 #empty for now, later holds the rectangle so that .delete() can be called

    def coords(self): #This isn't used
        return f"({self.x}, {self.y})"

    def loopCells(self, xSize, ySize, cell):
        #the 8 neighbors of the current cell (midCent skipped; is just currentCell)
        topLeft = [cell.x - 1, cell.y - 1]
        topCent = [cell.x - 1, cell.y]
        topRight = [cell.x - 1, cell.y + 1]
        midLeft = [cell.x , cell.y - 1]
        midRight = [cell.x, cell.y + 1]
        bottomLeft = [cell.x + 1, cell.y - 1]
        bottomCent = [cell.x + 1, cell.y]
        bottomRight = [cell.x + 1, cell.y + 1]
        mainCell = [cell.x, cell.y] #original cell: Sometimes, it does not get included, I don't know why
        self.coordsList = [topLeft, topCent, topRight, midLeft, midRight, bottomLeft, bottomCent, bottomRight]
        for coords in self.coordsList: #loops cells that are out of range
            if coords[0] > xSize - 1:
                coords[0] = 0
            if coords[1] > ySize - 1:
                coords[1] = 0
            if coords[0] < 0:
                coords[0] = xSize - 1
            if coords[1] < 0:
                coords[1] = ySize - 1
        return self.coordsList
    
    def findNeighbors(self, xSize, ySize, cellList): #Finds original 8 neighbors of current cell
        coordsList = self.loopCells(xSize, ySize, self)
        self.neighbors = []
        for coords in coordsList:
            self.neighbors.append(cellList[coords[0]][coords[1]])
        return self.neighbors
    
    def updateCells(self, neighbors, cellsSet, cellList, xSize, ySize): #finds the 8 neighbors for each neighbor of the current cell
        for i in neighbors:
            coordsList = self.loopCells(xSize, ySize, i)
            if i.alive == True:
                cellsSet.add(i)
                for j in coordsList:
                    cellsSet.add(cellList[j[0]][j[1]])
        return cellsSet

class gameClass: #makes each cell an object
    def __init__(self, columns, rows):
        numberOfCells = rows * columns
        self.cellList = []
        cellListY = []
        currentRow = 0
        currentColumn = 0
        while currentColumn < columns:
            while currentRow < rows:
                cellListY.append(cellClass(currentColumn, currentRow))
                currentRow += 1
            self.cellList.append(cellListY)
            cellListY = []
            currentRow = 0
            currentColumn += 1

#testing with the functions and classes
'''game = gameClass(10, 10)
x = 1
y = 2
print(game.cellList[x][y].coords())
game.cellList[x][y].alive = True
print(f"Cell {game.cellList[x][y]} is {game.cellList[x][y].alive}")'''