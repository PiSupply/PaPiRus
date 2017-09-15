#! /usr/bin/env python

import time
import os
import argparse

import Image

from papirus import Papirus

WHITE = 1
BLACK = 0

PICTURES_TYPES = ['jpg', 'png', 'bmp', 'gif']

# Create an instance of papirus
papirus = Papirus()

def main():
    """main program"""
    p = argparse.ArgumentParser()
    p.add_argument('filepath', type=str, help="Path to pictures")
    p.add_argument('--delay', '-d', type=int, default=0, help="Extra delay between pictures")
    p.add_argument('--rotation', '-r', type=int, default=0, help="Rotation one of 0, 90, 180, 270")
    p.add_argument('--fullupdate', '-f', action='store_true', default=False, help="Force full update between each picture")
    p.add_argument('--loop', '-l', action='store_true', default=False, help="Sets the script in a continuous loop. CTRL^C to stop it")
    args = p.parse_args()

    papirus = Papirus(rotation=args.rotation)
    if args.filepath:
        print("Animation on PaPiRus.......")
        animate(papirus, args.filepath, args.delay, args.fullupdate, args.loop)
        print("Finished!")

def animate(papirus, imagepath, extradelay, fullupdate, loop):
    """animation"""

    reps = 0 # Counts the times the screen has been used even when in loop to ensure a refresh every 10

    papirus.clear()

    print('Displaying the animation')

    try: # Extracts name and extension of the first file in the list
        name = os.listdir(imagepath)[0].split(".")[0]
        extension = os.listdir(imagepath)[0].split(".")[1]
        if name.isdigit() and extension in PICTURES_TYPES: # If it is a number assumes it is an animated sequence
            stringnamepictures = False
            print('Numbered sequence')
        elif name[0].isalpha() and extension in PICTURES_TYPES: # If it is an alpha then it is a slideshow
            stringnamepictures = True
            print('Unnumbered sequence')
        else:
            print('There are no compatible files in the chosen directory')
            exit()
    except Exception as e:
        raise e
        print "No file found"

    try:
        while loop or reps == 0:
            for i in range(0, len(os.listdir(imagepath))):
                if not stringnamepictures:
                    name = imagepath + '/' + str(i+1) + '.' + extension
                else:
                    name = imagepath + '/' + os.listdir(imagepath)[i]
                reps = reps + 1
                if os.path.isfile(name):
                    image = Image.open(name)
                    image = image.resize((papirus.width, papirus.height), Image.ANTIALIAS)
                    image = image.convert("1", dither=Image.FLOYDSTEINBERG)

                    papirus.display(image)
                    if fullupdate or reps % 10 == 0: # Refresh every ten partials
                        papirus.update()
                    else:
                        papirus.partial_update()

                    if extradelay > 0:
                        time.sleep(extradelay)
    except KeyboardInterrupt:
        # quit
        papirus.clear()
        sys.exit()

    papirus.update()

# main
if "__main__" == __name__:
    main()

# Site for conversion https://ezgif.com/
# Resize to 264 then crop to 176 then optimise to remove some frames, finally sp                                                    lit

# Use the bulk rename bash script to rename the files into 1.gif, 2.gif, etc.
