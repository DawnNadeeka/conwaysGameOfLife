'''Imports and Variables'''
import random, math, time, asyncio, classes
from tkinter import *

master = Tk() #create new window or "canvas" called "master"
canvasWidth = 60 #canvas width
canvasHeight = 40 #canvas height
cellSize = 10 #the size length of the cell; should fit evenly into both canvasWidth and canvasHeight
startingCells = int(canvasHeight / 2) #how many cells the game should start with
cellColor = ["#7ec2cc", "#a3dae3"]
cellSpacing = 2
speed = 0.1 #speed of cells (in seconds), or how often it should update to the next generation
listOfCells = set() #empty set, used to hold all alive cells while removing duplicates
gameOn = False #Game starts turned off


inProgress = True #disables settings; I'm not done with it

'''Functions'''
def checkered(canvas, lineDistance): #draws lines
    #vertical lines, each lineDistance pixels apart
    for x in range(lineDistance, (canvasWidth * cellSize), lineDistance):
        canvas.create_line(x, 0, x, (canvasHeight * cellSize), fill="#dddddd")
    #horizontal lines, each lineDistance pixels apart
    for y in range(lineDistance, (canvasHeight * cellSize), lineDistance):
        canvas.create_line(0, y, (canvasWidth * cellSize), y, fill="#dddddd")

def startingBoard(): #places startingCells random cells, semi-near each other, for a starting board
    #picks the first random cells
    x = random.randint(0, canvasWidth)
    y = random.randint(0, canvasHeight)
    for i in range (startingCells): #spawns the first startingCells starting cubes
        #loops board
        if x > canvasWidth - 1:
            x = 0
        if x < 0:
            x = canvasWidth - 1
        if y > canvasHeight - 1:
            y = 0
        if y < 0:
            y = canvasHeight - 1
        game.cellList[x][y].alive = True
        #moves next cell up to cellSpacing squares away in any direction
        x += random.randint(-cellSpacing, cellSpacing)
        y += random.randint(-cellSpacing, cellSpacing)
    listOfCells = drawCells(game) #draws cube
    return listOfCells

def resetCanvas(): #resets the canvas
    pen.delete("all") #clears canvas
    pen.create_rectangle(0, 0, (canvasWidth * cellSize), (canvasHeight * cellSize), fill="#ffffff", outline="#dddddd") #draws border
    for i in game.cellList: #deletes any alive drawn cells
        for j in i:
            j.alive = False
            pen.delete(j.rectangle)
    checkered(pen, cellSize) #draws grid
    listOfCells = startingBoard()
    cellCountText["text"] = f"Cell count: {len(listOfCells)}"

def resumeGame(): #Start/stop loop
    global gameOn
    if gameOn: #if game is on; turns it off
        gameOn = False
        playPause["text"] = "Play"
        playPause["bg"] = "#7df585"
        playPause["fg"] = "#007a08"
    else: #if game is off; turns it on
        gameOn = True
        playPause["text"] = "Pause"
        playPause["bg"] = "#ff6b6b"
        playPause["fg"] = "#8f0000"
        checkIfOn()

def checkIfOn(): #Used to check if it should keep running; a while loop in resumeGame doesn't work; it won't draw any cells or enable buttons until the while loop finishes. It never will finish, causing the game to lag and eventually crash.
    global gameOn
    global listOfCells
    global cellCountText
    if gameOn:
        nextGen()
        cellCountText["text"] = f"Cell count: {len(listOfCells)}" #won't work?
    master.after(int(speed * 1000), checkIfOn) #how long to wait before running the function again

def nextGen():
    listOfCells = set()
    for i in game.cellList:
        for j in i:
            if j.alive:
                cellsSet = set()
                neighbors = j.findNeighbors(canvasWidth, canvasHeight, game.cellList) #stores first 8 neighbors
                tempCellSet = j.updateCells(neighbors, cellsSet, game.cellList, canvasWidth, canvasHeight) #stores the 8 neighbors of each neighbor for the current cell, putting them in a set so that duplicates are removed
                for k in tempCellSet: #moves all the neighbors of the neighbors of the current cell to listOfCells; tempCellSet gets reset for each new current cell; listOfCells does not
                    listOfCells.add(k)
                if not j in listOfCells: #for some reason, sometimes the original cell does not get added; adds it here
                    listOfCells.add(j)
    checkCells(listOfCells)
    listOfCells = drawCells(game)
    return listOfCells

def checkCells(totalCells):
    for i in totalCells:
        coordsList = game.cellList[i.x][i.y].loopCells(canvasWidth, canvasHeight, i)
        #renames 8 neighbors to be the actual cells, and not a list of the two coords
        topLeft = game.cellList[coordsList[0][0]][coordsList[0][1]]
        topCent = game.cellList[coordsList[1][0]][coordsList[1][1]]
        topRight = game.cellList[coordsList[2][0]][coordsList[2][1]]
        midLeft = game.cellList[coordsList[3][0]][coordsList[3][1]]
        midRight = game.cellList[coordsList[4][0]][coordsList[4][1]]
        bottomLeft = game.cellList[coordsList[5][0]][coordsList[5][1]]
        bottomCent = game.cellList[coordsList[6][0]][coordsList[6][1]]
        bottomRight = game.cellList[coordsList[7][0]][coordsList[7][1]]
        neighbors = [topLeft.alive, topCent.alive, topRight.alive, midLeft.alive, midRight.alive, bottomLeft.alive, bottomCent.alive, bottomRight.alive].count(True) #counts the neighbors of the current cell
        #updates cell to whether it should be alive or not
        if i.alive:
            if neighbors > 3 or neighbors < 2:
                i.alive = False
        else:
            if neighbors == 3:
                i.alive = True

def drawCells(game): #deletes all cells, and then draws all alive cells
    listOfCells = set()
    for i in game.cellList:
        for j in i:
            pen.delete(j.rectangle) #deletes all living cells
            if j.alive:
                listOfCells.add(j)
                j.rectangle = pen.create_rectangle((j.x * cellSize), (j.y * cellSize), ((j.x * cellSize) + cellSize), ((j.y * cellSize) + cellSize), fill=cellColor[0], outline=cellColor[1]) #draws cell
    return listOfCells

def updateSettings(update, xSize, ySize, cellSizeBox, startingCellsBox, cellColorBox, cellSpacingBox, speedBox):
    #collects data
    global canvasWidth
    global canvasHeight
    global cellSize
    global startingCells
    global cellColor
    global cellSpacing
    global speed
    global master
    toCheck = [xSize, ySize, cellSizeBox, startingCellsBox, cellColorBox, cellSpacingBox, speedBox]
    toAssign = [canvasWidth, canvasHeight, cellSize, startingCells, cellColor, cellSpacing, speed]
    for i in toCheck:
        if len(i.get()) > 0: #only updates variables if there was an entry
            toAssign[toCheck.index(i)] = i.get()
    #update["text"] = "Updated!"
    master.destroy()
    #create canvas
    master = Tk() #create new window or "canvas" called "master"
    master.title("Conway's Game of Life") #window title
    pen = Canvas(master, width = (canvasWidth * cellSize), height = (canvasHeight * cellSize))
    pen.pack()
    game = classes.gameClass(canvasWidth, canvasHeight) #creates game class, where all cells will be held
    resetCanvas()
    #update["text"] = "Update"

def adjustSettings(): #opens settings window; changes window/cell size, starting cells, cell color, etc.
    if inProgress:
        global canvasWidth
        global canvasHeight
        global cellSize
        global cellColor
        global speed
        gameOn = False #turns off the game so it isn't running while settings are being adjusted
        print("Settings opened")
        #creates window
        settingsBox = Tk()
        settingsBox.title("Settings")
        settingsBoxPen = Canvas(settingsBox, width = ((canvasWidth * cellSize) / 2), height = ((canvasHeight * cellSize) / 2))
        settingsBoxPen.pack()
        #labels
        xSizeLabel = Label(settingsBox, text="Canvas width:", font = 50) #canvas x
        xSizeLabel.pack()
        ySizeLabel = Label(settingsBox, text="Canvas height:", font = 50) #canvas y
        ySizeLabel.pack()
        cellSizeLabel = Label(settingsBox, text="Cell size:", font = 50) #cell size
        cellSizeLabel.pack()
        startingCellsLabel = Label(settingsBox, text="Number of starting cells:", font = 50) #starting cells
        startingCellsLabel.pack()
        cellColorLabel = Label(settingsBox, text="Cell color (provide hex code):", font = 50) #cell color
        cellColorLabel.pack()
        cellSpacingLabel = Label(settingsBox, text="Cell spacing (How close together the cells generate):", font = 50) #how close together the cells generate
        cellSpacingLabel.pack()
        speedLabel = Label(settingsBox, text="Game speed:", font = 50) #game speed
        speedLabel.pack()
        #entry boxes
        xSize = Entry (settingsBox)
        settingsBoxPen.create_window(canvasWidth, canvasHeight, window=xSize)
        ySize = Entry (settingsBox)
        settingsBoxPen.create_window(canvasWidth, canvasHeight + 25, window=ySize)
        cellSizeBox = Entry (settingsBox)
        settingsBoxPen.create_window(canvasWidth, canvasHeight + 50, window=cellSizeBox)
        startingCellsBox = Entry (settingsBox)
        settingsBoxPen.create_window(canvasWidth, canvasHeight + 75, window=startingCellsBox)
        cellColorBox = Entry (settingsBox)
        settingsBoxPen.create_window(canvasWidth, canvasHeight + 100, window=cellColorBox)
        cellSpacingBox = Entry (settingsBox)
        settingsBoxPen.create_window(canvasWidth, canvasHeight + 125, window=cellSpacingBox)
        speedBox = Entry (settingsBox)
        settingsBoxPen.create_window(canvasWidth, canvasHeight + 150, window=speedBox)
        #buttons
        closeSettings = Button(settingsBox, command=lambda: quitSettings(settingsBox), text="Close", bd=0, bg="#ff6b6b", padx=10, pady=5, fg="#8f0000", activebackground="#ff3636", activeforeground="#690000") #"lambda" is used so that the function can be called with arguments
        closeSettings.pack(side="right")
        update = Button(settingsBox, command=lambda: updateSettings(update, xSize, ySize, cellSizeBox, startingCellsBox, cellColorBox, cellSpacingBox, speedBox), text="Update", bd=0, bg="#ffe770", padx=10, pady=5, fg="#877100", activebackground="#ffe359", activeforeground="#665500")
        update.pack(side="right")
    else:
        print("This feature is in progress. Come back soon!")

def quit(): #closes the game
    master.destroy()

def quitSettings(settingsBox):
    settingsBox.destroy()

'''code'''
#create canvas
master.title("Conway's Game of Life") #window title
pen = Canvas(master, width = (canvasWidth * cellSize), height = (canvasHeight * cellSize))
pen.pack()
game = classes.gameClass(canvasWidth, canvasHeight) #creates game class, where all cells will be held

#buttons
quit = Button(master, command=quit, text="Quit", bd=0, bg ="#ff6b6b", padx=15, pady=10, fg="#8f0000", activebackground="#ff3636", activeforeground="#690000").pack(side="right")
reset = Button(master, command=resetCanvas, text="Reset", bd=0, bg="#ffe770", padx=15, pady=10, fg="#877100", activebackground="#ffe359", activeforeground="#665500").pack(side="right")
playPause = Button(master, command=resumeGame, text="Play", bd=0, bg="#7df585", padx=15, pady=10, fg="#007a08", activebackground="#5ee067", activeforeground="#005906")
playPause.pack(side="right")
settings = Button(master, command=adjustSettings, text="Settings", bd=0, bg="#ffe770", padx=15, pady=10, fg="#877100", activebackground="#ffe359", activeforeground="#665500") #"lambda" is used so that the function can be called with arguments
settings.pack(side="right")

#labels/text in window
canvasTitle = Label(master, text="Conway's Game of Life", font = 200)
canvasTitle.pack() #pack has to be separate for some reason; else will break
cellCountText = Label(master, text=f"Cell count: {len(listOfCells)}", font = 100)
cellCountText.pack()

resetCanvas()
mainloop() #dunno why this is here tbh, is used for Tkinter