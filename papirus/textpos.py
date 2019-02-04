import os
import sys

from PIL import Image, ImageDraw, ImageFont
from papirus import Papirus
import uuid

WHITE = 1
BLACK = 0

# Class for holding the details of the text
class DispText(object):
    def __init__(self, text, x, y, size, invert):
        self.text = text
        self.x = x
        self.y = y
        self.size = size
        self.endx = 0
        self.endy = 0
        self.invert = invert

class PapirusTextPos(object):
    def __init__(self, autoUpdate=True, rotation=0):
        # Set up the PaPirus and dictionary for text
        self.papirus = Papirus(rotation=rotation)
        self.allText = dict()
        self.image = Image.new('1', self.papirus.size, WHITE)
        self.autoUpdate = autoUpdate
        self.partialUpdates = False

    def AddText(self, text, x=0, y=0, size=20, Id=None, invert=False, fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf', maxLines=100):
        # Create a new Id if none is supplied
        if Id is None:
            Id = str(uuid.uuid4())

        # If the Id doesn't exist, add it  to the dictionary
        if Id not in self.allText:
            self.allText[Id] = DispText(text, x, y, size, invert)
            # add the text to the image
            self.addToImageText(Id, fontPath, maxLines)
            #Automatically show?
            if self.autoUpdate:
                self.WriteAll()

    def UpdateText(self, Id, newText, fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf', maxLines=100):
        # If the ID supplied is in the dictionary, update the text
        # Currently ONLY the text is update
        if Id in self.allText:
            self.allText[Id].text = newText

            # Remove from the old text from the image (that doesn't use the actual text)
            self.removeImageText(Id)
            # Add the new text to the image
            self.addToImageText(Id, fontPath, maxLines)
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


    def addToImageText(self, Id, fontPath='/usr/share/fonts/truetype/freefont/FreeMono.ttf', maxLines=100):
        # Break the text item back in to parts
        size = self.allText[Id].size
        x =  self.allText[Id].x
        y =  self.allText[Id].y
        fontColor = BLACK
        backgroundColor = WHITE

        if self.allText[Id].invert:
            fontColor = WHITE
            backgroundColor = BLACK

        # prepare for drawing
        draw = ImageDraw.Draw(self.image)

        # Grab the font to use, fixed at the moment
        font = ImageFont.truetype(fontPath, size)

        # Calculate the max number of char to fit on line
        # Taking in to account the X starting position
        lineWidth = self.papirus.width - x

        # Starting vars
        currentLine = 0
        # Unicode by default
        textLines = [u""]

        # Split the text by \n first
        toProcess = self.allText[Id].text.splitlines()

        # Go through the lines and add them
        for line in toProcess:
            # Add in a line to add the words to
            textLines.append(u"")
            currentLine += 1
            # Compute each line
            for word in line.split():
                # Always add first word (even it is too long)
                if len(textLines[currentLine]) == 0:
                    textLines[currentLine] += word
                elif (draw.textsize(textLines[currentLine] + " " + word, font=font)[0]) < lineWidth:
                    textLines[currentLine] += " " + word
                else:
                    # No space left on line so move to next one
                    textLines.append(u"")
                    if currentLine < maxLines:
                        currentLine += 1
                        textLines[currentLine] += word

        # Remove the first empty line
        if len(textLines) > 1:
            del textLines[0]

        # Go through all the lines as needed, drawing them on to the image

        # Reset the ending position of the text
        self.allText[Id].endy = y
        self.allText[Id].endx = x

        # Start at the beginning, calc all the end locations
        currentLine = 0
        for l in textLines:
            # Find out the size of the line to be drawn
            textSize = draw.textsize(l, font=font)
            # Adjust the x end point if needed
            if textSize[0]+x > self.allText[Id].endx:
                self.allText[Id].endx = textSize[0] + x
            # Add on the y end point
            self.allText[Id].endy += size
            # If next line does not fit, quit
            currentLine += 1
            if self.allText[Id].endy > (self.papirus.height - size - 3):
                del textLines[currentLine:]
                break

        # Little adjustment to make sure the text gets covered
        self.allText[Id].endy += 3

        # If the text is wanted inverted, put a rectangle down first
        if self.allText[Id].invert:
            draw.rectangle([self.allText[Id].x, self.allText[Id].y, self.allText[Id].endx, self.allText[Id].endy], fill=backgroundColor)

        # Start at the beginning, add all the lines to the image
        currentLine = 0
        for l in textLines:
            # Draw the text to the image
            yline = y + size*currentLine
            draw.text( (x, yline), l, font=font, fill=fontColor)
            currentLine += 1

    def WriteAll(self, partialUpdate=False):
        # Push the image to the PaPiRus device, and update only what's needed
        # (unless asked to do a full update)
        self.papirus.display(self.image)
        if partialUpdate or self.partialUpdates:
            self.papirus.partial_update()
        else:
            self.papirus.update()

    def Clear(self):
        # Clear the image, clear the text items, do a full update to the screen
        self.image = Image.new('1', self.papirus.size, WHITE)
        self.allText = dict()
        self.papirus.clear()

