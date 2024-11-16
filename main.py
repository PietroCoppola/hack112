from cmu_graphics import *
from random import randint, choice, uniform

def onAppStart(app):
    app.width, app.height = 600, 400
    app.fruits = []
    app.store = FruitStore()
    app.controller = GameController(app)
    app.stepsPerSecond = 30
    app.score = 0
    app.gameOver = False
    app.strikes = 0
    app.spawnCounter = 0
    app.fruitSpawnInterval = 100
    app.elapsedTime = 0


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

    def move(self):
        self.time += 1 / self.app.stepsPerSecond
        if self.time >= .5:
            gravity = 350 / self.app.stepsPerSecond
        else: # Create initial push
            gravity = -30 / (1+self.time)
        self.x, self.y, = calculateProjectileMotion(self.x, self.y, self.vX, self.vY, gravity, self.time)
# Store
class FruitStore:
    def __init__(self):
        self.fruits = []

    def addFruit(self, fruit):
        self.fruits.append(fruit)

    def removeFruit(self, fruit):
        self.fruits.remove(fruit)

    def getFruits(self):
        return self.fruits

# Controller
class GameController:
    def __init__(self, app):
        self.store = app.store
        self.app = app
        self.speedMultiplier = 1.0

    def createFruit(self):
        radius = 30
        x = randint(radius, self.app.width - radius)
        y = self.app.height + radius
        vX = uniform(0.5, 2)
        vY = (-randint(360, 380))/(self.app.stepsPerSecond)
        xCenter = self.app.width / 2
        vX *= (xCenter - x) / (self.app.width/2.5)
        color = choice(['red', 'green', 'yellow', 'orange'])
        vY *= self.speedMultiplier
        fruit = Fruit(self.app, x, y, vX, vY, color, radius)
        self.store.addFruit(fruit)

    def updateFruits(self):
        for fruit in self.store.getFruits()[:]:
            fruit.move()
            if (fruit.y - fruit.radius > self.app.height or  
            fruit.x + fruit.radius < 0 or        
            fruit.x - fruit.radius > self.app.width): 
                self.store.removeFruit(fruit)
    # def adjustSpeed(self):
    #     fluctuation = uniform(0.95, 1.1)
    #     self.speedMultiplier *= fluctuation
    #     if self.speedMultiplier 

        

# TODO write redrawAll function
def redrawAll(app):
    for fruit in app.store.getFruits():
        drawFruit(fruit)
    if app.gameOver:
        drawLabel("Game Over!", app.width / 2, app.height / 2, size=60, align='center')

def drawFruit(fruit):
    drawCircle(fruit.x, fruit.y, fruit.radius, fill=fruit.color)

# def drawLives(app):
#     crossX = 20
#     crossY = 
#     for i in range(3):
#         if i < app.strikes:
#             drawRedCross()
#         else:
#             drawHollowCross()

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
            app.store.removeFruit(fruit)
            app.score += 1
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