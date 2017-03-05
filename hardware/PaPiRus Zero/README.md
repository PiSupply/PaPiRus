#PaPiRus Zero additional details
##Pinout for buttons 

The schematic labels switches SW1 to SW5 as well as the signal lines to those buttons (signals are labeled BUT1 to BUT5) but confusingly the signals to specific switches do not maintain the same number as the switch.

Below is a clarification to make this a little less confusing:
```
SW1 = BUT5 = pin 40 = GPIO 21

SW2 = BUT4 = pin 36 = GPIO 16

SW3 = BUT1 = pin 38 = GPIO 20

SW4 = BUT3 = pin 35 = GPIO 19

SW5 = BUT2 = pin 37 = GPIO 26
```
Also see the schematic area this refers to here - https://github.com/PiSupply/PaPiRus/blob/master/hardware/PaPiRus%20Zero/button-schematic.jpg

##Jumper settings and meaning
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
CN10  Raspberry Pi pin 13
CN11  Raspberry Pi pin 7
CN12  Raspberry Pi pin 15
CN15  Raspberry Pi pin 32
CN17  Raspberry Pi pin 29
```
##Temperature Sensor

The temperature sensor in use is a [NXP LM75BD](http://www.nxp.com/documents/data_sheet/LM75B.pdf) and this is located at 0x48 on i2c-1 when using a 40 pin Raspberry Pi. If you are using this with a 26 pin Raspberry Pi it will be on i2c-0 at the same address but this is a rare use case.

The temperature sensor has many more features than we have documented. We will not be officially supporting all of these features as they are already well documented in the datasheets and elsewhere. But we have left them available for advanced users.
