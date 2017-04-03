import os
import sys

from PIL import Image
from PIL import ImageOps
from papirus import Papirus
from papirus import PapirusTextPos

WHITE = 1
BLACK = 0

# Class for holding the details of the text
class DispImg():
    def __init__(self, image, x, y, size):
        self.image = image
        self.x = x
        self.y = y
        self.size = size
        self.endx = 0
        self.endy = 0

class PapirusComposite (PapirusTextPos):

    def __init__(self, autoUpdate = True):
        super(PapirusComposite, self).__init__(autoUpdate)
        self.papirus = Papirus()
        self.allImg = dict()
        self.image = Image.new('1', self.papirus.size, WHITE)

    def AddImage(self, image, x=0, y=0, size = (10,10), Id = None):
        # Create a new Id if none is supplied
        if Id == None:
            Id = str(uuid.uuid4())

        image = Image.open(image)
        image = ImageOps.grayscale(image)
        image = image.resize(size)
        image = image.convert("1", dither=Image.FLOYDSTEINBERG)

        # If the Id doesn't exist, add it  to the dictionary
        if Id not in self.allImg:
            self.allImg[Id] = DispImg(image, x, y, size)
            # add the text to the image
            self.addToImageImage(Id)
            #Automatically show?
            if self.autoUpdate:
                self.WriteAll()

    def UpdateImg(self, Id, image):
        # If the ID supplied is in the dictionary, update the text
        # Currently ONLY the text is update
        if Id in self.allImg:
            image = Image.open(image)
            image = ImageOps.grayscale(image)
            image = image.resize(self.allImg[Id].size)
            image = image.convert("1", dither=Image.FLOYDSTEINBERG)

            self.allImg[Id].image = image
            
            # Remove from the old text from the image (that doesn't use the actual text)
            self.removeImageImage(Id)
            # Add the new text to the image
            self.addToImageImage(Id)
            #Automatically show?
            if self.autoUpdate:
                self.WriteAll()

    def RemoveImg(self, Id):
        # If the ID supplied is in the dictionary, remove it.
        if Id in self.allImg:
            self.removeImageImage(Id)
            del self.allImg[Id]

            #Automatically show?
            if self.autoUpdate:
                self.WriteAll()

    def removeImageImage(self, Id):
        # prepare for drawing
        filler = Image.new('1', self.allImg[Id].size, WHITE)
        # Draw over the top of the text with a rectangle to cover it
        x =  self.allImg[Id].x
        y =  self.allImg[Id].y
        self.image.paste(filler,(x,y))

    def addToImageImage(self, Id):
        x =  self.allImg[Id].x
        y =  self.allImg[Id].y

        self.image.paste(self.allImg[Id].image,(x,y))