#! /usr/bin/env python

from distutils.core import setup

setup(name='papirus',
      version='1.0.0',
      description="PaPiRus API",
      author='PiSupply',
      author_email='sales@pi-supply.com',
      url='pi-supply.com',
      packages=['papirus'],
      scripts=['bin/papirus-animation','bin/papirus-buttons', 'bin/papirus-cam', 'bin/papirus-clear', 'bin/papirus-clock', 'bin/papirus-composite-write', 'bin/papirus-config', 'bin/papirus-draw', 'bin/papirus-gol', 'bin/papirus-radar', 'bin/papirus-set', 'bin/papirus-setup', 'bin/papirus-temp', 'bin/papirus-test', 'bin/papirus-system', 'bin/papirus-textfill', 'bin/papirus-twitter', 'bin/papirus-write', 'bin/papirus-snake', 'bin/papirus-fbcopy'],
      data_files=[('bitmaps', ['bitmaps/papirus-logo.bmp', 'bitmaps/0.gif', 'bitmaps/1.gif', 'bitmaps/2.gif', 'bitmaps/3.gif', 'bitmaps/4.gif', 'bitmaps/5.gif', 'bitmaps/6.gif', 'bitmaps/7.gif', 'bitmaps/8.gif', 'bitmaps/9.gif', 'bitmaps/10.gif', 'bitmaps/11.gif', 'bitmaps/12.gif', 'bitmaps/13.gif', 'bitmaps/14.gif', 'bitmaps/15.gif', 'bitmaps/papirus-cam-intro.jpg', 'bitmaps/python.png'])]
     )
