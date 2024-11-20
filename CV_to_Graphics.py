from cmu_graphics import *
from Hack112_CV_Test import *
from collections import deque
from Game_Mechanics import *
import threading

def onAppStart(app):
    setupTrackerGraphics(app)
    setupMechanicsApp(app)
    app.width = 1024
    app.height = 1280

def setupTrackerGraphics(app):
    app.displayCount = 3
    app.countdown = True
    app.timeCounter = 0
    app.pastCoords = deque()
    app.stepsPerSecond = 30
    app.stopTracker = False
    app.startTracker = False
    app.trackerStarted = False
    app.pointerX = None
    app.pointerY = None

def redrawAll(app):
    drawCountdown(app)
    drawCharacterSwipe(app)
    
def drawCharacterSwipe(app):
    if not app.gameOver and not app.countdown:
        if len(app.pastCoords) > 1:
            for i in range(len(app.pastCoords)-1):
                x1, y1 = app.pastCoords[i]
                x2, y2 = app.pastCoords[i+1]
                x1 *= app.width
                x2 *= app.width
                y1 *= app.height
                y2 *= app.height
                drawLine(x1, y1, x2, y2, dashes=app.lineDashes, lineWidth=app.lineWidth, fill=app.slashColors[app.slashColorIndex])

def initialGamePause(app):
    if app.countdown:
        app.timeCounter += 1
        if app.timeCounter % 30 == 0: # 30 sps
            app.displayCount -= 1
        if app.displayCount == 0:
            app.countdown = False

def drawCountdown(app):
    if app.countdown:
        drawLabel(f'{app.displayCount}', app.width//2, app.height//2, size=150, bold=True, fill=app.textUIColor)

def onStep(app):
    initialGamePause(app)
    if not app.countdown:
        app.startTracker = True
    takeCVStep(app)

def startTracking(app):
    if app.startTracker and not app.trackerStarted:
        app.trackerStarted = True
        handTrackerThread = threading.Thread(target=hand_tracker, args=(app,))
        handTrackerThread.daemon = True  # Ensure it closes when the app exits
        handTrackerThread.start()

def takeCVStep(app):
    startTracking(app)
    if app.gameOver:
        setGlobalCoords(deque())
        app.pastCoords = getGlobalCoords()
        print(app.pastCoords)
        app.stopTracker = True
    else:
        app.pastCoords = getGlobalCoords()
        if len(app.pastCoords) > 0:
            app.pointerX, app.pointerY = app.pastCoords[-1]
            print(app.pointerX, app.pointerY)
    

def onKeyPress(app, key):
    checkCVKeys(app, key)

def checkCVKeys(app, key):
    if key == 'q':
        app.stopTracker = True

def main():
    runApp()

# main()

