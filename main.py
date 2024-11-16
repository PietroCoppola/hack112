from cmu_graphics import *
from random import randint, choice

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

# Fruit Object 
class Fruit:
    def __init__(self, x, y, vX, vY, color, radius):
        self.x = x
        self.y = y
        self.vX = vX
        self.vY = vY
        self.entryPoint = (x,y)
        self.color = color
        self.radius = radius
        self.time = 0

    def move(self):
        ay = 9.8  
        self.time += 1/(app.stepsPerSecond)  # Increment time (adjust step size as needed)
        self.x, self.y = calculate_projectile_motion(self.x, self.y, self.vX, self.vY, ay, self.time)

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

    def createFruit(self):
        radius = 10
        x = randint(radius, self.app.width - radius)
        y = self.app.height + radius
        #vX = randint(-2, 2)
        vY = randint(-10, -5)
        color = choice(['red', 'green', 'yellow', 'orange'])

        fruit = Fruit(x, y, vX, vY, color, radius)
        self.store.addFruit(fruit)

    def updateFruits(self):
        for fruit in self.store.getFruits()[:]:
            fruit.move()
            if (fruit.y - fruit.radius > self.app.height or  
            fruit.x + fruit.radius < 0 or        
            fruit.x - fruit.radius > self.app.width): 
                self.store.removeFruit(fruit)

# TODO write redrawAll function
def redrawAll(app):
    for fruit in app.store.getFruits():
        drawFruit(fruit)
    if app.gameOver:
        drawLabel("Game Over!", app.width / 2, app.height / 2, size=60, align='center')

def drawFruit(fruit):
    drawCircle(fruit.x, fruit.y, fruit.radius, fill=fruit.color)

def calculate_projectile_motion(x0, y0, vX, vY, ay, time):
    x = x0 + vX * time
    y = y0 + vY * time + 0.5 * ay * time**2
    return x, y

# Function to update the game state
def onStep(app):
    if app.strikes >= 3:
        app.gameOver = True
        return
    if randint(1, 5) == 1:  
        app.controller.createFruit()
    app.controller.updateFruits()

    app.spawnCounter += 1
    if app.spawnCounter >= app.spawnInterval:
        app.controller.createFruit()
        app.spawnCounter = 0  # Reset the counter after spawning a fruit

# Function to handle mouse movements
def onMouseMove(app, mouseX, mouseY):
    for fruit in app.store.getFruits():
        if distance(fruit.x, fruit.y, mouseX, mouseY)  <= fruit.radius ** 2:
            app.store.removeFruit(fruit)
            app.score += 1
            break

def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

# Start the game loop
def main():
    runApp()
main()