# I2C tools for Linux
#
# Copyright (C) 2007-2012  Jean Delvare <jdelvare@suse.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

CC	?= gcc

CFLAGS	?= -O2
# When debugging, use the following instead
#CFLAGS	:= -O -g
CFLAGS	+= -Wall

PYTHON ?= python
DISTUTILS := \
	CPPFLAGS="$(CPPFLAGS) -Iinclude" $(PYTHON) setup.py

all: include/linux/i2c-dev.h
	$(DISTUTILS) build

clean:
	$(DISTUTILS) clean
	rm -rf build

install:
	$(DISTUTILS) install --user
