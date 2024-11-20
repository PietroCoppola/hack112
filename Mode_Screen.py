from cmu_graphics import *
import os


def onAppStart(app):
    app.width, app.height = 1024, 1280
    setupModeApp(app)

def setupModeApp(app):
    app.gameMode = 'Fruit'
    app.isKosbieMode = False

def loadFruits(app):
    app.fruitImages = {}
    fruits_folder = './images/fruits' if app.gameMode == 'Fruit' else './images/fruits/Kosbie'
    for filename in os.listdir(fruits_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_name = os.path.splitext(filename)[0]
            image_path = os.path.join(fruits_folder, filename)
            app.fruitImages[image_name] = image_path

def redrawAll(app):
    drawModeScreen(app)

def drawModeScreen(app):
    drawLabel("Mode", app.width//2, 50, size=100, bold=True, fill = app.textUIColor)

    normalModeString = 'Play'
    drawLabel(normalModeString, app.width//2, 350, size=50, bold=True, fill =  app.textUIColor)
    drawRect(app.width//2, 350, 130, 70, fill=None, border=app.borderUIColor, borderWidth=3, align='center')

    kosbieModeString = 'Kosbie Mode'
    fill='red'
    border='darkRed'
    if app.isKosbieMode:
        fill='lightGreen'
        border='green'
    drawRect(app.width//2, 550, 326, 70, fill=fill, border=border, borderWidth=3, align='center')
    drawLabel(kosbieModeString, app.width//2, 550, size=50, bold=True)

    homeString = 'Home'
    drawLabel(homeString, 70, app.height-50, size=40, bold=True, fill = app.textUIColor )
    drawRect(70, app.height-50, 120, 60, fill=None, border=app.borderUIColor, borderWidth=3, align='center')


def onMousePress(app, mouseX, mouseY):
    checkModeClicks(app, mouseX, mouseY)

def checkModeClicks(app, x, y):
    if (app.width//2-65 <= x <= app.width//2+65) and (350-35 <= y <= 350+35):
        app.currentScreen = 'FruitMode'
        loadFruits(app)
    elif (app.width//2-163 <= x <= app.width//2+163) and (550-35 <= y <= 550+35):
        app.isKosbieMode = not app.isKosbieMode
        app.gameMode = 'Kosbie' if app.isKosbieMode else 'Fruit'
    elif (70-60 <= x <= 70+60) and (app.height-50-30 <= y <= app.height-50+30):
        app.currentScreen = 'Title'


def main():
    runApp()

# For testing
# main()