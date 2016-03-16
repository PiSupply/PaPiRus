#!/usr/bin/python

import os
import sys
from papirus import Papirus
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from time import sleep
import RPi.GPIO as GPIO


user = os.getuid()
if user != 0:
    print "Please run script as root"
    sys.exit()

# Command line usage
# papirus-buttons

WHITE = 1
BLACK = 0

SIZE = 27

SW1 = 16
SW2 = 26
SW3 = 20
SW4 = 21

def main():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(SW1, GPIO.IN)
    GPIO.setup(SW2, GPIO.IN)
    GPIO.setup(SW3, GPIO.IN)
    GPIO.setup(SW4, GPIO.IN)

    papirus = Papirus()

    write_text(papirus, "Ready...", SIZE)

    while True:
        if GPIO.input(SW1) == False:
            write_text(papirus, "One", SIZE)

        if GPIO.input(SW2) == False:
            write_text(papirus, "Two", SIZE)

        if GPIO.input(SW3) == False:
            write_text(papirus, "Three", SIZE)

        if GPIO.input(SW4) == False:
            write_text(papirus, "Four", SIZE)

        sleep(0.1)

def write_text(papirus, text, size):

    # initially set all white background
    image = Image.new('1', papirus.size, WHITE)

    # prepare for drawing
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', size)

    # Calculate the max number of char to fit on line
    line_size = (papirus.width / (size*0.65))

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

    papirus.display(image)
    papirus.update()

if __name__ == '__main__':
    main()
