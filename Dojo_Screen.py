from cmu_graphics import *
import os
import math

def onAppStart(app):
    app.width, app.height = 1024, 1280
    setupDojoScreen(app)

def setupDojoScreen(app):
    app.rows = 4
    app.cols = 4
    app.boardLeft = 162
    app.boardTop = 130
    app.boardWidth = 700
    app.boardHeight = 700
    app.cellBorderWidth = 4
    app.selection = None
    loadImages(app)

def redrawAll(app):
    drawDojoScreen(app)

def drawDojoScreen(app):
    drawLabel('Dojos', app.width//2, 50, size=100, bold=True, fill = app.textUIColor)
    drawBoard(app)
    drawBoardBorder(app)

    homeString = 'Home'
    drawLabel(homeString, 70, app.height-50, size=40, bold=True, fill = app.textUIColor)
    drawRect(70, app.height-50, 120, 60, fill=None, border=app.borderUIColor, borderWidth=3, align='center')

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col, row*app.cols + col + 1)

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
          fill=None, border='black',
          borderWidth=2*app.cellBorderWidth)
    
def loadImages(app):
    app.dojoImages = {}
    dojos_folder = './Images/Dojos/Preview'
    for filename in os.listdir(dojos_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_name = os.path.splitext(filename)[0]
            image_path = os.path.join(dojos_folder, filename)
            app.dojoImages[image_name] = image_path

def drawCell(app, row, col, dojoNumber):
    imageName = 'Dojo' + str(dojoNumber)
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    color = 'lime' if (row, col) == app.selection else None
    borderColor = 'lime' if (row, col) == app.selection else 'black'
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border=borderColor,
             borderWidth=app.cellBorderWidth)
    drawImage(app.dojoImages[imageName], cellLeft, cellTop, width = cellWidth , height = cellHeight)

def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
      return (row, col)
    else:
      return None

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def onMousePress(app, mouseX, mouseY):
    checkDojoClicks(app, mouseX, mouseY)

def checkDojoClicks(app, x, y):
    selectedCell = getCell(app, x, y)
    
    if selectedCell != None:
      if selectedCell == app.selection:
          app.selection = None
          app.selectedDojoScreen = 'Dojo1'
      else:
          app.selection = selectedCell
          app.selectedDojoScreen = f'Dojo{app.selection[0]*4+app.selection[1]+1}'
    elif (70-60 <= x <= 70+60) and (app.height-50-30 <= y <= app.height-50+30):
        app.currentScreen = 'Title'


def main():
    runApp()

# main()