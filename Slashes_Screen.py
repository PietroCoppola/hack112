from cmu_graphics import *

def onAppStart(app):
    app.width, app.height = 1024, 1280
    setupSlashApp(app)

def setupSlashApp(app):
    app.lineDashes = False
    app.lineWidth = 10
    app.slashColors = ['red',
                      'orange',
                      'gold',
                      'green',
                      'mediumAquamarine',
                      'blue',
                      'midnightBlue',
                      'darkOrchid',
                      'hotPink',
                      'peru',
                      'darkGray',
                      'black']
    app.slashColorIndex = 0


def redrawAll(app):
    drawSlashesScreen(app)

def drawSlashesScreen(app):
    drawLabel("Slashes", app.width//2, 50, size=100, bold=True, fill = app.textUIColor)

    dashesString = f'Dashed: {str(app.lineDashes)[0]}'
    drawLine(app.width//2-125, 320, app.width//2+125, 320, dashes = app.lineDashes, fill=app.borderUIColor, lineWidth=10)
    drawLabel(dashesString, app.width//2, 250, bold=True, size=50, fill = app.textUIColor)
    drawRect(app.width//2, 250, 270, 70, fill=None, border=app.borderUIColor, borderWidth=3, align='center')

    colorString = 'Color: '
    color = app.slashColors[app.slashColorIndex]
    drawRect(app.width//2+105, 453, 37, 37, fill=color, align='center')
    drawLabel(colorString, app.width//2, 450, bold=True, size=50,fill = app.textUIColor)
    drawRect(app.width//2, 450, 360, 70, fill=None, border=app.borderUIColor, borderWidth=3, align='center')

    widthString = f'Width: {app.lineWidth}'
    drawLabel(widthString, app.width//2, 650, bold=True, size=50, fill = app.textUIColor)
    drawRect(app.width//2, 650, 300, 70, fill=None, border=app.borderUIColor, borderWidth=3, align='center')

    homeString = 'Home'
    drawLabel(homeString, 70, app.height-50, size=40, bold=True, fill = app.textUIColor)
    drawRect(70, app.height-50, 120, 60, fill=None, border=app.borderUIColor, borderWidth=3, align='center')

def onMousePress(app, mouseX, mouseY):
    checkSlashClicks(app, mouseX, mouseY)

def checkSlashClicks(app, x, y):
    print(x, y)
    if (512-135 <= x <= 512+135) and (250-35 <= y <= 250+35): # dashes
        app.lineDashes = not app.lineDashes
    elif (512-180 <= x <= 512+180) and (450-35 <= y <= 450+35): # color
        app.slashColorIndex += 1
        app.slashColorIndex %= len(app.slashColors)
    elif (512-150 <= x <= 512+150) and (650-35 <= y <= 650+35): # width
        app.lineWidth %= 20 # keeps width on [1,6]
        if app.lineWidth == 0:
            app.lineWidth = 9
        app.lineWidth += 1
    elif (70-60 <= x <= 70+60) and (app.height-50-30 <= y <= app.height-50+30):
        app.currentScreen = 'Title'

def main():
    runApp()

# main()