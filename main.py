from cmu_graphics import *
from random import randint, choice, uniform
import os

def onAppStart(app):
    app.width, app.height = 1024, 1280
    app.fruits = []
    app.slicedFruits = []
    app.store = FruitStore()
    app.controller = GameController(app)
    app.stepsPerSecond = 30
    app.score = 0
    app.gameOver = False
    app.strikes = 0
    app.exploding = False
    app.spawnCounter = 0
    app.fruitSpawnInterval = 100
    app.explosionOpacity = 50
    app.elapsedTime = 0
    app.homeScreen = True
    loadImages(app)
    
def loadImages(app):
    app.fruitImages = {}
    fruits_folder = './images/fruits'
    app.dojoImages = {}
    dojos_folder = './images/dojos'
    app.guiImages = {}
    gui_folder = './images/gui'
    for filename in os.listdir(fruits_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_name = os.path.splitext(filename)[0]
            image_path = os.path.join(fruits_folder, filename)
            app.fruitImages[image_name] = image_path
    for filename in os.listdir(dojos_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_name = os.path.splitext(filename)[0]
            image_path = os.path.join(dojos_folder, filename)
            app.dojoImages[image_name] = image_path
    for filename in os.listdir(gui_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_name = os.path.splitext(filename)[0]
            image_path = os.path.join(gui_folder, filename)
            app.guiImages[image_name] = image_path

# Fruit Object 
class Fruit:
    def __init__(self, app, x, y, vX, vY, color, radius):
        self.x = x
        self.y = y
        self.vX = vX
        self.vY = vY
        self.entryPoint = (x,y)
        self.color = color
        self.radius = radius
        self.time = 0
        self.app = app
        self.alignment = 'center'

    def move(self):
        self.time += 1 / self.app.stepsPerSecond
        if self.time >= .5:
            gravity = 880 / self.app.stepsPerSecond
        elif self.time >= 2.5:
            gravity = 0
        else: # Create initial push
            gravity = -75 / (1+self.time)
        self.x, self.y, = calculateProjectileMotion(self.x, self.y, self.vX, self.vY, gravity, self.time)

    def inBounds(self):
        if self.time < 0.2:
            return True
        return (self.y - self.radius < self.app.height and 
                self.x + self.radius > 0 and 
                self.x - self.radius < self.app.width)
    
    def slice(self):
        self.app.store.removeFruit(self)
        speedDifference = uniform(0.1, 0.3)
        if self.vX > 0:
            rightSlicevX = self.vX * (1-speedDifference) + 1
            leftSlicevX = self.vX * (speedDifference) - 1
        else:
            rightSlicevX = self.vX * (speedDifference) + 1
            leftSlicevX = self.vX * (1-speedDifference) - 1
        rightSlice = SlicedFruit(self.app, self.x, self.y, rightSlicevX, self.vY, self.color, self.radius, self.time, 'Right')
        leftSlice = SlicedFruit(self.app, self.x, self.y, leftSlicevX, self.vY, self.color, self.radius, self.time, 'Left')
        self.app.store.addSlicedFruit(rightSlice)
        self.app.store.addSlicedFruit(leftSlice)
        self.app.store.addSplat(Splat(self.app, self.x, self.y, self.color))


class SlicedFruit(Fruit):
    def __init__(self, app, x, y, vX, vY, color, radius, time, side):
        self.app = app
        self.x = x
        self.y = y
        self.vX = vX
        self.vY = vY
        self.color = side + color[-1]
        self.radius = radius
        self.time = time
        self.alignment = 'right' if side == 'Left' else 'left'

    def slice(self):
        pass       
    
class Bomb(Fruit):
    def __init__(self, app, x, y, vX, vY, color, radius):
        super().__init__(app, x, y, vX, vY, color, radius)
        self.alignment = 'center'

    def slice(self):
        self.app.exploding = True
        # TODO: DO BOMB STUFFS

class Splat:
    def __init__(self, app, x, y, color):
        self.app = app
        self.x = x
        self.y = y
        self.color = 'Splat' + color[-1]
        self.opacity = 100

class FruitStore:
    def __init__(self):
        self.fruits = []
        self.slicedFruits = []
        self.bombs = []
        self.splats = []

    def addFruit(self, fruit):
        self.fruits.append(fruit)
    def removeFruit(self, fruit):
        self.fruits.remove(fruit)
    def getFruits(self):
        return self.fruits

    def addSlicedFruit(self, slicedFruit):
        self.slicedFruits.append(slicedFruit)
    def removeSlicedFruit(self, slicedFruit):
        self.slicedFruits.remove(slicedFruit)
    def getSlicedFruits(self):
        return self.slicedFruits
    
    def addSplat(self, splat):
        self.splats.append(splat)
    def reduceSplatOpacity(self, splat):
        splat.opacity -= 5
        if splat.opacity <= 0:
            self.splats.remove(splat)
    def getSplats(self):
        return self.splats

    def addBomb(self, bomb):
        self.bombs.append(bomb)
    def removeBomb(self, bomb):
        self.bombs.remove(bomb)
    def getBombs(self):
        return self.bombs


class GameController:
    def __init__(self, app):
        self.store = app.store
        self.app = app
        self.speedMultiplier = 1.0

    def createFruit(self):
        color, radius = choice([('Fruit1', 80), ('Fruit2', 65), ('Fruit3', 75), ('Fruit4', 100), ('Bomb', 50)])
        x = randint(radius, self.app.width - radius)
        y = self.app.height + radius
        vX = uniform(1, 4)
        vY = (-randint(920, 972))/(self.app.stepsPerSecond)
        xCenter = self.app.width / 2
        vX *= (xCenter - x) / (self.app.width/2.5)
        vY *= self.speedMultiplier
        if color == 'Bomb':
            bomb = Bomb(self.app, x, y, vX, vY, color, radius)
            self.store.addBomb(bomb)
        else:
            fruit = Fruit(self.app, x, y, vX, vY, color, radius)
            self.store.addFruit(fruit)

    def updateFruits(self):
        for fruit in self.store.getFruits()[:]:
            fruit.move()
            if not fruit.inBounds():
                self.app.strikes += 1
                if self.app.strikes > 3: self.app.strikes = 3
                self.store.removeFruit(fruit)
        for slicedFruit in self.store.getSlicedFruits()[:]:
            slicedFruit.move()
            if not slicedFruit.inBounds():
                self.store.removeSlicedFruit(slicedFruit)
        for bomb in self.store.getBombs()[:]:
            bomb.move()
            if not bomb.inBounds():
                self.store.removeBomb(bomb)
        for splat in self.store.getSplats()[:]:
            self.store.reduceSplatOpacity(splat)
                


def redrawAll(app):
    for slicedFruit in app.store.getSlicedFruits():
        drawFruit(app, slicedFruit)
    for fruit in app.store.getFruits():
        drawFruit(app, fruit)
    for bomb in app.store.getBombs():
        drawFruit(app, bomb)
    for splat in app.store.getSplats():
        drawSplat(app, splat)
    drawLives(app)
    drawLabel(f'Score : {app.score}', 100, 50, size = 33)
    if app.exploding:
        drawRect(0, 0, app.width, app.height, fill='white', opacity=app.explosionOpacity)
        
    if app.gameOver:
        drawLabel("Game Over!", app.width / 2, app.height / 2, size=60, align='center')

def drawFruit(app, fruit):
    imageWidth, imageHeight = getImageSize(app.fruitImages[fruit.color])
    if fruit.color == 'Bomb': 
        imageWidth *= 2
        imageHeight *= 2
    drawImage(app.fruitImages[fruit.color], fruit.x, fruit.y, width=imageWidth/2, height=imageHeight/2, align=fruit.alignment)
    if fruit.color == 'Bomb' and app.exploding:
        drawLabel("BOOM!", fruit.x, fruit.y, size=60, align='center')

def drawSplat(app, splat):
    imageWidth, imageHeight = getImageSize(app.fruitImages[splat.color])
    drawImage(app.fruitImages[splat.color], splat.x, splat.y, width=imageWidth/2, height=imageHeight/2, align='center', opacity=splat.opacity)

def drawLives(app):
    x = app.width - 170
    y = 75
    imageWidth, imageHeight = getImageSize(app.guiImages[f'Strikes{app.strikes}'])
    drawImage(app.guiImages[f'Strikes{app.strikes}'], x, y, width=imageWidth*1.5, height=imageHeight*1.5, align='center')


# Function to update the game state
def onStep(app):
    if app.strikes >= 3:
        app.gameOver = True
        gameOver()

    app.elapsedTime += 1/app.stepsPerSecond
    app.spawnCounter += 1
    if app.spawnCounter >= app.fruitSpawnInterval:
        numFruits = getNumFruits(app.elapsedTime)
        for _ in range(numFruits):
            app.controller.createFruit()
        app.spawnCounter = 0 
        app.fruitSpawnInterval -= 10 # 10 is for demo purposes; ordinarily would've been 5.
        if app.fruitSpawnInterval < 50:
            app.fruitSpawnInterval = 50
    app.controller.updateFruits()
    if app.exploding:
        doExplosion(app)

def doExplosion(app):
    app.explosionOpacity += 4
    if app.explosionOpacity >= 100:
        app.explosionOpacity = 100
        app.gameOver = True
        gameOver()

def getNumFruits(elapsedTime):
    if elapsedTime < 5:
        return 1
    elif elapsedTime > 5:
        return randint(1, 2)
    elif elapsedTime > 20:
        return randint(1, 3)
    elif elapsedTime > 40:
        return randint(1, 4)

def onMouseMove(app, mouseX, mouseY):
    for fruit in app.store.getFruits():
        if distance(fruit.x, fruit.y, mouseX, mouseY)  <= fruit.radius:
            fruit.slice()
            app.score += 5
            break
    for bomb in app.store.getBombs():
        if distance(bomb.x, bomb.y, mouseX, mouseY)  <= bomb.radius:
            bomb.slice()
            break

def calculateProjectileMotion(x0, y0, vX, vY, gravity, time):
    x = x0 + vX * time
    y = y0 + vY * time + 0.5 * gravity * (time**2)
    return x, y

def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def gameOver():
    pass

# Start the game loop
def main():
    runApp()
main()