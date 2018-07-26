#!/usr/bin/bash

rm -R /home/"$SUDO_USER"/PaPiRus
rm /usr/local/bin/papirus*
cd /usr/local/bitmaps
for del in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
do
rm $del.gif
done
rm papirus*
rm python.png



