![Alt text](https://user-images.githubusercontent.com/1878314/73881257-e9cb7080-4857-11ea-8bb8-3d005c41bbac.png)
# PaPiRus
You can find here a variety of software, hardware and other resources for the [PaPiRus](http://papirus.ws) range of ePaper eInk displays from [Pi Supply](https://www.pi-supply.com). This repository is based on, and makes use of, the [rePaper/gratis GitHub repository](https://github.com/repaper/gratis).

You can purchase one of the PaPiRus boards from [our webshop](https://www.pi-supply.com/?s=papirus&post_type=product&tags=1&limit=5&ixwps=1) or from a variety of resellers worldwide.

# Setup PaPiRus
## Auto Installation
Just run the following script in a terminal window and PaPiRus will be automatically setup.
```bash
# Run this line and PaPiRus will be setup and installed
curl -sSL https://pisupp.ly/papiruscode | sudo bash
```

## Manual Installation
If you have any troubles with the auto installation or if for some reason you prefer to install PaPiRus manually, then follow the steps below.

### Python 2 and Python 3 support
The library and examples work on both Python 2 and Python 3. Currently (July 2020) Python 2 is still the default Python in Raspbian. The Python 2 and Python 3 versions can be installed side by side.


#### Enabling SPI and I2C interfaces on Raspberry Pi
Before using PaPiRus, do not forget to enable the SPI and the I2C interfaces.
You can enable the SPI by typing `sudo raspi-config` at the command line and then selecting `Interfacing options` > `SPI` and then selecting Enable. Without exiting the tool still in `Interfacing options` > `I2C` and then selecting Enable.
#### Install Python API (best to run all of these commands as root using sudo)
```bash
# Install dependencies
sudo apt-get install git bc i2c-tools fonts-freefont-ttf whiptail make gcc -y
# For Python 2
sudo apt-get install python-pil python-smbus python-dateutil -y
# For Python 3
sudo apt-get install python3-pil python3-smbus python3-dateutil python3-distutils -y

git clone --depth=1 https://github.com/PiSupply/PaPiRus.git
cd PaPiRus

# For Python 2
sudo python setup.py install    # Install PaPirRus python library
# For Python 3
sudo python3 setup.py install    # Install PaPirRus python library
```

#### Install Driver (Option 1) (best to run all of these commands as root using sudo)
```bash
sudo papirus-setup    # This will auto install the driver
```

#### Install Driver (Option 2) (best to run all of these commands as root using sudo)
```bash
# Install fuse driver
sudo apt-get install libfuse-dev -y

mkdir /tmp/papirus
cd /tmp/papirus
git clone https://github.com/repaper/gratis.git

cd /tmp/papirus/gratis
make rpi EPD_IO=epd_io.h PANEL_VERSION='V231_G2'
sudo make rpi-install EPD_IO=epd_io.h PANEL_VERSION='V231_G2'
sudo systemctl enable epd-fuse.service
sudo reboot
```

#### Select your screen size
```bash
sudo papirus-set [1.44 | 1.9 | 2.0 | 2.6 | 2.7 ]
or
sudo papirus-config
```
# Python API
**NOTE:** In the following examples where `rotation = rot` rot should be one of the following values: 0, 90, 180 or 270 degrees, depending on the screen orientation. i.e. `screen = Papirus([rotation = 90])`

#### The Basic API

```python
from papirus import Papirus

# The epaper screen object.
# Optional rotation argument: rot = 0, 90, 180 or 270 degrees
screen = Papirus([rotation = rot])

# Write a bitmap to the epaper screen
screen.display('./path/to/bmp/image')

# Perform a full update to the screen (slower)
screen.update()

# Update only the changed pixels (faster)
screen.partial_update()

# Update only the changed pixels with user defined update duration
screen.fast_update()

# Disable automatic use of LM75B temperature sensor
screen.use_lm75b = False

```

#### The Text API
```python
from papirus import PapirusText

text = PapirusText([rotation = rot])

# Write text to the screen
# text.write(text)
text.write("hello world")

# Write text to the screen specifying all options
text.write(text, [size = <size> ],[fontPath = <fontpath>],[maxLines = <n>])
# maxLines is the max number of lines to autowrap the given text.
# New lines ('\n') in the text will not go to the next line, but are interpreted as white space.
# Use PapirusTextPos() instead which recognizes '\n'.
```

#### The Positional Text API (example 1)
```python
from papirus import PapirusTextPos

# Same as calling "PapirusTextPos(True [,rotation = rot])"
text = PapirusTextPos([rotation = rot])

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
```

#### The Positional Text API (example 2)
```python
from papirus import PapirusTextPos

# Calling PapirusTextPos this way will mean nothing is written to the screen by default
text = PapirusTextPos(False [,rotation = rot])

# Write text to the screen at selected point, with an Id
# Nothing will show on the screen
text.AddText("hello world", 10, 10, Id="Start" )

# Add another line of text, at the default location
# Nothing will show on the screen
text.AddText("Another line", Id="Top")

# Now display BOTH lines on the screen
text.WriteAll()

# Update the first line
# No change will happen on the screen
text.UpdateText("Start", "New Text")

# Remove the second line of text
# The text won't be removed from the screen yet
text.RemoveText("Top")

# Now update the screen to show the changes
text.WriteAll()
```

#### The Positional Text API (example 3)
```python
from papirus import PapirusTextPos

# Same as calling "PapirusTextPos(True)"
text = PapirusTextPos()

# Write text to the screen at selected point, with an Id
# This will write "hello world" to the screen with white text and a black background
text.AddText("hello world", 10, 10, Id="Start", invert=True)
```

#### Notes
PapirusTextPos will take into account \n as a line break (or multiple line breaks)
Meaning text will be aligned to the X position given, it will not return to x=0 for the start of the next line.

When the text is longer than will fit on a single line, PapirusTextPos will break the text into multiple lines.
You can limit the number of lines by specifying the parameter `maxLines` in the `AddText()` method.

When using the PapirusTextPos, in either mode, setting the "partialUpdates" property to True will cause partial updates to be done, meaning only the section of the PaPiRus screen that has been changed will be updated.  These can be vastly quicker than a full update for each piece of text.

If not using the "partialUpdates" property, calling `WriteAll(True)` will do the same thing on a one off basis.

#### Unicode Support in the Text API
```python
from papirus import PapirusText

text = PapirusText()

# Write text to the screen, in this case forty stars alternating black and white
# note the use of u"" syntax to specify unicode (needed for Python 2, optional for Python 3 since unicode is default in Python 3)
text.write(u"\u2605 \u2606 \u2605 \u2606 \u2605 \u2606 \u2605 \u2606 \u2605 \u2606 \u2605 \u2606 \u2605 \u2606 \u2605 \u2606 \u2605 \u2606 \u2605 \u2606 \u2605 \u2606 \u2605 \u2606 \u2605 \u2606 \u2605 \u2606 \u2605 \u2606 \u2605 \u2606 \u2605 \u2606 \u2605 \u2606 \u2605 \u2606 \u2605 \u2606")
```
#### Note
The default font, FreeMono, has [limited unicode support](http://www.fileformat.info/info/unicode/font/freemono/blocklist.htm), so you may want to specify an alternate font to use a fuller range characters.

#### The Image API
```python
from papirus import PapirusImage

image = PapirusImage([rotation = rot])

# easy write image to screen
# image.write(path)
image.write('/path/to/image')
```

#### The composite API (Text and image)
```python
from papirus import PapirusComposite

# Calling PapirusComposite this way will mean nothing is written to the screen until WriteAll is called
textNImg = PapirusComposite(False [, rotation = rot])

# Write text to the screen at selected point, with an Id
# Nothing will show on the screen
textNImg.AddText("hello world", 10, 10, Id="Start" )

# Add image
# Nothing will show on the screen
# textNImg.AddImg(path, posX,posY,(w,h),id)
textNImg.AddImg("/path/to/image",20,20,(25,25), Id="BigImg")

# Add image to the default place and size
# Nothing will show on the screen
textNImg.AddImg("/path/to/image", Id="Top")

# Now display all elements on the screen
textNImg.WriteAll()

# Update the first line
# No change will happen on the screen
textNImg.UpdateText("Start", "New Text")

# Update the BigImg
# No change will happen on the screen
textNImg.UpdateImg("BigImg", "/path/to/new/images")

# Remove top image
# The images won't be removed from the screen yet
textNImg.RemoveImg("Top")

# Now update the screen to show the changes
textNImg.WriteAll()
```

#### Code versioning
For PaPiRus we have adopted a common definition for the major.minor.micro version number. Whenever submitting code make sure to update the version number if applicable.

* The major number should be increased whenever the API changes in an incompatible way.
* The minor number should be increased whenever the API changes in a compatible way.
* The micro number should be increased whenever the implementation changes, while the API does not.

You can change the version in the [__init__.py](https://github.com/PiSupply/PaPiRus/blob/master/papirus/__init__.py).

#### Font family
PaPiRusText and PaPiRusTextPos are using the font _FreeMono.ttf_ by default. It is possible to specify the argument `font_path` in `PapirusText.write`, `PapirusTextPos.AddText`, `PapirusTextPos.UpdateText` and `PapirusTextPos.addToImageText` to change the _font family_. The argument must be a string containing the path to the _.ttf_ file.
```
# Change font family
from papirus import PapirusText
text = PapirusText()
text.write("Hello World", fontPath='/path/to/ttf')
```

# Command Line

```bash
# Set the screen size you are using
papirus-set [1.44 | 1.9 | 2.0 | 2.6 | 2.7 ]

# Write data to the screen
papirus-write "Some text to write" [-x ] [-y ] [-fsize ] [-rot] [-inv]

# Draw image on the screen
papirus-draw /path/to/image -t [resize | crop] -r [0 | 90 | 180 | 270] [-i]

# Clear the screen
papirus-clear

```
**Note:** The line break '\n' is not converted by the shell (bash). In order to do this you need to use the method described [here](https://stackoverflow.com/questions/3005963/how-can-i-have-a-newline-in-a-string-in-sh). For example: `papirus-write $'hello\nWorld'`. Bear in mind that you need to use single quotes after the '$', double quotes do not work.

### Demos
All demos can be seen by running the following commands. Code can be found in the repo for the python bin directory.

```bash
# Board and screen diagnostic
papirus-test

# Show clock
papirus-clock [rotation]

# Run game of life
papirus-gol

# Show system information
papirus-system

# Push framebuffer to screen
papirus-framepush (coming soon)

# Demo of using the buttons
papirus-buttons [rotation]

# Demo of getting temperature from LM75
papirus-temp [rotation]

# Demo showing effect of fast update
papirus-radar

# Display text filling the width of the display
papirus-textfill 'Some text' [rotation]

# Snake game
papirus-snake

# Display Twitter feeds
papirus-twitter

# Composite text and graphics
papirus-composite-write

# Copy framebuffer (text console or desktop) to PaPiRus using the buttons to zoom and pan
# Only for 2.7" and 2.0" displays
papirus-fbcopy

# Display image sequences or slideshow
# For an animation, the directory containing the images must have numbered images in the form 0.gif, 1.gif, 2.gif, etc.
# Otherwise the images will be displayed in filename order.
papirus-animation [--delay DELAY] [--rotation ROTATION] [--fullupdate] [--loop] directory

# Take a picture with the RPi camera using the PaPiRus screen as viewfinder
# Only for 2.7" and 2.0" displays
papirus-cam
```

### Demos for using the Real Time Clock of the PaPiRus HAT

The PaPiRus HAT has a battery backed-up Real Time Clock. For more information about the RTC and demos see the
[RTC-Hat-Examples](./RTC-Hat-Examples) directory and README files.

### Tips for using images
The PaPiRus can only display Bitmap images (.BMP) in black and white (1 bit colour). If you pass an image to PaPiRus
that is not a 1 Bit Bitmap, it will automatically be converted to this by the software. However, for best results
and higher image quality we would recommend that you convert the image to a 1 Bit Bitmap before pushing to the
PaPiRus screen using GIMP or Photoshop or similar photo editing tools like
[the rePaper companion](https://github.com/aerialist/repaper_companion) to resize images and convert them to XBM format
or [WIF (the WyoLum Image Format)](http://wyolum.com/introducing-wif-the-wyolum-image-format/).

### Screen Resolutions
The screens have the following screen resolutions:
```
1.44"     128 x 96
1.9"      144 x 128
2.0"      200 x 96
2.6"      232 x 128
2.7"      264 x 176
```

### Refresh rates and screen lifespan
A typical ePaper refresh rate for a full-screen update is around 1 to 2 Hz (1 to 2 updates per second). The refresh rate of the ePaper displays is dependent on a number of factors including temperature. At lower temperatures you have to drive the display more slowly otherwise you can get "ghosting" and also can damage the display.

Lastly, a good way to increase the refresh rate of information on the screen is to not use full screen updates but use partial updates as described below.

### Full and Partial Updates
Also try using the method partial_update() instead of the update() one if you want to refresh the screen faster and maybe want to create some simple animations. Remember though that the partial method cannot be used indefinitely.
You should refresh the screen using a Full Update every few minutes and it is also recommended to completely power down the screen every few hours.

### Fast Update
Fast Update works the same as Partial Update, except the refresh rate is not dependent on temperature but can be set by the user. The refresh duration for this mode is set in milliseconds by writing to `/dev/epd/pu_stagetime`. See the papirus-radar demo code for details.
Using this mode is only advised if you know what you are doing as it will severely reduce the life of the display and may cause other bizarre side-effects.
As with the Partial Update mode you should refresh the screen using a Full Update every few minutes and it is also recommended to completely power down the screen every few hours.

# Hardware tips
In case you have problems assembling the board please [check this article on our website](https://www.pi-supply.com/make/papirus-assembly-tips-and-gotchas/) on which you can find:
* Connect the screen to the PaPiRus board
* Connect the GPIO adapter
* Install the pogo pin connector
* Install the push buttons

Please note: Not all the sections apply to both the PaPiRus HAT and the PaPiRus Zero.

### Datasheets, connectivity, pinout, jumpers and further information
For additional information follow the links below:
* [PaPiRus HAT](https://github.com/PiSupply/PaPiRus/tree/master/hardware/PaPiRus%20HAT)
* [PaPiRus Zero](https://github.com/PiSupply/PaPiRus/tree/master/hardware/PaPiRus%20Zero)
* [Pinout.xyz resources](https://pinout.xyz/boards#manufacturer=Pi%20Supply)

# Third party software libraries

It is safe to say we have an awesome and growing community of people using epaper with PaPiRus and beyond and we get a huge amount of contributions of code, some of which we can easily integrate here and others which we can't (we are only a small team). However we want to make sure that any contributions are easy to find, for anyone looking. So here is a list of other software libraries that might be useful to you (if you have one of your own, please visit the ["Issues"](https://github.com/PiSupply/PaPiRus/issues) tab above and let us know!):

* [Go software library for driving PaPiRus](https://github.com/wmarbut/go-epdfuse)
* [RISC OS software library for driving PaPiRus](https://www.riscosopen.org/forum/forums/1/topics/9142?page=1)
* [PaPiRus HAT working with resin.io](https://github.com/resin-io-playground/resinio-PaPiRus)
* [Raspberry Pi Internal Watchdog Setup and Information](http://www.switchdoc.com/2014/11/reliable-projects-using-internal-watchdog-timer-raspberry-pi/)
* [Baseball Pi - get the live box score, plays, and batter stats of your favorite MLB team right on your desktop](https://github.com/eat-sleep-code/baseball-pi)
* PaPiRus Netapp (find Raspberry Pi’s on your network, run a speed test of your internet connection, show a graph of your past speed test results) - [blog here](https://www.talktech.info/2017/09/30/papirus-netapp/) and [GitHub Repo here](https://github.com/vwillcox/papirus-netapp)
* [PaPiRus Ruby gem for the Raspberry Pi PaPiRus eInk screen](https://github.com/mmolhoek/papirus)
* [PaPiRuby - Ruby wrapper for the Raspberry Pi PaPiRus eInk screen](https://github.com/EddWills95/PaPiRuby)
* Power outage monitor (using PiJuice and PaPiRus) by Frederick Vandenbosch. [You can find pictures and code here](http://frederickvandenbosch.be/?p=2876)
