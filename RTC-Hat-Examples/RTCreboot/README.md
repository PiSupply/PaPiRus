# Rebooting the PI using the wake-on-alarm function of the MCP7940N

This example uses two programs:

* `rtcreboot` which sets the alarm a number of seconds in the future and then shuts down the RPi.
  The default is 120 seconds. You can specify a different delay (in seconds) as an argument to rtcreboot.
  `rtcreboot` writes the expected reboot time on the Papirus display.

* the second program is `bootinfo` which should be run at system boot. This writes the start time (the output
  from `uptime -s`, the current system time and the hardware clock time (normally in UTC) to the Papirus display.

Both programs rely on the smbusf module (See [py_smbusf](../py-smbusf) for build and installation instructions).
In order to run `bootinfo` at system boot add the following line to `/etc/rc.local`:
```
sudo -u pi /home/pi/PaPiRus/RTC-Hat-Examples/RTCreboot/bootinfo
```
Modify the path as required for your installation.  
`bootinfo` has to be run as user pi, since the smbusf module is only installed for user pi when you follow the
instructions in [py_smbusf](../py-smbusf).

Both programs use support functions in `prtc.py` (hardware clock access functions) and `pwrite_text.py` (custom
version to write text on the Papirus display)

The programs text output is layed out for the large Papirus display (2.7 inch 264 x 176).

For the programming details of the MCP7940N the [datasheet](../mcp7940n.pdf) is the best reference.
See section 5 and especially section 5.4 about alarms.
