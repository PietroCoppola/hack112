from cmu_graphics import *
from random import randint, choice, uniform
import os

def onAppStart(app):
    app.width, app.height = 1280, 1024
    app.fruits = []
    app.slicedFruits = []
    app.store = FruitStore()
    app.controller = GameController(app)
    app.stepsPerSecond = 30
    app.score = 0
    app.gameOver = False
    app.strikes = 0
    app.spawnCounter = 0
    app.fruitSpawnInterval = 100
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
            rightSlicevX = self.vX * (1-speedDifference)
            leftSlicevX = self.vX * (speedDifference)
        else:
            rightSlicevX = self.vX * (speedDifference)
            leftSlicevX = self.vX * (1-speedDifference)
        rightSlice = SlicedFruit(self.app, self.x, self.y, rightSlicevX, self.vY, self.color, self.radius, self.time, 'Right')
        leftSlice = SlicedFruit(self.app, self.x, self.y, leftSlicevX, self.vY, self.color, self.radius, self.time, 'Left')
        self.app.store.addSlicedFruit(rightSlice)
        self.app.store.addSlicedFruit(leftSlice)

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
        
    
class FruitStore:
    def __init__(self):
        self.fruits = []
        self.slicedFruits = []

    def addFruit(self, fruit):
        self.fruits.append(fruit)

    def addSlicedFruit(self, slicedFruit):
        self.slicedFruits.append(slicedFruit)

    def removeFruit(self, fruit):
        self.fruits.remove(fruit)

    def removeSlicedFruit(self, slicedFruit):
        self.slicedFruits.remove(slicedFruit)

    def getFruits(self):
        return self.fruits
    
    def getSlicedFruits(self):
        return self.slicedFruits

# Controller
class GameController:
    def __init__(self, app):
        self.store = app.store
        self.app = app
        self.speedMultiplier = 1.0

    def createFruit(self):
        radius = 40
        x = randint(radius, self.app.width - radius)
        y = self.app.height + radius
        vX = uniform(1, 4)
        vY = (-randint(920, 972))/(self.app.stepsPerSecond)
        xCenter = self.app.width / 2
        vX *= (xCenter - x) / (self.app.width/2.5)
        color = choice(['Fruit1', 'Fruit2', 'Fruit3', 'Fruit4'])
        vY *= self.speedMultiplier
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
                
        
    # def adjustSpeed(self):
    #     fluctuation = uniform(0.95, 1.1)
    #     self.speedMultiplier *= fluctuation
    #     if self.speedMultiplier 

        

# TODO write redrawAll function
def redrawAll(app):
    for slicedFruit in app.store.getSlicedFruits():
        drawFruit(app, slicedFruit)
    for fruit in app.store.getFruits():
        drawFruit(app, fruit)
    drawLives(app)
    if app.gameOver:
        drawLabel("Game Over!", app.width / 2, app.height / 2, size=60, align='center')
    drawLabel(f'Score:{app.score}', 100, 50, size = 25)
    

def drawFruit(app, fruit):
    drawImage(app.fruitImages[fruit.color], fruit.x, fruit.y, align=fruit.alignment)

def drawLives(app):
    crossX = 1090
    crossY = 75
    drawImage(app.guiImages[f'Strikes{app.strikes}'], crossX, crossY, align='center')


# Function to update the game state
def onStep(app):
    if app.strikes >= 3:
        app.gameOver = True
        gameOver()
    # app.elapsedTime += 1 / app.stepsPerSecond
    # app.spawnInterval = max(50, 100 - int(app.elapsedTime * 1.5)) 
    # app.controller.updateFruits()

    app.spawnCounter += 1
    if app.spawnCounter >= app.fruitSpawnInterval:
        app.controller.createFruit()
        app.spawnCounter = 0 
    app.controller.updateFruits()
    # if randint(1, 100) <= max(10, 100 - app.elapsedTime * 2): 
    #     app.controller.createFruit()

def onMouseMove(app, mouseX, mouseY):
    for fruit in app.store.getFruits():
        if distance(fruit.x, fruit.y, mouseX, mouseY)  <= fruit.radius:
            fruit.slice()
            app.score += 5
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