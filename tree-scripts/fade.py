from tree import RGBXmasTree
from colorzero import Color
from time import sleep
import random

colors = [Color('red'), Color('green'), Color('blue'), Color('yellow'), Color('magenta')]

tree = RGBXmasTree(brightness = 0.0)

def random_color():
    global colors
    return random.choice (colors)

tree.color = random_color ()

b = 0.0
step = 0.05

change_color = False
try:
    while True:
        b = b + step
        if (b <= 0):
            b = 0
            step = -step
            change_color = True
        elif (b >= 0.5):
            b = 0.5
            step = -step
        tree.brightness = b
        if change_color:
            tree.color = Color(random_color ())
            change_color = False
        sleep(0.1)
except KeyboardInterrupt:
    tree.close()
