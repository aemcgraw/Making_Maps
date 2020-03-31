from PIL import Image

from app.components.Region import Region

class Water(Region):
    def __init__(self, image, bound=None):
        super().__init__(image, bound=bound)

    def color(self):
        pixels = self.image.load()
        for (x, y) in self.interior:
            pixels[x, y] = (0, 0, 255, 255)

    def outline(self):
        pixels = self.image.load()
        for (x, y) in self.interior:
            pixels[x, y] = (255, 255, 255, 255)
