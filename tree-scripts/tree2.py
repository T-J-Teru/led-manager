from gpiozero import SPIDevice, SourceMixin
from colorzero import Color, Hue
from statistics import mean
from time import sleep

class Pixel:
    def __init__(self, parent, index):
        self.parent = parent
        self.index = index

    @property
    def brightness(self):
        br, r, g, b = self.parent.value[self.index]
        return br

    @brightness.setter
    def brightness(self, br):       
        old_br, r, g, b = self.value
        self.value = (br, r, g, b)

    @property
    def value(self):
        return self.parent.value[self.index]

    @value.setter
    def value(self, value):
        new_parent_value = list(self.parent.value)
        new_parent_value[self.index] = value
        self.parent.value = tuple(new_parent_value)

    @property
    def color(self):
        br, r, g, b = self.value
        return Color(r, g, b)

    @color.setter
    def color(self, c):
        r, g, b = c
        br = self.brightness
        self.value = (br, r, g, b)

    def on(self):
        self.color = Color (1, 1, 1)

    def off(self):
        self.color = Color (0, 0, 0)

class PixelGroup:
    def __init__(self, parent, indices):
        self.parent = parent
        self.indices = indices

    @property
    def brightness(self):
        return mean(self.parent.value[i][0] for i in self.indices)

    @brightness.setter
    def brightness(self, br):
        new_parent_value = list(self.parent.value)
        for i in self.indices:
            new_parent_value[i][0] = br
        self.parent.value = tuple(new_parent_value)

    @property
    def color(self):
        for i in self.indices:
            average_r = mean(self.parent[i].color[0])
            average_g = mean(self.parent[i].color[1])
            average_b = mean(self.parent[i].color[2])
        return Color(average_r, average_g, average_b)

    @color.setter
    def color(self, c):
        new_parent_value = list(self.parent.value)
        r, g, b = c
        for i in self.indices:
            new_parent_value[i][1] = r
            new_parent_value[i][2] = g
            new_parent_value[i][3] = b
        self.parent.value = tuple(new_parent_value)

    def on(self):
        self.color = Color (1, 1, 1)

    def off(self):
        self.color = Color (0, 0, 0)

class RGBXmasTree(SourceMixin, SPIDevice):
    def __init__(self, pixels=25, brightness=0.5, mosi_pin=12, clock_pin=25, *args, **kwargs):
        super(RGBXmasTree, self).__init__(mosi_pin=mosi_pin, clock_pin=clock_pin, *args, **kwargs)
        self._all = [Pixel(parent=self, index=i) for i in range(pixels)]
        self._value = [(brightness, 0, 0, 0)] * pixels
        self._sides = []
        self._sides.append (PixelGroup(parent=self, indices=[0, 1, 2]))
        self._sides.append (PixelGroup(parent=self, indices=[16, 17, 18]))
        self._sides.append (PixelGroup(parent=self, indices=[15, 14, 13]))
        self._sides.append (PixelGroup(parent=self, indices=[6, 5, 4]))
        self._sides.append (PixelGroup(parent=self, indices=[12, 11, 10]))
        self._sides.append (PixelGroup(parent=self, indices=[24, 23, 22]))
        self._sides.append (PixelGroup(parent=self, indices=[19, 20, 21]))
        self._sides.append (PixelGroup(parent=self, indices=[7, 8, 9]))
        self._layers = []
        self._layers.append (PixelGroup(parent=self, indices=[3]))
        self._layers.append (PixelGroup(parent=self, indices=[2, 18, 13, 4, 10, 22, 21, 9]))
        self._layers.append (PixelGroup(parent=self, indices=[1, 17, 14, 5, 11, 23, 20, 8]))
        self._layers.append (PixelGroup(parent=self, indices=[0, 16, 15, 6, 12, 24, 19, 7]))
        self.off()

    def __len__(self):
        return len(self._all)

    def __getitem__(self, index):
        return self._all[index]

    def __iter__(self):
        return iter(self._all)

    @property
    def color(self):
        average_r = mean(pixel.color[0] for pixel in self)
        average_g = mean(pixel.color[1] for pixel in self)
        average_b = mean(pixel.color[2] for pixel in self)
        return Color(average_r, average_g, average_b)

    @color.setter
    def color(self, c):
        r, g, b = c
        old_value = self.value
        new_value = []
        for p in old_value:
            br, old_r, old_g, old_b = p
            new_value.append ([br, r, g, b])
        self.value = new_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        start_of_frame = [0]*4
        end_of_frame = [0]*5

        pixel_data = []
        for p in value:
            br, r, g, b = p
            br = 0b11100000 | int (br * 31)
            r = int (255 * r)
            g = int (255 * g)
            b = int (255 * b)           
            pixel_data.append ([br, b, g, r])
        pixel_data = [i for p in pixel_data for i in p]

        data = start_of_frame + pixel_data + end_of_frame
        self._spi.transfer(data)
        self._value = value

    def on(self):
        self.color = Color (1, 1, 1)

    def off(self):
        self.color = Color (0, 0, 0)

    def close(self):
        super(RGBXmasTree, self).close()

    @property
    def sides(self):
        return self._sides

    @property
    def layers(self):
        return self._layers

    @property
    def star(self):
        return self[3]

if __name__ == '__main__':
    tree = RGBXmasTree()

    tree.layers[0].on ()
    sleep (1)
    tree.layers[0].off ()
    tree.layers[1].on ()
    sleep (1)
    tree.layers[1].off ()
    tree.layers[2].on ()
    sleep (1)
    tree.layers[2].off ()
    tree.layers[3].on ()
    sleep (1)
    tree.off ()
    sleep (1)
    tree.on()
    sleep (1)
    tree.off ()
    sleep (1)
    tree.sides[0].color = Color ('red')
    sleep (1)
    tree.off ()
