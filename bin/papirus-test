#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Quick & Dirty hack PaPiRus test script.
# Mostly cut and paste from https://github.com/repaper/gratis demos
# and https://github.com/Percheron-Electronics/gratis 
# LM75 stuff taken from https://github.com/glitch003/LM75
# Russell "UKScone" Davis 06/02/16

import time
import sys
import os
import random
import subprocess
import smbus
import Image
import ImageOps
import ImageDraw
import ImageFont

from papirus import Papirus 

LM75_ADDRESS             = 0x48

LM75_TEMP_REGISTER       = 0
LM75_CONF_REGISTER       = 1
LM75_THYST_REGISTER      = 2
LM75_TOS_REGISTER        = 3

LM75_CONF_SHUTDOWN       = 0
LM75_CONF_OS_COMP_INT    = 1
LM75_CONF_OS_POL         = 2
LM75_CONF_OS_F_QUE       = 3


class LM75(object):
        def __init__(self, mode=LM75_CONF_OS_COMP_INT, address=LM75_ADDRESS,
                                                         busnum=1):
                self._mode = mode
                self._address = address
                self._bus = smbus.SMBus(busnum)

        def regdata2float (self, regdata):
                return (regdata / 32.0) / 8.0
        def toFah(self, temp):
                return (temp * (9.0/5.0)) + 32.0

        def getTemp(self):
                raw = self._bus.read_word_data(self._address, LM75_TEMP_REGISTER) & 0xFFFF
                #print "raw: "
                #print raw
                raw = ((raw << 8) & 0xFF00) + (raw >> 8)
                return self.toFah(self.regdata2float(raw))



vendor  = subprocess.check_output(["cat", "/proc/device-tree/hat/vendor"])
product = subprocess.check_output(["cat", "/proc/device-tree/hat/product"])
serial  = subprocess.check_output(["cat", "/proc/device-tree/hat/uuid"])

WHITE = 1
BLACK = 0

FONT_FILE = '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf'

TEXT_FONT_SIZE1 = 11
TEXT_FONT_SIZE2 = 16
TEXT_FONT_SIZE3 = 36
panel =''
def main(argv):
    """main program - display logo, report product details
    print 'Number of arguments:', len(sys.argv)
    print 'Argument List:', str(sys.argv)"""
    papirus = Papirus()
    papirus.clear()
    
    print (vendor)
    print (product)
    print (serial)
   
    
    global panel 
    panel = '{p:s} {w:d} x {h:d} version={v:s} COG={g:d} FILM={f:d}'.format(p=papirus.panel, w=papirus.width, h=papirus.height, v=papirus.version, g=papirus.cog, f=papirus.film)  
    print "panel = ",panel

    for file_name in argv:
        if not os.path.exists(file_name):
            sys.exit('error: image file{f:s} does not exist'.format(f=file_name))
        print('display: {f:s}'.format(f=file_name))
        display_file(papirus, file_name)
        display_demo(papirus)
        print ('Now some text')
        display_partial(papirus)
        display_papirusdata(papirus)
 	            




def display_papirusdata(papirus):
    w = papirus.width
    h = papirus.height
    sensor = LM75()

    text_font1 = ImageFont.truetype(FONT_FILE, TEXT_FONT_SIZE1)
    text_font2 = ImageFont.truetype(FONT_FILE, TEXT_FONT_SIZE2)
    text_font3 = ImageFont.truetype(FONT_FILE, TEXT_FONT_SIZE3)

    # initially set all white background
    image = Image.new('1', papirus.size, WHITE)

    # prepare for drawing
    draw = ImageDraw.Draw(image)
    draw.rectangle((1, 1, w - 1, h - 1), fill=WHITE, outline=BLACK)
    draw.rectangle((2, 2, w - 2, h - 2), fill=WHITE, outline=BLACK)
    # text
    draw.text((38,3), vendor[:-1], fill=BLACK, font=text_font3)
    draw.text((15,40), product[:-1], fill=BLACK, font=text_font2)
    draw.text((45,70), panel[0:17], fill=BLACK, font=text_font2)
    draw.text((4,90),panel[17:], fill=BLACK, font=text_font2)
    draw.text((45,120),"Temperature"+str(sensor.getTemp())+"°F".decode('utf-8'), fill=BLACK, font=text_font2)

    draw.text((5,160), serial[:-1], fill=BLACK, font=text_font1)
   
    print (panel)
    # display image on the panel
    papirus.display(image)
    papirus.update()

def display_demo(papirus):
    """simple drawing demo - black drawing on white background"""

    # initially set all white background
    image = Image.new('1', papirus.size, WHITE)

    # prepare for drawing
    draw = ImageDraw.Draw(image)

    # three pixels in top left corner
    draw.point((0, 0), fill=BLACK)
    draw.point((1, 0), fill=BLACK)
    draw.point((0, 1), fill=BLACK)

    # lines
    draw.line([(10,20),(100,20)], fill=BLACK)
    draw.line([(10,90),(100,60)], fill=BLACK)

    # filled circle, elipse
    draw.ellipse((120, 10, 150, 40), fill=BLACK, outline=BLACK)
    draw.ellipse((120, 60, 170, 90), fill=WHITE, outline=BLACK)

    # text
    draw.text((30, 30), 'hello world', fill=BLACK)

    # display image on the panel
    papirus.display(image)
    papirus.update()
    time.sleep(3) # delay in seconds

def display_partial(papirus):
    """simple partial update demo - draw random shapes"""

    # initially set all white background
    image = Image.new('1', papirus.size, WHITE)

    # prepare for drawing
    draw = ImageDraw.Draw(image)
    width, height = image.size

    # repeat for number of frames
    for i in range(0, 50):
        for j in range(0, 5):
            if random.randint(0, 1):
                fill = WHITE
                outline = BLACK
            else:
                fill = BLACK
                outline = WHITE
            w = random.randint(10, width / 2)
            h = random.randint(10, height / 2)
            x = random.randint(0, width - w)
            y = random.randint(0, height - h)
            box = (x, y, x + w, y + h)
            draw.rectangle(box, fill=fill, outline=outline)

        # display image on the panel
        papirus.display(image)
        papirus.partial_update()


def display_file(papirus, file_name):
    """display resized image"""

    image = Image.open(file_name)
    image = ImageOps.grayscale(image)

    rs = image.resize((papirus.width, papirus.height))
    bw = rs.convert("1", dither=Image.FLOYDSTEINBERG)

    papirus.display(bw)
    papirus.update()

    time.sleep(3) # delay in seconds


# main
if "__main__" == __name__:
    if len(sys.argv) < 2:
        sys.exit('usage: {p:s} image-file'.format(p=sys.argv[0]))
    main(sys.argv[1:])
    
