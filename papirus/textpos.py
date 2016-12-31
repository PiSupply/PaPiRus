import os
import sys

from PIL import Image, ImageDraw, ImageFont
from papirus import Papirus
import uuid


WHITE = 1
BLACK = 0

class PapirusTextPos():

    def __init__(self):
        # Set up the PaPirus and dictionary for text
        self.papirus = Papirus()
        self.allText = dict()

    def AddText(self, text, x=0, y=0, size = 20, Id = None):
        # Create a new Id if none is supplied
        if Id == None:
            Id = str(uuid.uuid4())

        # If the Id doesn't exist, add it as a 4 part Tuple to the dictionary
	if Id not in self.allText:
            self.allText[Id] = (text, x, y, size)

    def UpdateText(self, Id, newText):
        # If the ID supplied is in the dictionary, update the text
        # Currently ONLY the text is update
        if Id in self.allText:
            item = self.allText[Id]
            self.allText[Id] = (newText, item[1], item[2], item[3])

    def addToImageText(self, image, item):
        # Break the text item back in to parts
        size = item[3]
        x = item[1]
        y = item[2]

        # prepare for drawing
        draw = ImageDraw.Draw(image)

        # Grab the font to use, fixed at the moment
        font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', size)

        # Calculate the max number of char to fit on line
        # Taking in to account the X starting position
        line_size = ((self.papirus.width - x) / (size*0.65))

        # Starting vars
        current_line = 0
        text_lines = [""]

        # Compute each line
        for word in item[0].split():
            # If there is space on line add the word to it
            if (len(text_lines[current_line]) + len(word)) < line_size:
                text_lines[current_line] += " " + word
            else:
                # No space left on line so move to next one
                text_lines.append("")
                current_line += 1
                text_lines[current_line] += " " + word

        #  Go through all the lines as needed, drawing them on to the image
        current_line = 0
        for l in text_lines:
            current_line += 1
            draw.text( (x, ((size*current_line)-size) + y) , l, font=font, fill=BLACK)

    def WriteAll(self):
        image = Image.new('1', self.papirus.size, WHITE)

        for key in self.allText:
            self.addToImageText(image, self.allText[key])

        self.papirus.display(image)
        self.papirus.update()
