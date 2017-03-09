# Using the MCP7940N Hardware Clock on the Papirus HAT

During the Papirus Kickstarter campaign a lot of time has been spent on finding a hardware clock
with a proper alarm function and the right pogo pin to connect the alarm output to the Pi reset header.
This to make a wake-on-alarm function possible.
However a wake-on-alarm software example was not provided. The two examples in [RTCreboot](RTCreboot) and [RTCgpio](RTCgpio)
should give you sufficient information to use the hardware clock.
 
The Papirus HAT (not the Papirus Zero) has a MCP7940N battery backed-up hardware clock.
The MCP7940N is controlled via the i2c bus. Its i2c address is 0x6f.
For all the details on the MCP7940N see the [datasheet](mcp7940n.pdf).

The MCP7940N alarm output (MFP pin) on the Papirus hat is connected to a pulse shaping circuit. The output of this
circuit (signal RTC_OUT on the Papirus hat schematic) is connected to both the pogo pin and to RPi's GPIO 27
(pin 13 on the GPIO connector). The normal state of RTC_OUT is high. When the MFP output goes from high to low
a low pulse of about 12 msec is output on RTC_OUT. A low to high transition of the MFP output causes no change of RTC_OUT.

When the pogo pin is connected to the Raspberry Pi reset header the RTC_OUT pulse will cause
a (re)boot of the Pi even after it is shut down (but with power still connected).
When the pogo pin is not connected to the Pi reset header the RTC_OUT pulse can still be detected with GPIO 27.

The example in the [RTCreboot](RTCreboot) directory shows how to use the wake-on-alarm function.
When the pogo pin is not connected to the Raspberry Pi reset header you can stil detect the RTC_OUT pulses
using GPIO 27. See [RTCgpio](RTCgpio).

But first how to use the clock function to keep the time on the Pi between boots.

# Using the Hardware Clock

Raspbian Jessie has built-in support for the MCP7940N provided by the rtc_ds1307 module.
This module supports various i2c based real time clocks including the MCP7940N.
Add the following line to `/boot/config.txt`:
```
dtoverlay=i2c-rtc,mcp7940x=1
```
In order to set the system time from the hardware clock at boot you need to modify `/lib/udev/hwclock-set` by
commenting out the check for systemd:
```
#!/bin/sh
# Reset the System Clock to UTC if the hardware clock from which it
# was copied by the kernel was in localtime.

dev=$1

#if [ -e /run/systemd/system ] ; then
#    exit 0
#fi

if [ -e /run/udev/hwclock-set ]; then
    exit 0
fi
```
The reason for this is that standard Debian assumes the system time is already set from the hardware clock by systemd.
This requires a built-in hardware clock driver in the kernel since systemd does this before any modules are loaded.
Since the Pi can only use external hardware clocks, Raspbian only supports the hardware clock driver as a module.
Therefore we have to set the system clock from the hardware clock when udev detects the hardware clock.
Note that the system clock (and hence the hardware clock) on a Linux system is usually kept in UTC. 

After a reboot you can check if the MCP7940N has been recognized.
In the dmesg output you should find something like:
```
[    5.735640] rtc-ds1307 1-006f: rtc core: registered mcp7940x as rtc0
[    5.735692] rtc-ds1307 1-006f: 64 bytes nvram
```
If you have i2c-tools installed you can look at the i2cdetect output:
```
pi@papirus-hat:~ $ i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- 48 -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- UU 
70: -- -- -- -- -- -- -- -- 
```
The `UU` for MCP7940N address 0x6f means this address is used by a kernel driver (rtc_ds1307).
Address 0x48 is the temperature sensor on the Papirus hat.

You can check the current hardware clock time with the command `sudo hwclock -r`.
For more info try `sudo hwclock -r --debug`. Here is a sample output:
```
pi@papirus-hat:~ $ sudo hwclock -r --debug
hwclock from util-linux 2.25.2
Using the /dev interface to the clock.
Last drift adjustment done at 1470071156 seconds after 1969
Last calibration done at 1470071156 seconds after 1969
Hardware clock is on UTC time
Assuming hardware clock is kept in UTC time.
Waiting for clock tick...
/dev/rtc does not have interrupt functions. Waiting in loop for time from /dev/rtc to change
...got clock tick
Time read from Hardware Clock: 2016/08/05 19:33:53
Hw clock time : 2016/08/05 19:33:53 = 1470425633 seconds since 1969
Fri 05 Aug 2016 21:33:53 CEST  -0.133460 seconds
```
Note the hardware clock is in UTC, but the time is presented in CEST (Central European Summer Time).

You can set the hardware clock to the system clock with `sudo hwclock -w`
When you are connected to the internet you can just wait about 15 minutes.
The system (provided the ntp daemon is enabled, which it normally is in Raspbian) will copy the system
time to the hardware clock approximately once every 15 minutes.

Systemd provides a hwclock-save service which is run at shutdown. However when ntp is installed (/usr/sbin/ntpd
is an executable file) the system time is *not* copied to the hardware clock. Therefore I recommend to
comment out the ntpd check in `/lib/systemd/system/hwclock-save.service`:
```
[Unit]
Description=Synchronise Hardware Clock to System Clock
DefaultDependencies=no
Before=shutdown.target
#ConditionFileIsExecutable=!/usr/sbin/ntpd
ConditionFileIsExecutable=!/usr/sbin/openntpd
ConditionFileIsExecutable=!/usr/sbin/chrony
ConditionVirtualization=!container

[Service]
Type=oneshot
ExecStart=/sbin/hwclock -D --systohc

[Install]
WantedBy=reboot.target halt.target poweroff.target
```
This ensures the hardware clock is always set from the system clock at shutdown independent from the network and ntp.

# Accessing the MCP7940N from Python with the kernel driver (rtc_ds1307) loaded

If you try to access the MCP7940N registers with i2cget or i2cset (from i2c-tools) or from Python with the smbus
module you will get errors since the kernel has already claimed i2c address 0x6f.
In order to be able to set the MCP7940N alarm registers from Python we need to be able to access i2c addres 0x6f.

I have modified the smbus module (renamed to smbusf) so it allows access to an i2c device which the kernel has
already claimed. Smbusf uses the same mechanism as the '-f' option of i2cget/i2cset.  
See the [py-smbusf](py-smbusf) directory for details how to build and install this module.
Both the MCP7940N Python examples use the smbusf module. The smbusf calling interface is identical to the standard smbus
module.

# The Sample Programs

## Pogo pin connected to the Raspberry Pi reset header

See the [RTCreboot](RTCreboot) directory for details.

## Detecting the alarm output on GPIO 27 when the pogo pin is not connected

See the [RTCgpio](RTCgpio) directory for details.

## Video

See both in action on [YouTube](https://youtu.be/H8aviSTrx4Q).
