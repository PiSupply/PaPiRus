# !/usr/bin/env python
# coding: utf-8
# ------------------------------------------------------
# Filename papirus-twitter.py
# ------------------------------------------------------
# Displays Tweets on PaPiRus Zero display
#
# v1.0 by James West June 2016
# 
# I used the Twython tutorials at tecoed.co.uk
# to get me started
# ------------------------------------------------------

# import libraries to make it work
import os
import re
import time
import RPi.GPIO as GPIO
from twython import Twython
from papirus import Papirus
from papirus import PapirusText

# set up PaPiRus
screen = Papirus()
text = PapirusText()

# Twitter authorisation keys - add your own here
CONSUMER_KEY = 'YOUR CONSUMER KEY HERE'
CONSUMER_SECRET = 'YOUR CONSUMER SECRET HERE'
ACCESS_KEY = 'YOUR ACCESS KEY HERE'
ACCESS_SECRET = 'YOUR ACCESS SECRET HERE'

api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

# Identifies the GPIOs that the buttons operate on
SW1 = 26
SW2 = 19
SW3 = 20
SW4 = 16
SW5 = 21

def main():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(SW1, GPIO.IN)
    GPIO.setup(SW2, GPIO.IN)
    GPIO.setup(SW3, GPIO.IN)
    GPIO.setup(SW4, GPIO.IN)
    GPIO.setup(SW5, GPIO.IN)

# Writes the menu to the PaPiRus - 14 is the font size
    text.write('1 = News\n2 = Weather\n3 = My timeline\n4 = My mentions\n5 = Off', 14)
    while True:
        if GPIO.input(SW1) == False:

# Put the Twitter usernames of the news organisations you want to read here
            twits = ["BBCNews", "GranadaReports", "SkyNews", "itvnews", "MENnewsdesk"]
            for index in range (len(twits)):
            
# The count parameter defines how many tweets from each account you'll read            
                tweets = api.get_user_timeline(screen_name=twits[index], count=4)
                for tweet in tweets:
                    clean_tweet = '%s: %s' % (      tweet['user']['screen_name'].encode('utf-8'),
                                                        tweet['text'].encode('utf-8'))

# These lines clear URLs from the tweets and tidies up other elements the display
# doesn't seem to like
                    clean_tweet = re.sub(r"(https?\://|http?\://|https?\:)\S+", "", clean_tweet)
                    clean_tweet = re.sub(r"&amp;", "&", clean_tweet)
                    clean_tweet = re.sub(r"&horbar|&hyphen|&mdash|&ndash", "-", clean_tweet)
                    clean_tweet = re.sub(r"&apos|&rsquo|&rsquor|&prime", "'", clean_tweet)
                    clean_tweet = re.sub(r"£", "", clean_tweet)

                    text.write(clean_tweet, 14)

# Sets how many seconds each tweet is on screen for
                    time.sleep(5)

            text.write('1 = News\n2 = Weather\n3 = My timeline\n4 = My mentions\n5 = Off', 14)

        if GPIO.input(SW2) == False:
# usernames of the weather accounts you'll be using        
            twitweather = ["mcrweather", "Manches_Weather"]
            for index in range (len(twitweather)):
                tweets = api.get_user_timeline(screen_name=twitweather[index], count=1)
                for tweet in tweets:
                    clean_tweet = '%s: %s' % (      tweet['user']['screen_name'].encode('utf-8'),
                                                        tweet['text'].encode('utf-8'))

                    clean_tweet = re.sub(r"(https?\://|http?\://)\S+", "", clean_tweet)
                    clean_tweet = re.sub(r"&amp;", "&", clean_tweet)
                    clean_tweet = re.sub(r"&horbar|&hyphen|&mdash|&ndash", "-", clean_tweet)
                    clean_tweet = re.sub(r"&apos|&rsquo|&rsquor|&prime", "'", clean_tweet)
                    clean_tweet = re.sub(r"£", "", clean_tweet)
                    text.write(clean_tweet, 14)
                    time.sleep(8)

            text.write('1 = News\n2 = Weather\n3 = My timeline\n4 = My mentions\n5 = Off', 14)

        if GPIO.input(SW3) == False:
# Gets your home timeline
            tweets = api.get_home_timeline(screen_name='jameswest', count=20)
            for tweet in tweets:
                clean_tweet = '%s: %s' % (      tweet['user']['screen_name'].encode('utf-8'),
                                                        tweet['text'].encode('utf-8'))

                clean_tweet = re.sub(r"(https?\://|http?\://)\S+", "", clean_tweet)
                clean_tweet = re.sub(r"&amp;", "&", clean_tweet)
                clean_tweet = re.sub(r"&horbar|&hyphen|&mdash|&ndash", "-", clean_tweet)
                clean_tweey = re.sub(r"&apos|&rsquo|&rsquor|&prime", "'", clean_tweet)
                clean_tweet = re.sub(r"£", "", clean_tweet)
                text.write(clean_tweet, 14)
                time.sleep(5)

            text.write('1 = News\n2 = Weather\n3 = My timeline\n4 = My mentions\n5 = Off', 14)

        if GPIO.input(SW4) == False:
# gets your mentions
            tweets = api.get_mentions_timeline(screen_name='jameswest', count=5)
            for tweet in tweets:
                clean_tweet = '%s: %s' % (      tweet['user']['screen_name'].encode('utf-8'),
                                                        tweet['text'].encode('utf-8'))

                clean_tweet = re.sub(r"(https?\://|http?\://)\S+", "", clean_tweet)
                clean_tweet = re.sub(r"&amp;", "&", clean_tweet)
                clean_tweet = re.sub(r"&horbar|&hyphen|&mdash|&ndash", "-", clean_tweet)
                clean_tweey = re.sub(r"&apos|&rsquo|&rsquor|&prime", "'", clean_tweet)
                clean_tweet = re.sub(r"£", "", clean_tweet)
                text.write(clean_tweet, 14)
                time.sleep(5)

            text.write('1 = News\n2 Weather\n3 = My timeline\n4 = My mentions\n5 = Off', 14)

        if GPIO.input(SW5) == False:
# Says goodbye, clears the screen and shuts the Pi down
            text.write('Goodbye...')
            text.write(' ')
            os.system("sudo shutdown -h now")

if __name__ == '__main__':
    main()
