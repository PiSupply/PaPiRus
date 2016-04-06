import os
import sys
import re

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from papirus import Papirus
import random

WHITE = 1
BLACK = 0

class PapirusText(Papirus):

    def __init__(self):
        Papirus.__init__(self)
        #self.papirus = Papirus()

    def write(self, text, size = 20):

        # initially set all white background
        image = Image.new('1', self.size, WHITE)

        # prepare for drawing
        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', size)

        # Calculate the max number of char to fit on line
        line_size = (self.width / (size*0.65))

        current_line = 0
        for l in re.split(r'[\r\n]+', text):
            current_line += 1
            draw.text( (0, ((size*current_line)-size)) , l, font=font, fill=BLACK)

        self.display(image)
        self.update()


