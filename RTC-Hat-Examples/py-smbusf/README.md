# py-smbusf

This module is identical to the normal smbus module, but it allows to access
i2c devices already claimed by a kernel driveri (e.g. the hardware clock in our case).  
This is the same as using the '-f' option on the i2c-get and i2c-set programs from i2c-tools.

You need the python-devel package for building this module:
```
  sudo apt-get install python-dev
```

To build and install: 
```
  # For Python 2
  $ make clean
  $ make install

  # For Python 3
  $ make clean
  $ PYTHON=python3 make install
```
This will install the module in the directory: `/home/pi/.local/lib/python2.7/site-packages` for Python 2
and in the directori `/home/pi/.local/lib/python3.x/site-packages` for Python 3..  

Programs using this module therefore need to run as user pi.
