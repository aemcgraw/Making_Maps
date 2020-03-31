from PIL import Image

from random import randint

from app.components.Region import Region

class rIsland(Region):
    def __init__(self, image, bound=None):
        super().__init__(image, bound=bound)

    def color(self):
        pixels = self.image.load()
        for (x, y) in self.interior:
            pixels[x, y] = (0, 255, 0, 255)
