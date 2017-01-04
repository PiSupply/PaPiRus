# PaPiRus
Resources for PaPiRus ePaper eInk display

# Enabling SPI and I2C interfaces on Raspberry Pi
Before using PaPiRus, do not forget to enable the SPI and the I2C interfaces.
You can enable the SPI by typing `sudo raspi-config` at the command line and then selecting `Interfacing options` > `SPI` and then selecting Enable. Without exiting the tool still in `Interfacing options` > `I2C` and then selecting Enable.

# Setup PaPiRus
```bash
# Run this line and PaPiRus will be setup and installed
curl -sSL https://goo.gl/i1Imel | sudo bash
```

# Getting Started
```bash
# Select your screen size
sudo papirus-set [1.44 | 1.9 | 2.0 | 2.6 | 2.7 ]
or
sudo papirus-config
# System will now reboot
```

# Manual Installation

#### Install Python API
```bash

# Install dependencies
sudo apt-get install python-imaging

git clone https://github.com/PiSupply/PaPiRus.git
cd PaPiRus
sudo python setup.py install    # Install PaPirRus python library
```

#### Install Driver (Option 1)
```bash
papirus-setup    # This will auto install the driver
````

#### Install Driver (Option 2)
```bash
# Install fuse driver
sudo apt-get install libfuse-dev -y

sudo mkdir /tmp/papirus
cd /tmp/papirus
git clone https://github.com/repaper/gratis.git

cd /tmp/papirus/gratis-master/PlatformWithOS
make rpi-epd_fuse
sudo make rpi-install
sudo service epd-fuse start
```

# Python API

#### The Basic API

```python
from papirus import Papirus

# The epaper screen object
screen = Papirus()

# Write a bitmap to the epaper screen
screen.display('./path/to/bmp/image')

# Perform a full update to the screen (slower)
screen.update()

# Update only the changed pixels (faster)
screen.partial_update()

# Change screen size
# SCREEN SIZES 1_44INCH | 1_9INCH | 2_0INCH | 2_6INCH | 2_7INCH
screen.set_size(papirus.2_7INCH)

```

#### The Text API
```python
from papirus import PapirusText

text = PapirusText()

# Write text to the screen
# text.write(text)
text.write("hello world")
```

#### The Positional Text API
```python (Example 1)
from papirus import PapirusTextPos

# Same as calling "PapirusTextPos(True)"
text = PapirusTextPos()

# Write text to the screen at selected point, with an Id
# "hello world" will appear on the screen at (10, 10), font size 20, straight away
text.AddText("hello world", 10, 10, Id="Start" )

# Add another line of text, at the default location
# "Another line" will appear on screen at (0, 0), font size 20, straight away
text.AddText("Another line", Id="Top")

# Update the first line
# "hello world" will disappear and "New Text" will be displayed straight away
text.UpdateText("Start", "New Text")

# Remove The second line of text
# "Another line" will be removed from the screen straight away
text.RemoveText("Top")

# Clear all text from the screen
# This does a full update so is a little slower than just removing the text.
text.Clear()


```python (Example 2)
from papirus import PapirusTextPos

# Calling PapirusTextPos this way will mean nothing is written to the screen be default
text = PapirusTextPos(False)

# Write text to the screen at selected point, with an Id
# Nothing will show on the screen
text.AddText("hello world", 10, 10, Id="Start" )

# Add another line of text, at the default location
# Nothing will show on the screen
text.AddText("Another line", Id="Top")

# Now display BOTH lines on the scrren
text.WriteAll()

# Update the first line
# No change will happen on the screen
text.UpdateText("Start", "New Text")

# Remove The second line of text
# The text won't be removed just yet from the screen
text.RemoveText("Top")

# Now update the screen to show the changes
text.WriteAll()
```

#### The Image API
```python
from papirus import PapirusImage

image = PapirusImage()

# easy write image to screen
# image.write(path)
image.write('/path/to/image')

# write image to the screen with size and position
# image.write(path, width, (x,y))
image.write('/path/to/image', 20, (10, 10) )
```
#### Notes
PaPiRusTextPos will take in to account \n as a line break (or multiple line breaks)
Meaning text will be aligned to the X position given, it will not return to x=0 for the start of the next line.

```

# Command Line

```bash
# Set the screen size you are using
papirus-set [1.44 | 1.9 | 2.0 | 2.6 | 2.7 ]

# Write data to the screen
papirus-write "Some text to write"

# Draw image on the screen
papirus-draw /path/to/image -t [resize | crop]

# Clear the screen
papirus-clear
```

#### Demos
All demos can be seen by running the following commands. Code can be found in the repo for the python bin directory. 

```bash
# Show clock
papirus-clock

# Run game of life
papirus-gol

# Show system information
papirus-system

# Push framebuffer to screen
papirus-framepush

# Demo of using the buttons
papirus-buttons

# Demo of getting temperature from LM75
papirus-temp

# Snakes game
papirus-snakes
```
