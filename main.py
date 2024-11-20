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
    # Kept for reference
    # app.uiColor = rgb(247, 182, 63)

    app.borderUIColor = rgb(245,156,52)
    app.textUIColor = rgb(250, 226, 83)

    reset(app)
    app.width, app.height = 1024, 1280 # width//2 = 512; height//2 = 640
    
def reset(app):
    # Set up variables needed by each screen
    setupSlashApp(app)
    setupDojoScreen(app)
    setupTrackerGraphics(app)
    setupMechanicsApp(app)
    setupModeApp(app)
    app.currentScreen = 'Title' 

def redrawAll(app):
    drawCurrentScreen(app)

# Change the current screen based on app.currentScreen
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

# Detect mouse clicks
def onMousePress(app, mouseX, mouseY):
    checkCurrentClicks(app, mouseX, mouseY)

# Check for mouse clicks based on the current screen
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

