import os
import sys

from PIL import Image
from PIL import ImageOps
from papirus import Papirus

class PapirusImage():

    def __init__():
        self.papirus = Papirus()

    def write(self, image):
        image = Image.open(image)
        image = ImageOps.grayscale(image)

        # crop to the middle
        w,h = image.size
        x = w / 2 - epd.width / 2
        y = h / 2 - epd.height / 2

        rs = image.resize((epd.width, epd.height))
        bw = rs.convert("1", dither=Image.FLOYDSTEINBERG)

        epd.display(bw)
        epd.update()
