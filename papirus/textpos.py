import os
import sys

from PIL import Image, ImageDraw, ImageFont
from papirus import Papirus
import uuid


WHITE = 1
BLACK = 0

# Class for holding the details of the text
class DispText():
    def __init__(self, text, x, y, size):
        self.text = text
        self.x = x
        self.y = y
        self.size = size
        self.endx = 0
        self.endy = 0

class PapirusTextPos(object):
    def __init__(self, autoUpdate = True, rotation = 0):
        # Set up the PaPirus and dictionary for text
        self.papirus = Papirus(rotation = rotation)
        self.allText = dict()
        self.image = Image.new('1', self.papirus.size, WHITE)
        self.autoUpdate = autoUpdate

    def AddText(self, text, x=0, y=0, size = 20, Id = None, font_path='/usr/share/fonts/truetype/freefont/FreeMono.ttf'):
        # Create a new Id if none is supplied
        if Id == None:
            Id = str(uuid.uuid4())

        # If the Id doesn't exist, add it  to the dictionary
	if Id not in self.allText:
            self.allText[Id] = DispText(text, x, y, size)
            # add the text to the image
            self.addToImageText(Id, font_path)
            #Automatically show?
            if self.autoUpdate:
                self.WriteAll()

    def UpdateText(self, Id, newText, font_path='/usr/share/fonts/truetype/freefont/FreeMono.ttf'):
        # If the ID supplied is in the dictionary, update the text
        # Currently ONLY the text is update
        if Id in self.allText:
            self.allText[Id].text = newText

            # Remove from the old text from the image (that doesn't use the actual text)
            self.removeImageText(Id)
            # Add the new text to the image
            self.addToImageText(Id, font_path)
            #Automatically show?
            if self.autoUpdate:
                self.WriteAll()

    def RemoveText(self, Id):
        # If the ID supplied is in the dictionary, remove it.
        if Id in self.allText:
            self.removeImageText(Id)
            del self.allText[Id]

            #Automatically show?
            if self.autoUpdate:
                self.WriteAll()

    def removeImageText(self, Id):
        # prepare for drawing
        draw = ImageDraw.Draw(self.image)
        # Draw over the top of the text with a rectangle to cover it
        draw.rectangle([self.allText[Id].x, self.allText[Id].y, self.allText[Id].endx, self.allText[Id].endy], fill="white")


    def addToImageText(self, Id, font_path='/usr/share/fonts/truetype/freefont/FreeMono.ttf'):
        # Break the text item back in to parts
        size = self.allText[Id].size
        x =  self.allText[Id].x
        y =  self.allText[Id].y

        # prepare for drawing
        draw = ImageDraw.Draw(self.image)

        # Grab the font to use, fixed at the moment
        font = ImageFont.truetype(font_path, size)

        # Calculate the max number of char to fit on line
        # Taking in to account the X starting position
        line_size = ((self.papirus.width - x) / (size*0.65))

        # Starting vars
        current_line = 0
        # unicode by default
        text_lines = [u""]

        # Split the text by \n first
        toProcess = self.allText[Id].text.splitlines()

        # Go through the lines and add them
        for line in toProcess:
            # Add in a line to add the words to
            text_lines.append("")
            # Compute each line
            for word in line.split():
                # If there is space on line add the word to it
                if (len(text_lines[current_line]) + len(word)) < line_size:
                    text_lines[current_line] += " " + word
                else:
                    # No space left on line so move to next one
                    text_lines.append("")
                    current_line += 1
                    text_lines[current_line] += " " + word
            # Move the pointer to next line
            current_line +=1

        #  Go through all the lines as needed, drawing them on to the image

        # Reset the ending position of the text
        self.allText[Id].endy = y
        self.allText[Id].endx = x

        # Start at the beginning
        current_line = 0
        for l in text_lines:
            current_line += 1
            # Find out the size of the line to be drawn
            textSize = draw.textsize(l, font=font)
            # Adjust the x end point if needed
            if textSize[0]+x> self.allText[Id].endx:
                self.allText[Id].endx = textSize[0] + x
            # Add on the y end point
            self.allText[Id].endy += textSize[1]
            # Draw the text to the image
            draw.text( (x, ((size*current_line)-size) + y) , l, font=font, fill=BLACK)

        # Little adjustment to make sure the text gets covered
        self.allText[Id].endy += 3

    def WriteAll(self):
        # Push the image to the PaPiRus device, and update only what's needed
        self.papirus.display(self.image)
        self.papirus.update()

    def Clear(self):
        # Clear the image, clear the text items, do a full update to the screen
        self.image = Image.new('1', self.papirus.size, WHITE)
        self.allText = dict()
        self.papirus.display(self.image)
        self.papirus.update()
