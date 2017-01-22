import os
import sys

from PIL import Image
from PIL import ImageOps
from papirus import Papirus

class PapirusImage():

    def __init__(self):
        self.papirus = Papirus()

    def write(self, image):
        image = Image.open(image)
        image = ImageOps.grayscale(image)

        # crop to the middle
        w,h = image.size
        x = w / 2 - self.papirus.width / 2
        y = h / 2 - self.papirus.height / 2

        rs = image
        if w != self.papirus.width or h != self.papirus.height:
            rs = image.resize((self.papirus.width, self.papirus.height))
        bw = rs.convert("1", dither=Image.FLOYDSTEINBERG)

        self.papirus.display(bw)
        self.papirus.update()
