#! /usr/bin/env python

from distutils.core import setup

setup(name='papirus',
      version='0.0.1',
      description="PaPiRus API",
      author='PiSupply',
      author_email='example@example.com',
      url='pi-supply.com',
      packages=['papirus'],
      install_requires=["pillow"],
      scripts=['bin/papirus-clear', 'bin/papirus-write', 'bin/papirus-set']
     )
