from cmu_graphics import *
from Slashes_Screen import *
from Title_Screen import *
from Mode_Screen import *
from Dojo_Screen import *
from CV_to_Graphics import *
from Default_Mode_Screen import *
from Hack112_CV_Test import *
from Game_Mechanics import *


def onAppStart(app):
    reset(app)
    app.width, app.height = 1024, 1280 # width//2 = 512; height//2 = 640
    
def reset(app):
    setupSlashApp(app)
    setupDojoScreen(app)
    setupTrackerGraphics(app)
    setupMechanicsApp(app)
    setupModeApp(app)
    app.currentScreen = 'Title' 

def redrawAll(app):
    drawCurrentScreen(app)

def drawCurrentScreen(app):
    drawBackground(app)
    if app.currentScreen == 'Title':
        drawTitleScreen(app)
    elif app.currentScreen == 'Slashes':
        drawSlashesScreen(app)
    elif app.currentScreen == 'Dojo':
        drawDojoScreen(app)
    elif app.currentScreen == 'Mode':
        drawModeScreen(app)
    elif app.currentScreen == 'FruitMode':
        drawDefaultModeScreen(app)

def onMousePress(app, mouseX, mouseY):
    checkCurrentClicks(app, mouseX, mouseY)

def checkCurrentClicks(app, mouseX, mouseY):
    if app.currentScreen == 'Title':
        checkTitleClicks(app, mouseX, mouseY)
    elif app.currentScreen == 'Slashes':
        checkSlashClicks(app, mouseX, mouseY)
    elif app.currentScreen == 'Dojo':
        checkDojoClicks(app, mouseX, mouseY)
    elif app.currentScreen == 'Mode':
        checkModeClicks(app, mouseX, mouseY)
    elif app.currentScreen == 'FruitMode':
        pass # playing the game; no clicks


def onStep(app):
    if app.currentScreen == 'FruitMode':
        takeDefaultModeStep(app)
    # ^ only screen that uses onStep

def main():
    runApp()

def onKeyPress(app, key):
    if app.gameOver and key == 'r':
        reset(app)


main()

