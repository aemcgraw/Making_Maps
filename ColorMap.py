from PIL import Image

from HeightMap import HeightMap

class ColorMap():
    def __init__(self, image, heightmap):
        self.image = image
        self.heightmap = heightmap
        self.mapping = heightmap.mapping
        self.scale = heightmap.scale

    def greyscale(self):
        pixels = self.image.load()

        for x in range(len(self.mapping)):
            for y in range(len(self.mapping[x])):
                val = self.mapping[x][y] + 1
                pixels[x, y] = ( int(127 * val),
                                 int(127 * val),
                                 int(127 * val),
                                 255 )

    def std(self):
        pixels = self.image.load()

        print(max([max(x) for x in self.mapping]))
        print("HI")
        for x in range(len(self.mapping)):
            for y in range(len(self.mapping[x])):
                val = self.mapping[x][y]
                if val < 0:
                    pixels[x, y] = (0, 0, 255, 255)
                elif val/self.scale > 1.0:
                    pixels[x, y] = (255, 0, 0, 255)
                elif val/self.scale > 0.7:
                    pixels[x, y] = (255, 255, 255, 255)
                elif val/self.scale > 0.3:
                    pixels[x, y] = (120, 120, 120, 255)
                else:
                    pixels[x, y] = (int(120 * val / self.scale),
                                        max(120, 255-int(135 * val / self.scale)),
                                        int(120 * val / self.scale), 255)

    def cosmic(self):
        pixels = self.image.load()

        print(max([max(x) for x in self.mapping]))
        print("COSMIC")
        for x in range(len(self.mapping)):
            for y in range(len(self.mapping[x])):
                val = self.mapping[x][y]
                if val/self.scale < 0:
                    pixels[x, y] = (0, 0, 0, 255)
                else:
                    pixels[x, y] = (0, 255, 0, 255)
