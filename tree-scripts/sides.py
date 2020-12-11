from tree2 import RGBXmasTree
from colorzero import Color, Hue
from time import sleep

colors = list (Color('red').gradient(Color('blue'), 9))
c_index = 0
s_index = 0
br = 0.5
br_step = -0.1

tree = RGBXmasTree(brightness = br)

try:
    tree.star.color = Color('white')
    while True:
        tree.star.brightness = br
        tree.sides[s_index].color = colors[c_index]
        s_index = (s_index + 1) % len(tree.sides)
        c_index = (c_index + 1) % len(colors)
        br += br_step
        if br <= 0.1:
            br = 0.1
            br_step = -1.0 * br_step
        elif br >= 0.5:
            br = 0.5
            br_step = -1.0 * br_step
        sleep (0.1)
except KeyboardInterrupt:
    tree.close()
