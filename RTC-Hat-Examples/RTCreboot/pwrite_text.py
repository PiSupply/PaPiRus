#!/usr/bin/env python

from papirus import Papirus
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os

WHITE = 1
BLACK = 0
RTCADR = 0x6f

lock = False


def main():
    papirus = Papirus()

    write_text(papirus, 'Line 1', save=True)
    write_text(papirus, 'Line 2', y=20, load=True, ldfile='save.bmp')


def write_text(papirus, text, x=0, y=0, size=20, load=False, ldfile=' ',
               save=False, file='save.bmp'):
    global image, draw, font

    if os.path.isfile(ldfile):
        image = Image.open(ldfile)
        image.load()
        os.remove(ldfile)
    else:
        # set all white background
        image = Image.new('1', papirus.size, WHITE)

    # prepare for drawing
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(
               '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', size)

    # Calculate the max number of char to fit on line
    line_size = ((papirus.width - x) / (size*0.65))

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
        draw.text( (x, (size*current_line + y)), l, font=font, fill=BLACK)
        current_line += 1

    papirus.display(image)
    papirus.partial_update()
    if (save):
        image.save(file)


def replace_line(papirus, x, y, text, size=20):
    global image, draw, font, lock

    while lock:
        pass
    lock = True
    draw.rectangle((x, y, papirus.width, y + size), fill=WHITE, outline=WHITE)
    draw.text((x, y), text, font=font, fill=BLACK)
    lock = False


def update_lines(papirus):
    global image
    papirus.display(image)
    papirus.partial_update()


if __name__ == '__main__':
    main()
