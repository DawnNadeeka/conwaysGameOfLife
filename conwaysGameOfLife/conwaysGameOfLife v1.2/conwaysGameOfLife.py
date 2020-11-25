'''Imports and Variables'''
import random, math, string, classes
from tkinter import *

canvasWidth = 60 #canvas width
canvasHeight = 40 #canvas height
cellSize = 10 #the size length of the cell; should fit evenly into both canvasWidth and canvasHeight
startingCells = int(canvasHeight / 2) #how many cells the game should start with
cellColor = "#cce9fc"
cellBorder = "#67acdb"
cellSpacing = 2
gameSpeed = 0.15 #speed of cells (in seconds), or how often it should update to the next generation
listOfCells = set() #empty set, used to hold all alive cells while removing duplicates
gameOn = False #Game starts turned off

'''Functions'''
def checkered(canvas, lineDistance): #draws lines
    #vertical lines, each lineDistance pixels apart
    for x in range(lineDistance, (canvasWidth * cellSize), lineDistance):
        canvas.create_line(x, 0+60, x, (canvasHeight * cellSize)+60, fill=cellColor)
    #horizontal lines, each lineDistance pixels apart
    for y in range(lineDistance, (canvasHeight * cellSize), lineDistance):
        canvas.create_line(0, y+60, (canvasWidth * cellSize), y+60, fill=cellColor)

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
    pen.create_rectangle(0, 0+60, (canvasWidth * cellSize), (canvasHeight * cellSize)+60, fill="#ffffff", outline=cellColor) #draws border
    for i in game.cellList: #deletes any alive drawn cells
        for j in i:
            j.alive = False
            pen.delete(j.rectangle)
    checkered(pen, cellSize) #draws grid
    listOfCells = startingBoard()
    cellCountText.configure(text=f"Cell count: {len(listOfCells)}")

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
        listOfCells = nextGen()
        cellCountText.configure(text=f"Cell count: {len(listOfCells)}") #won't work?
    master.after(int(gameSpeed * 1000), checkIfOn) #how long to wait before running the function again

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
                j.rectangle = pen.create_rectangle((j.x * cellSize), (j.y * cellSize)+60, ((j.x * cellSize) + cellSize), ((j.y * cellSize) + cellSize)+60, fill=cellColor, outline=cellBorder) #draws cell
    return listOfCells

def resetSettings(canvasWidthBox, canvasHeightBox, cellSizeBox, startingCellsBox, cellColorBox, cellBorderBox, cellSpacingBox, gameSpeedBox):
    #The default settings
    canvasWidthBox.delete(0, END)
    canvasWidthBox.insert(0, 60)
    canvasHeightBox.delete(0, END)
    canvasHeightBox.insert(0, 40)
    cellSizeBox.delete(0, END)
    cellSizeBox.insert(0, 10)
    startingCellsBox.delete(0, END)
    startingCellsBox.insert(0, 20)
    cellColorBox.delete(0, END)
    cellColorBox.insert(0, "#cce9fc")
    cellBorderBox.delete(0, END)
    cellBorderBox.insert(0, "#67acdb")
    cellSpacingBox.delete(0, END)
    cellSpacingBox.insert(0, 2)
    gameSpeedBox.delete(0, END)
    gameSpeedBox.insert(0, 0.15)

def updateSettings(labelsList, settingsBox, settingsPen, canvasWidthBox, canvasHeightBox, cellSizeBox, startingCellsBox, cellColorBox, cellBorderBox, cellSpacingBox, gameSpeedBox):
    #collects data
    global canvasWidth
    global canvasHeight
    global cellSize
    global startingCells
    global cellColor
    global cellBorder
    global cellSpacing
    global gameSpeed
    global master
    global game

    #These cells would need to update the canvas (things like color don't need to, and shouldn't if someone wants to save their game board)
    if (int(float(canvasWidthBox.get())) > 0 and (not int(float(canvasWidthBox.get())) == canvasWidth)) or (int(float(canvasHeightBox.get())) > 0 and (not int(float(canvasHeightBox.get()))) == canvasHeight) or (int(float(cellSizeBox.get())) > 0 and (not int(float(cellSizeBox.get())) == cellSize)):
        doUpdateCanvas = True
    else:
        doUpdateCanvas = False
    print(int(float(canvasWidthBox.get())), canvasWidth, doUpdateCanvas)

    #Entry box updates
    if int(float(canvasWidthBox.get())) > 0:
        canvasWidth = int(float(canvasWidthBox.get())) #float and then int has to be cast to turn the string to a decimal, and then an integer (in case the number given was a decimal)
        canvasWidthBox.configure(bg=cellColor, fg=cellBorder)
    if int(float(canvasHeightBox.get())) > 0:
        canvasHeight = int(float(canvasHeightBox.get()))
        canvasHeightBox.configure(bg=cellColor, fg=cellBorder)
    if int(float(cellSizeBox.get())) > 0:
        cellSize = int(float(cellSizeBox.get()))
        cellSizeBox.configure(bg=cellColor, fg=cellBorder)
    if int(float(startingCellsBox.get())) > 0:
        startingCells = int(float(startingCellsBox.get()))
        startingCellsBox.configure(bg=cellColor, fg=cellBorder)
    #if len(cellColorBox.get()) == 7 and cellColorBox.get()[0] == "#" and int(cellColorBox.get()[1:6]):
    if len(cellColorBox.get()) == 7 and all(i in string.hexdigits for i in cellColorBox.get()[1:7]):
        cellColor = cellColorBox.get()
        cellColorBox.configure(bg=cellColor, fg=cellBorder)
    if len(cellBorderBox.get()) == 7 and cellBorderBox.get()[0] == "#":
        cellBorder = cellBorderBox.get()
        cellBorderBox.configure(bg=cellColor, fg=cellBorder)
    if int(float(cellSpacingBox.get())) > 0:
        cellSpacing = int(float(cellSpacingBox.get()))
        cellSpacingBox.configure(bg=cellColor, fg=cellBorder)
    if float(gameSpeedBox.get()) > 0:
        gameSpeed = float(gameSpeedBox.get())
        gameSpeedBox.configure(bg=cellColor, fg=cellBorder)

    #Canvases
    if canvasWidth * cellSize < 340: #prevents the window from getting so small it can't display the buttons
        pen.configure(width=340, height=((canvasHeight * cellSize) + 130), bg=cellBorder, highlightbackground=cellBorder) 
    else:
        pen.configure(width=(canvasWidth * cellSize), height=((canvasHeight * cellSize) + 130), bg=cellBorder, highlightbackground=cellBorder)
    master.configure(bg=cellBorder)
    settingsBox.configure(bg=cellBorder)
    settingsPen.configure(bg=cellBorder, highlightbackground=cellBorder)

    game = classes.gameClass(canvasWidth, canvasHeight)

    #Labels
    canvasTitle.configure(fg=cellColor, bg=cellBorder)
    cellCountText.place(y=(canvasHeight*cellSize)+65)
    cellCountText.configure(fg=cellColor, bg=cellBorder)
    for i in labelsList:
            i.configure(fg=cellColor, bg=cellBorder)
            if i == labelsList[4]:
                i.configure(text=f"Canvas width ({canvasWidth}):")
            if i == labelsList[7]:
                i.configure(text=f"Canvas height ({canvasHeight}):")
            if i == labelsList[10]:
                i.configure(text=f"Cell size ({cellSize}):")
            if i == labelsList[13]:
                i.configure(text=f"Starting cells ({startingCells}):")
            if i == labelsList[16]:
                i.configure(text=f"Cell color ({cellColor}):")
            if i == labelsList[19]:
                i.configure(text=f"Cell border ({cellBorder}):")
            if i == labelsList[22]:
                i.configure(text=f"Cell spacing ({cellSpacing}):")
            if i == labelsList[25]:
                i.configure(text=f"Game speed ({gameSpeed}):")

    #Buttons
    playPause.place(x=2, y=(canvasHeight*cellSize)+90)
    reset.place(x=77, y=(canvasHeight*cellSize)+90)
    settings.place(x=152, y=(canvasHeight*cellSize)+90)
    if (canvasWidth*cellSize)-69 < 227: #233 is the number that adds up all the button spacings
        quitButton.place(x=227, y=(canvasHeight*cellSize)+90)
    else:
        quitButton.place(x=(canvasWidth*cellSize)-69, y=(canvasHeight*cellSize)+90)
    
    if doUpdateCanvas:
        resetCanvas()

def openSettings(): #opens settings window; changes window/cell size, starting cells, cell color, etc.
    if gameOn: #turns off the game so it isn't running while settings are being adjusted
        resumeGame()
    #creates window
    settingsBox = Toplevel(bg=cellBorder, bd=10)
    settingsBox.title("Settings")
    settingsBox.resizable(False, False) #disables resize screen
    settingsPen = Canvas(settingsBox, width=475, height=405, bg=cellBorder, highlightbackground=cellBorder)
    settingsPen.grid()
    '''labels'''
    #settings
    settingsTitle = Label(settingsBox, text="Settings", font = ("", 16), fg=cellColor, bg=cellBorder)
    settingsTitle.place(x=5)
    settingsDesc = Label(settingsBox, text=f"Adjust the game settings. All numbers must be postive integers, and the colors \nmust be 6-digit hex codes. Large and small numbers may impact performance.", font = ("", 10), fg=cellColor, bg=cellBorder, justify=LEFT)
    settingsDesc.place(x=5, y=30)
    #canvas width
    canvasWidthLabel = Label(settingsBox, text=f"Canvas width ({canvasWidth}):", font = ("", 12), fg=cellColor, bg=cellBorder)
    canvasWidthLabel.place(x=5, y=75)
    canvasWidthDesc = Label(settingsBox, text="The width of the board. Multiples of \n10 recommended.", font = ("", 10), fg=cellColor, bg=cellBorder, justify=LEFT)
    canvasWidthDesc.place(x=10, y=100)
    #canvas height
    canvasHeightLabel = Label(settingsBox, text=f"Canvas height ({canvasHeight}):", font = ("", 12), fg=cellColor, bg=cellBorder)
    canvasHeightLabel.place(x=240, y=75)
    canvasHeightDesc = Label(settingsBox, text="The hight of the board. Multiples of \n10 recommended.", font = ("", 10), fg=cellColor, bg=cellBorder, justify=LEFT)
    canvasHeightDesc.place(x=250, y=100)
    #cell size
    cellSizeLabel = Label(settingsBox, text=f"Cell size ({cellSize}):", font = ("", 12), fg=cellColor, bg=cellBorder)
    cellSizeLabel.place(x=5, y=150)
    cellSizeDesc = Label(settingsBox, text="The size of each cell.", font = ("", 10), fg=cellColor, bg=cellBorder, justify=LEFT)
    cellSizeDesc.place(x=10, y=175)
    #starting cells
    startingCellsLabel = Label(settingsBox, text=f"Starting cells ({startingCells}):", font = ("", 12), fg=cellColor, bg=cellBorder)
    startingCellsLabel.place(x=240, y=150)
    startingCellsDesc = Label(settingsBox, text="The approximate number of starting \ncells. Will sometimes be less.", font = ("", 10), fg=cellColor, bg=cellBorder, justify=LEFT)
    startingCellsDesc.place(x=250, y=175)
    #cell color
    cellColorLabel = Label(settingsBox, text=f"Cell color ({cellColor}):", font = ("", 12), fg=cellColor, bg=cellBorder)
    cellColorLabel.place(x=5, y=225)
    cellColorDesc = Label(settingsBox, text="The color of each cell, grid lines, and \ntext. Wrong codes may break.", font = ("", 10), fg=cellColor, bg=cellBorder, justify=LEFT)
    cellColorDesc.place(x=10, y=250)
    #cell border
    cellBorderLabel = Label(settingsBox, text=f"Cell border ({cellBorder}):", font = ("", 12), fg=cellColor, bg=cellBorder)
    cellBorderLabel.place(x=240, y=225)
    cellBorderDesc = Label(settingsBox, text="The color of each cell border and game \nbackground. Wrong codes may break.", font = ("", 10), fg=cellColor, bg=cellBorder, justify=LEFT)
    cellBorderDesc.place(x=250, y=250)
    #cell spacing
    cellSpacingLabel = Label(settingsBox, text=f"Cell spacing ({cellSpacing}):", font = ("", 12), fg=cellColor, bg=cellBorder)
    cellSpacingLabel.place(x=5, y=300)
    cellSpacingDesc = Label(settingsBox, text="The space between cells during \nranomization.", font = ("", 10), fg=cellColor, bg=cellBorder, justify=LEFT)
    cellSpacingDesc.place(x=10, y=325)
    #game speed
    gameSpeedLabel = Label(settingsBox, text=f"Game speed ({gameSpeed}):", font = ("", 12), fg=cellColor, bg=cellBorder)
    gameSpeedLabel.place(x=240, y=300)
    gameSpeedDesc = Label(settingsBox, text="The amount of time between each \ngeneration. Can be a decimal.", font = ("", 10), fg=cellColor, bg=cellBorder, justify=LEFT)
    gameSpeedDesc.place(x=250, y=325)

    '''entry boxes'''
    canvasWidthBox = Entry(settingsBox, width=10, bd=0, bg=cellColor, fg=cellBorder)
    canvasWidthBox.place(x=170, y=79)
    canvasWidthBox.insert(0, canvasWidth)

    canvasHeightBox = Entry(settingsBox, width=10, bd=0, bg=cellColor, fg=cellBorder)
    canvasHeightBox.place(x=410, y=79)
    canvasHeightBox.insert(0, canvasHeight)

    cellSizeBox = Entry(settingsBox, width=10, bd=0, bg=cellColor, fg=cellBorder)
    cellSizeBox.place(x=170, y=154)
    cellSizeBox.insert(0, cellSize)

    startingCellsBox = Entry(settingsBox, width=10, bd=0, bg=cellColor, fg=cellBorder)
    startingCellsBox.place(x=410, y=154)
    startingCellsBox.insert(0, startingCells)

    cellColorBox = Entry(settingsBox, width=10, bd=0, bg=cellColor, fg=cellBorder)
    cellColorBox.place(x=170, y=229)
    cellColorBox.insert(0, cellColor)

    cellBorderBox = Entry(settingsBox, width=10, bd=0, bg=cellColor, fg=cellBorder)
    cellBorderBox.place(x=410, y=229)
    cellBorderBox.insert(0, cellBorder)
    
    cellSpacingBox = Entry(settingsBox, width=10, bd=0, bg=cellColor, fg=cellBorder)
    cellSpacingBox.place(x=170, y=304)
    cellSpacingBox.insert(0, cellSpacing)

    gameSpeedBox = Entry(settingsBox, width=10, bd=0, bg=cellColor, fg=cellBorder)
    gameSpeedBox.place(x=410, y=304)
    gameSpeedBox.insert(0, gameSpeed)

    '''buttons'''
    #This list is long so that I don't have to have all of these variables listed in every function call that uses it
    labelsList = [settingsTitle, settingsDesc, version, author, canvasWidthLabel, canvasWidthDesc, canvasWidthBox, canvasHeightLabel, canvasHeightDesc, canvasHeightBox, cellSizeLabel, cellSizeDesc, cellSizeBox, startingCellsLabel, startingCellsDesc, startingCellsBox, cellColorLabel, cellColorDesc, cellColorBox, cellBorderLabel, cellBorderDesc, cellBorderBox, cellSpacingLabel, cellSpacingDesc, cellSpacingBox, gameSpeedLabel, gameSpeedDesc, gameSpeedBox]
    closeSettings = Button(settingsBox, command=settingsBox.destroy, text="Close", bd=0, bg="#ff6b6b", padx=10, pady=5, fg="#8f0000", activebackground="#ff3636", activeforeground="#690000", width=5) #"lambda" is used so that the function can be called with arguments
    closeSettings.place(x=413, y=373)
    update = Button(settingsBox, command=lambda: updateSettings(labelsList, settingsBox, settingsPen, canvasWidthBox, canvasHeightBox, cellSizeBox, startingCellsBox, cellColorBox, cellBorderBox, cellSpacingBox, gameSpeedBox), text="Update", bd=0, bg="#7df585", padx=10, pady=5, fg="#007a08", activebackground="#5ee067", activeforeground="#005906", width=5)
    update.place(x=283, y=373)
    resetSettingsButton = Button(settingsBox, command=lambda: resetSettings(canvasWidthBox, canvasHeightBox, cellSizeBox, startingCellsBox, cellColorBox, cellBorderBox, cellSpacingBox, gameSpeedBox), text="Reset", bd=0, bg="#ffe770", padx=10, pady=5, fg="#877100", activebackground="#ffe359", activeforeground="#665500", width=5)
    resetSettingsButton.place(x=348, y=373)

'''code'''
#create canvas
master = Tk() #create new window or "canvas" called "master"
master.title("Conway's Game of Life") #window title
master.configure(bg = cellBorder, bd=10)
master.resizable(False, False) #disables resize screen
pen = Canvas(master, width=(canvasWidth * cellSize), height=(canvasHeight * cellSize) + 130, bg=cellBorder, highlightbackground=cellBorder)
pen.pack()
game = classes.gameClass(canvasWidth, canvasHeight) #creates game class, where all cells will be held

#buttons
playPause = Button(master, command=resumeGame, text="Play", bd=0, bg="#7df585", padx=15, pady=10, fg="#007a08", activebackground="#5ee067", activeforeground="#005906", width=5)
playPause.place(x=3, y=(canvasHeight*cellSize)+90)
reset = Button(master, command=resetCanvas, text="Reset", bd=0, bg="#ffe770", padx=15, pady=10, fg="#877100", activebackground="#ffe359", activeforeground="#665500", width=5)
reset.place(x=78, y=(canvasHeight*cellSize)+90)
settings = Button(master, command=openSettings, text="Settings", bd=0, bg="#ffe770", padx=15, pady=10, fg="#877100", activebackground="#ffe359", activeforeground="#665500", width=5)
settings.place(x=153, y=(canvasHeight*cellSize)+90)
quitButton = Button(master, command=master.destroy, text="Quit", bd=0, bg ="#ff6b6b", padx=15, pady=10, fg="#8f0000", activebackground="#ff3636", activeforeground="#690000", width=5)
quitButton.place(x=(canvasWidth*cellSize)-69, y=(canvasHeight*cellSize)+90)
#labels/text in window
canvasTitle = Label(master, text="Conway's Game of Life", font = ("", 18), fg=cellColor, bg=cellBorder)
canvasTitle.place(x=5) #pack has to be separate for some reason; else will break
version = Label(master, text="v.1.2 Nov. 2020", font = ("", 8), anchor="center", fg=cellColor, bg=cellBorder) #Version and date updated
version.place(x=257, y=10)
author = Label(master, text="By Raya Ronaghy", font = ("", 8), anchor="center", fg=cellColor, bg=cellBorder) #Author name
author.place(x=9, y=30)
cellCountText = Label(master, text=f"Cell count: {len(listOfCells)}", font = ("", 12), anchor="center", fg=cellColor, bg=cellBorder) #displays how many cells are on the board
cellCountText.place(y=(canvasHeight*cellSize)+65)

resetCanvas()
mainloop() #dunno why this is here tbh, is used for Tkinter