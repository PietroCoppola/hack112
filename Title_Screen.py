from cmu_graphics import *
from Slashes_Screen import *


def onAppStart(app):
    app.width, app.height = 1024, 1280

def redrawAll(app):
    drawTitleScreen(app)

def drawTitleScreen(app):
    drawImage('./images/gui/112Ninja.png', app.width//2-150, 50, width = 330, height = 240)

    drawLabel("Mode", app.width//2, 350, size=50, bold=True, fill = app.textUIColor)
    drawRect(app.width//2, 350, 150, 70, fill=None, borderWidth=3, border=app.borderUIColor, align='center')

    drawLabel("Dojos", app.width//2, 550, size=50, bold=True, fill = app.textUIColor)
    drawRect(app.width//2, 550, 170, 70, fill=None, borderWidth=3, border=app.borderUIColor, align='center')

    drawLabel("Slashes", app.width//2, 750, size=50, bold=True, fill = app.textUIColor)
    drawRect(app.width//2, 750, 220, 70, fill=None, borderWidth=3, border=app.borderUIColor, align='center')

def onMousePress(app, mouseX, mouseY):
    checkTitleClicks(app, mouseX, mouseY)

def checkTitleClicks(app, x, y):
    if (app.width//2-75 <= x <= app.width//2+75) and (350-70 <= y <= 350+70):
        app.currentScreen = 'Mode'
    elif (app.width//2-85 <= x <= app.width//2+85) and (550-35 <= y <= 550+35):
        app.currentScreen = 'Dojo'
    elif (app.width//2-110 <= x <= app.width//2+110) and (750-35 <= y <=750+35):
        app.currentScreen = 'Slashes'

# runApp()
