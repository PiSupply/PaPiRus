import os
import sys

from PIL import Image, ImageDraw, ImageFont
from papirus import Papirus
import random

WHITE = 1
BLACK = 0

class PapirusText(object):

    def __init__(self, rotation=0):
        self.papirus = Papirus(rotation=rotation)

    def write(self, text, size=20, fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf', maxLines=100):
        
        # initially set all white background
        image = Image.new('1', self.papirus.size, WHITE)

        # prepare for drawing
        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype(fontPath, size)

        # Calculate the max number of char to fit on line
        lineSize = (self.papirus.width / (size*0.65))

        currentLine = 0
        # unicode by default
        textLines = [u""]

        # Compute each line
        for word in text.split():
            # Always add first word (even when it is too long)
            if len(textLines[currentLine]) == 0:
                textLines[currentLine] += word
            elif (draw.textsize(textLines[currentLine] + " " + word, font=font)[0]) < self.papirus.width:
                textLines[currentLine] += " " + word
            else:
                # No space left on line so move to next one
                textLines.append(u"")
                if currentLine < maxLines:
                    currentLine += 1
                    textLines[currentLine] += word

        currentLine = 0
        for l in textLines:
            draw.text( (0, size*currentLine) , l, font=font, fill=BLACK)
            currentLine += 1

        self.papirus.display(image)
        self.papirus.update()

