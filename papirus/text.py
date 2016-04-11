import os
import sys

from PIL import Image, ImageDraw, ImageFont
from papirus import Papirus
import random

WHITE = 1
BLACK = 0

class PapirusText():

    def __init__(self):
        self.papirus = Papirus()

    def write(self, text, size = 20):
        
        # initially set all white background
        image = Image.new('1', self.papirus.size, WHITE)

        # prepare for drawing
        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', size)

        # Calculate the max number of char to fit on line
        line_size = (self.papirus.width / (size*0.65))

        current_line = 0
        text_lines = [""]

        # Compute each line
        for word in text.split():
            # If there is space on line add the word to it
            if (len(text_lines[current_line]) + len(word)) < line_size:
                text_lines[current_line] += " " + word
            else:
                # No space left on line so move to next one
                text_lines.append("")
                current_line += 1
                text_lines[current_line] += " " + word

        current_line = 0
        for l in text_lines:
            current_line += 1
            draw.text( (0, ((size*current_line)-size)) , l, font=font, fill=BLACK)

        self.papirus.display(image)
        self.papirus.update()
