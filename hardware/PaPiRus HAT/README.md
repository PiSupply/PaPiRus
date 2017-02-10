#PaPiRus HAT additional details
##Pinout for buttons 

As mentioned on the description and packaging, these buttons are optional and if you want to use them you will need to solder yourself. If you do, they connect as follows:

```
SW1 = BUT1 = pin 36 = GPIO 16

SW2 = BUT2 = pin 37 = GPIO 26

SW3 = BUT3 = pin 38 = GPIO 20

SW4 = BUT4 = pin 40 = GPIO 21
```

##Jumper settings and meaning
CN2 (Used to power the board from a different platform e.g. Arduino)
```
2-3 for 5V
1-2 for 3V3
```
CN14
```
2-3 for 1.44"-2.0"
1-2 for 2.7"
No  for 1.9"-2.6"
```

##Solder Pad
```
CN5   3V3
CN6   5V
CN7   GND
CN8   I2C_SDA
CN9   I2C_SCL
CN10  RTC
CN11  Raspberry Pi pin 7
CN12  Raspberry Pi pin 15
```
##Additional FPC connector

On the underside of the PaPiRus HAT ([picture here](https://www.pi-supply.com/wp-content/uploads/2015/06/PaPiRus-HAT-10-1000.png)) you will see two FPC connectors. The one closest to the edge (with a brown clasp - CN1) is for the ePaper display to connect into. The other FPC connector (CN4), is for use as a GPIO breakout in conjunction with the [GPIO breakout adapter](https://www.pi-supply.com/product/gpio-adapter-for-rpi-display-b-with-choice-of-header/) from Watterott Electronic. This can be used in one of two ways...either to breakout the GPIO pins and use them for additional purposes whilst the HAT is on top of the Pi, or to connect the PaPiRus HAT to the Raspberry Pi from further away, using an FPC cable (for example, if you wanted to mount the screen on the side of a case but have the Pi itself in the base of the case).

##Pogo Pin

There is a pogo pin included in the packaging for free. The purpose of this is to utilise the wake-on-alarm functionality built into the RTC (real time clock) on the HAT. This ties into the RUN pin on the Raspberry Pi and allows the Pi to be waken from a "halt" state at a specific time that you set in the RTC. There are two available positions for this - one for the A+/B+/2B and one for the new location on the Pi 3B. This needs to be soldered into place if you wish to use this functionality. The part number for the Pogo Pin is a Mil-Max 0908-9-15-20-75-14-11-0

##RTC (real time clock) and Temperature Sensor

The RTC is a [Microchip MCP7940N](http://ww1.microchip.com/downloads/en/DeviceDoc/20005010F.pdf) and on our board it is located at 0x6F on i2c-1 when using a 40 pin Raspberry Pi. If you are using this with a 26 pin Raspberry Pi it will be on i2c-0 at the same address but this is a rare use case. The RTC has a wake-on-alarm output which is connected to the pogo pin output (listed above) and this allows you to wake up the Raspberry Pi from a halt state at a specific time and date - the pogo pin interfaces with the run header.

The temperature sensor in use is a [NXP LM75BD](http://www.nxp.com/documents/data_sheet/LM75B.pdf) and this is located at 0x48 on i2c-1 when using a 40 pin Raspberry Pi. If you are using this with a 26 pin Raspberry Pi it will be on i2c-0 at the same address but this is a rare use case.

Both the RTC and temperature sensor have many more features than we have documented. We will not be officially supporting all of these features as they are already well documented in the datasheets and elsewhere. But we have left them available for advanced users.
