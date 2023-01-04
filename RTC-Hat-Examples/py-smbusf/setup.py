#!/usr/bin/env python

from distutils.core import setup, Extension

setup(
    name="smbusf",
    version="1.1",
    description="Python bindings for Linux SMBus access through i2c-dev, forced access version",
    author="Mark M. Hoffman",
    author_email="mhoffman@lightlink.com",
    maintainer="Mark M. Hoffman",
    maintainer_email="linux-i2c@vger.kernel.org",
    license="GPLv2",
    url="http://lm-sensors.org/",
    ext_modules=[Extension("smbusf", ["smbusmodule.c"])])
