# RTC GPIO

This demo shows the 3 different output modes for the MFP (Multi Function Pin) of the MCP7940N hardware clock:
- Alarm output from the two independent alarm clocks.
- Square wave output of various frequencies (the program only uses the lowest one: 1 Hz).
- Direct programming of the MFP output.

Remember that the circuit on the PaPiRus only generates a pulse on GPIO 27 on a high to low transition
of the MFP output.

Also this program relies on the smbusf module (See [py_smbusf](../py-smbusf) for build and installation instructions).

## Alarm output

We set the two alarms 10 seconds apart and wait for them to trigger.
Only one alarm can be enabled at the same time. The first alarm is enabled.
When the first alarm triggers, we disable it and enable the second alarm.
See the datasheet, section 5.5 for details.

## Square wave output

A square wave can be output of 1 Hz, 4096 kHz, 8192 kHz and 32768 kHz.
The demo uses the 1 Hz output becuase we want to show the individual interrupts on the Papirus display.

## Direct programming

The demo generates 5 interrupts 1 second apart followed by 5 interrupts 2 seconds apart.
