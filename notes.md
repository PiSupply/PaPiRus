```
RTC  NXP 8523T

pi@glooston ~ $ hwclock -r
hwclock: Cannot access the Hardware Clock via any known method.
hwclock: Use the --debug option to see the details of our search for an access method.
pi@glooston ~ $ i2cdetect -q 1
Error: Could not open file `/dev/i2c-1': Permission denied
Run as root?
pi@glooston ~ $ sudo i2cdetect -q 1
WARNING! This program can confuse your I2C bus, cause data loss and worse!
I will probe file /dev/i2c-1 using quick write commands.
I will probe address range 0x03-0x77.
Continue? [Y/n] y
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- 68 -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
pi@glooston ~ $ sudo modprobe rtc-pcf8523
pi@glooston ~ $ lsmod
Module                  Size  Used by
rtc_pcf8523             3601  0
i2c_dev                 6709  0
snd_bcm2835            21149  0
snd_pcm                90778  1 snd_bcm2835
snd_seq                61097  0
snd_seq_device          7209  1 snd_seq
snd_timer              23007  2 snd_pcm,snd_seq
snd                    66325  5 snd_bcm2835,snd_timer,snd_pcm,snd_seq,snd_seq_device
brcmfmac              189269  0
brcmutil                7856  1 brcmfmac
cfg80211              462846  1 brcmfmac
rfkill                 22347  2 cfg80211
i2c_bcm2708             6200  0
spi_bcm2708             6018  0
uio_pdrv_genirq         3666  0
uio                     9897  1 uio_pdrv_genirq
pi@glooston ~ $ sudo -s
root@glooston:/home/pi# echo pcf8523 0x68 > /sys/class/i2c-adapter/i2c-1/new_device
root@glooston:/home/pi# hwclock -r
Fri 24 Jul 2015 10:38:53 EDT  -0.678161 seconds
root@glooston:/home/pi# exit
pi@glooston ~ $ hwclock -r
hwclock: Cannot access the Hardware Clock via any known method.
hwclock: Use the --debug option to see the details of our search for an access method.
pi@glooston ~ $ sudo hwclock -r
Fri 24 Jul 2015 10:39:21 EDT  -0.059050 seconds
pi@glooston ~ $
```


NXP LM75BD Temperature sensor
http://www.nxp.com/documents/data_sheet/LM75B.pdf
It is supposed to be on I2C at an address somewhere in 0x48 thru 0x4F range but my particular PCB revision either I am doing something wrong or the LM75BD doesn't work. I have v1.4 rev of the PCB the KS people will be getting v1.5 rev so will leave it alone until 1.5's are out in the wild.

buttons gpio.25,27,28,29 (physical pins 36,37,38,40)
