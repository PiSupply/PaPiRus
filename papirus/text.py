import os
import sys

from PIL import Image, ImageDraw, ImageFont
from papirus import Papirus
import random

WHITE = 1
BLACK = 0

class PapirusText():

    def __init__(self, rotation = 0):
        self.papirus = Papirus(rotation = rotation)

    def write(self, text, size = 20, font_path='/usr/share/fonts/truetype/freefont/FreeMono.ttf'):
        
        # initially set all white background
        image = Image.new('1', self.papirus.size, WHITE)

        # prepare for drawing
        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype(font_path, size)

        # Calculate the max number of char to fit on line
        line_size = (self.papirus.width / (size*0.65))

        current_line = 0
        # unicode by default
        text_lines = [u""]

        # Compute each line
        for word in text.split():
            # Always add first word (even when it is too long)
            if len(text_lines[current_line]) == 0:
                text_lines[current_line] += word
            elif (draw.textsize(text_lines[current_line] + " " + word, font=font)[0]) < self.papirus.width:
                text_lines[current_line] += " " + word
            else:
                # No space left on line so move to next one
                text_lines.append(u"")
                current_line += 1
                text_lines[current_line] += " " + word

        current_line = 0
        for l in text_lines:
            draw.text( (0, size*current_line) , l, font=font, fill=BLACK)
            current_line += 1

        self.papirus.display(image)
        self.papirus.update()
