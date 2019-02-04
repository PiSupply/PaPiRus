from __future__ import division

import os
import sys

from PIL import Image
from papirus import Papirus

WHITE = 1

class PapirusImage(object):

    def __init__(self, rotation=0):
        self.papirus = Papirus(rotation=rotation)

    def write(self, imagefile):
        fileimg = Image.open(imagefile)

        w,h = fileimg.size

        rsimg = fileimg
        if w > self.papirus.width or h > self.papirus.height:
            rsimg.thumbnail(self.papirus.size)

        xpadding = (self.papirus.width  - rsimg.size[0]) // 2
        ypadding = (self.papirus.height - rsimg.size[1]) // 2

        image = Image.new('1', self.papirus.size, WHITE)
        image.paste(rsimg, (xpadding, ypadding))

        self.papirus.display(image)
        self.papirus.update()

