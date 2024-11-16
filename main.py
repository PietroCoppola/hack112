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
        gravity = 125/(0.8 * self.app.stepsPerSecond)
        self.time += 1/(self.app.stepsPerSecond)  # Increment time (adjust step size as needed)
        self.x, self.y = calculateProjectileMotion(self.x, self.y, self.vX, self.vY, gravity, self.time)

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
        vX = randint(-2, 2)
        vY = (-randint(200, 250))/(1.2 * self.app.stepsPerSecond)
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
    def adjustSpeed(self):
        fluctuation = uniform(0.95, 1.05)
        self.speedMultiplier *= fluctuation
        

        

# TODO write redrawAll function
def redrawAll(app):
    for fruit in app.store.getFruits():
        drawFruit(fruit)
    if app.gameOver:
        drawLabel("Game Over!", app.width / 2, app.height / 2, size=60, align='center')

def drawFruit(fruit):
    drawCircle(fruit.x, fruit.y, fruit.radius, fill=fruit.color)

def calculateProjectileMotion(x0, y0, vX, vY, gravity, time):
    x = x0 + vX * time
    y = y0 + vY * time + 0.5 * gravity * time**2
    return x, y

# Function to update the game state
def onStep(app):
    if app.strikes >= 3:
        app.gameOver = True
        return
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

def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

# Start the game loop
def main():
    runApp()
main()