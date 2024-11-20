from cmu_graphics import *
from CV_to_Graphics import *
from Hack112_CV_Test import *
from Game_Mechanics import *
from Slashes_Screen import *

def onAppStart(app):
    setupMechanicsApp(app)
    setupTrackerGraphics(app)
    setupSlashApp(app)
    
    app.width = 1024
    app.height = 1280

def redrawAll(app):
    drawDefaultModeScreen(app)

def drawDefaultModeScreen(app):
     drawMechanics(app)
     drawCountdown(app)
     drawCharacterSwipe(app)
     
    
def onStep(app):
    takeDefaultModeStep(app)

def takeDefaultModeStep(app):
    takeMechanicsStep(app)
    initialGamePause(app)
    if not app.countdown:
        app.startTracker = True
    takeCVStep(app)

def main():
    runApp()

# main()

   
