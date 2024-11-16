from cmu_graphics import *
from random import randint, choice

def onAppStart(app):
    app.width, app.height = 600, 400
    app.fruits = []
    app.store = FruitStore()
    app.controller = GameController(app)

# Fruit Object 
class Fruit:
    def __init__(self, x, y, vX, vY, color, radius):
        self.x = x
        self.y = y
        self.vX = vX
        self.vY = vY
        self.entryPoint = y
        self.color = color
        self.Radius = radius

    def move(self):
        self.x += self.vX
        self.y += self.vY

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

    def createFruit(self):
        x = randint(fruitRadius, width - fruitRadius)
        y = height + fruitRadius
        vX = randint(-2, 2)
        vY = randint(-10, -5)
        color = choice(['red', 'green', 'yellow', 'orange'])
        fruit = Fruit(x, y, vX, vY, color)
        radius = randint()
        self.store.addFruit(fruit)

    def updateFruits(self):
        for fruit in self.store.getFruits()[:]:
            fruit.move()
            if fruit.y < - fruitRadius:
                self.store.removeFruit(fruit)

    def handleMousePress(self, mouseX, mouseY):
        for fruit in self.store.getFruits()[:]:
            if (fruit.x - mouseX) ** 2 + (fruit.y - mouseY) ** 2 <= FRUIT_RADIUS ** 2:
                self.store.removeFruit(fruit)
                break

controller = GameController(store)

# TODO write redrawAll function
def redrawAll(app):
    pass

def calculate_projectile_motion(x0, y0, vX, vY, ay, time):
    """
    Calculate the position of a projectile at a given time.
    :param x0: Initial x-coordinate of the projectile.
    :param y0: Initial y-coordinate of the projectile.
    :param vx: Initial velocity in the x-direction.
    :param vy: Initial velocity in the y-direction.
    :param ay: Constant acceleration in the y-direction (e.g., gravity).
    :param time: Time elapsed since the start of motion.
    :return: A tuple (x, y) representing the position of the projectile.
    """
    x = x0 + vX * time
    y = y0 + vY * time + 0.5 * ay * time**2
    return x, y

# Function to update the game state
def onStep():
    pass

# Function to handle mouse press
def onMousePress(mouseX, mouseY):
    pass

# Set up the event handlers
app.onStep = onStep
app.onMousePress = onMousePress

# Start the game loop
runApp()
