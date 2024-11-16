from cmu_graphics import *

def onAppStart(app):
    app.width, app.height = 1280, 1024


def redrawAll(app):
    drawLabel("FRUIT NINJA", app.width//2 + 30, 100, size = 100, fill = 'purple')
    drawRect(400, 200, 500, 200, fill = None, borderWidth = 10, border = 'pink')
    drawRect(400, 450, 500, 200, fill = None, borderWidth = 10, border = 'pink')
    drawRect(400, 700, 500, 200, fill = None, borderWidth = 10, border = 'pink')
    drawLabel("Mode", 655, 300, size = 80)
    drawLabel("Dojos", 655, 550, size = 80)
    drawLabel("Slashes", 655, 800, size = 80)



def onMousePress(app, mouseX, mouseY):
    if 900 >= mouseX >= 400 and 400>= mouseY >= 200:
        mode()
    elif 900 >= mouseX >= 400 and 650>= mouseY >= 450:
        dojos()
    elif 900 >= mouseX >= 400 and 900>= mouseY >= 700:
        slashes()

runApp()

def mode():
    print (1)
def dojos():
    print (2)
def slashes():
    print (3)