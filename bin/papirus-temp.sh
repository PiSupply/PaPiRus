#!/usr/bin/env bash
# read the temperature from the LM75 on the papirus e-ink display HAT
# started 20 mar 2016 wse
#
# get temp word, re-order MSB and LSB, convert to decimal
# set -xv	#also debug
#DEBUG=true	#unset to skip debugging messages
ia=$(echo "ibase=16;$(i2cget -y 1 0x48 0x00 w | sed -e 's/^0x//g' | sed -n 's/\([0-9a-f][0-9a-f]\)\([0-9a-f][0-9a-f]\)/\2\1/p'| tr [[:lower:]] [[:upper:]])" | bc)
[ $DEBUG ] && echo "IA is ${ia}"
# convert that to binary
ib=$(echo "obase=2;$ia" | bc)
[ $DEBUG ] && echo "IB is ${ib}"
# strip last 5 bits
ic="${ib:0:-5}"
[ $DEBUG ] && echo "IC is ${ic}"
# if binary value is 11 bits long, number is negative (twos complement)
if [ $(echo -en "${ic}" | wc -c) -eq 11 ]
then
    [ $DEBUG ] && echo "Temperature is negative"
    ica=$(echo "ibase=2;${ic}" | bc)
    id=$(echo "-2048+${ica}" | bc)
else
    id=$(echo "ibase=2;${ic}" | bc)
fi
[ $DEBUG ] && echo "ID is ${id}"
ie=$(echo "scale=1;(${id}*0.125)*10/10" | bc)
if=$(echo "scale=1;${ie}*1.8+32" | bc)
echo "Temp is ${ie} deg C (${if} deg F)."
papirus-write "Temp is ${ie} deg C (${if} deg F)."