#! /usr/bin/env python

from distutils.core import setup

setup(name='papirus',
      version='0.0.1',
      description="PaPiRus API",
      author='PiSupply',
      author_email='example@example.com',
      url='pi-supply.com',
      packages=['papirus'],
      scripts=['bin/papirus-buttons', 'bin/papirus-clear', 'bin/papirus-clock', 'bin/papirus-composite-write', 'bin/papirus-config', 'bin/papirus-draw', 'bin/papirus-gol', 'bin/papirus-radar', 'bin/papirus-set', 'bin/papirus-setup', 'bin/papirus-temp', 'bin/papirus-system', 'bin/papirus-textfill', 'bin/papirus-twitter', 'bin/papirus-write'],
      data_files=[('bitmaps', ['bin/papirus-logo.bmp'])]
     )
