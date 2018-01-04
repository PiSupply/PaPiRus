# Read time from real time clock using the ioctl interface for /dev/rtc
#

from __future__ import print_function

from collections import namedtuple
from datetime import datetime
from fcntl import ioctl
import struct
from dateutil.tz import tzutc

# From /usr/include/asm-generic/ioctl.h
_IOC_NRBITS = 8
_IOC_TYPEBITS = 8
_IOC_SIZEBITS = 14
_IOC_DIRBITS = 2

_IOC_NRMASK = (1 << _IOC_NRBITS) - 1
_IOC_TYPEMASK = (1 << _IOC_TYPEBITS) - 1
_IOC_SIZEMASK = (1 << _IOC_SIZEBITS) - 1
_IOC_DIRMASK = (1 << _IOC_DIRBITS) - 1

_IOC_NRSHIFT = 0
_IOC_TYPESHIFT = _IOC_NRSHIFT + _IOC_NRBITS
_IOC_SIZESHIFT = _IOC_TYPESHIFT + _IOC_TYPEBITS
_IOC_DIRSHIFT = _IOC_SIZESHIFT + _IOC_SIZEBITS

_IOC_NONE = 0
_IOC_WRITE = 1
_IOC_READ = 2

def _IOC(dir, type, nr, size):
    return ((dir << _IOC_DIRSHIFT) |
            (type << _IOC_TYPESHIFT) |
            (nr << _IOC_NRSHIFT) |
            (size << _IOC_SIZESHIFT))

def _IOC_TYPECHECK(t):
    return len(t)

def _IO(type, nr):
    return _IOC(_IOC_NONE, type, nr, 0)

def _IOR(type, nr, size):
    return _IOC(_IOC_READ, type, nr, _IOC_TYPECHECK(size))

def _IOW(type, nr, size):
    return _IOC(_IOC_WRITE, type, nr, _IOC_TYPECHECK(size))

class RtcTime(namedtuple(
    # man(4) rtc
    "RtcTime",
    "tm_sec tm_min tm_hour "
    "tm_mday tm_mon tm_year "
    "tm_wday tm_yday tm_isdst"  # Last row is unused.
)):

    _fmt = 9 * "i"

    def __new__(cls, tm_sec=0, tm_min=0, tm_hour=0,
                tm_mday=0, tm_mon=0, tm_year=0,
                tm_wday=0, tm_yday=0, tm_isdst=0):
        return super(RtcTime, cls).__new__(cls, tm_sec, tm_min, tm_hour,
                                            tm_mday, tm_mon, tm_year,
                                            tm_wday, tm_yday, tm_isdst)

    def to_datetime(self):
        # From `hwclock.c`.
        return datetime(
            year=self.tm_year + 1900, month=self.tm_mon + 1, day=self.tm_mday,
            hour=self.tm_hour, minute=self.tm_min, second=self.tm_sec,
            tzinfo=tzutc())

    def pack(self):
        return struct.pack(self._fmt, *self)

    @classmethod
    def unpack(cls, buffer):
        return cls._make(struct.unpack(cls._fmt, buffer))

# From /usr/include/linux/rtc.h
rtc_time = RtcTime().pack()
RTC_RD_TIME = _IOR(ord("p"), 0x09, rtc_time)   # 0x80247009
RTC_SET_TIME = _IOW(ord("p"), 0x0a, rtc_time)  # 0x4024700a
del rtc_time

def get_hwclock(devrtc="/dev/rtc"):
    with open(devrtc) as rtc:
        ret = ioctl(rtc, RTC_RD_TIME, RtcTime().pack())
    return RtcTime.unpack(ret).to_datetime()

if __name__ == "__main__":
    print("Date/Time from RTC: {d:s}".format(d= get_hwclock().strftime("%A %d %B %Y - %H:%M:%S")))

