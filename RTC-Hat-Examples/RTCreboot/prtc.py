# utility functions for Papirus Hat hardware clock (MCP7940N)

from __future__ import division

from datetime import datetime
from calendar import isleap

RTCADR = 0x6f
STBIT = 0x80
LPYR = 0x20
almbase = [0xa, 0x11]


def tobcd(val):
    return (val % 10) | (val // 10) << 4


def writertc(i2cbus, dt):
    sec = dt.second
    min = dt.minute
    hour = dt.hour
    # rtc-ds1307 uses weekday convention Sun = 1, Sat = 7
    wkday = (dt.weekday() + 1) % 7 + 1
    day = dt.day
    month = dt.month
    year = dt.year
    leap = isleap(year)

    data = [0, 0, 0, 0, 0, 0, 0]
    data[0] = tobcd(sec) | STBIT
    data[1] = tobcd(min)
    data[2] = tobcd(hour)
    bits345 = i2cbus.read_byte_data(RTCADR, 3) & 0x38
    data[3] = bits345 | wkday
    data[4] = tobcd(day)
    data[5] = tobcd(month)
    if leap:
        data[5] |= LPYR
    data[6] = tobcd(year % 100)

    i2cbus.write_i2c_block_data(RTCADR, 0, data)


def writealm(i2cbus, alm, dt):
    if alm > 0:
        alm = 1
    else:
        alm = 0
    sec = dt.second
    min = dt.minute
    hour = dt.hour
    # rtc-ds1307 uses weekday convention Sun = 1, Sat = 7
    # wkday in alarm has to match the wkday of rtc time 
    # for the alarm to trigger
    wkday = (dt.weekday() + 1) % 7 + 1
    day = dt.day
    month = dt.month

    data = [0, 0, 0, 0, 0, 0]
    data[0] = tobcd(sec)
    data[1] = tobcd(min)
    data[2] = tobcd(hour)
    data[3] = 0x70 | wkday  # ALM0MSK = 111
    data[4] = tobcd(day)
    data[5] = tobcd(month)

    i2cbus.write_i2c_block_data(RTCADR, almbase[alm], data)


def readrtc(i2cbus):
    data = i2cbus.read_i2c_block_data(RTCADR, 0, 7)

    sec = (data[0] & 0x7f) // 16 * 10 + (data[0] & 0x0f)
    min = data[1] // 16 * 10 + (data[1] & 0x0f)
    hour = data[2] // 16 * 10 + (data[2] & 0x0f)
    day = data[4] // 16 * 10 + (data[4] & 0x0f)
    month = (data[5] & 0x10) // 16 * 10 + (data[5] & 0x0f)
    year = data[6] // 16 * 10 + (data[6] & 0x0f)
    dt = datetime(2000+year, month, day, hour, min, sec)
    return dt


def readalm(i2cbus, alm):
    if alm > 0:
        alm = 1
    else:
        alm = 0
    data = i2cbus.read_i2c_block_data(RTCADR, almbase[alm], 6)

    sec = data[0] // 16 * 10 + (data[0] & 0x0f)
    min = data[1] // 16 * 10 + (data[1] & 0x0f)
    hour = data[2] // 16 * 10 + (data[2] & 0x0f)
    day = data[4] // 16 * 10 + (data[4] & 0x0f)
    month = data[5] // 16 * 10 + (data[5] & 0x0f)
    # year not used in alarm time
    dt = datetime(2000, month, day, hour, min, sec)
    return dt


def enablealm0(i2cbus):
    data = i2cbus.read_byte_data(RTCADR, 7)
    data |= 0x10
    i2cbus.write_byte_data(RTCADR, 7, data)


def enablealm1(i2cbus):
    data = i2cbus.read_byte_data(RTCADR, 7)
    data |= 0x20
    i2cbus.write_byte_data(RTCADR, 7, data)


def disablealm0(i2cbus):
    # When disabling the alarm, keep the mfp output high
    # (otherwise we'll get an immediate reboot)
    data = i2cbus.read_byte_data(RTCADR, 7)
    data &= 0xef
    data |= 0x80
    i2cbus.write_byte_data(RTCADR, 7, data)


def disablealm1(i2cbus):
    # When disabling the alarm, keep the mfp output high
    # (otherwise we'll get an immediate reboot)
    data = i2cbus.read_byte_data(RTCADR, 7)
    data &= 0xdf
    data |= 0x80
    i2cbus.write_byte_data(RTCADR, 7, data)


def enablesqw(i2cbus):
    # Set 1 Hz square wave output
    i2cbus.write_byte_data(RTCADR, 7, 0x40)


def disablesqw(i2cbus):
    # Disable square wave and set ouput high
    i2cbus.write_byte_data(RTCADR, 7, 0x80)


def mfpoutput(i2cbus, val):
    # set MFP output directly
    if val == 0:
        data = 0x00
    else:
        data = 0x80
    i2cbus.write_byte_data(RTCADR, 7, data)
