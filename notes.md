***Notes***

[if using a 4.1.x+ kernel on raspbian jessie edit epd-fuse script to s/spi_bcm2708/spi_bcm2835/g seems true for all 40pin GPIO raspberry pi's e.g. A+,B+,2B possibly PiZero too]

EPD (2.7)
264x175 == 46464 bits, == 5808 bytes

origin top left

arranged in rows in memory

0,0 -> 263,0

```
rev 1.6 RTC has been changed to be a Microchip part. MCP7940N -- address range 0x68 to 0x6F
--------

modprobe i2c-dev
modprobe i2c:mcp7941x
echo mcp7941x 0x6f > /sys/class/i2c-dev/i2c-1/device/new_device
hwclock -s

------------------------

NXP LM75BD Temperature sensor
http://www.nxp.com/documents/data_sheet/LM75B.pdf
It is supposed to be on I2C at 0x48 but my particular PCB revision either I am doing something wrong or the LM75BD doesn't work. I have v1.4 rev of the PCB the KS people will be getting v1.5 rev so will leave it alone until 1.5's are out in the wild.

buttons gpio.25,27,28,29 (physical pins 36,37,38,40)
