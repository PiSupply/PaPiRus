import sys
import twitter
import RPi.GPIO as GPIO
from time import sleep
from papirus import Papirus
from papirus import PapirusText
from papirus import PapirusTextPos

api = twitter.Api()

SW1 = 16
SW2 = 26
SW3 = 20
SW4 = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(SW1, GPIO.IN)
GPIO.setup(SW2, GPIO.IN)
GPIO.setup(SW3, GPIO.IN)
GPIO.setup(SW4, GPIO.IN)

# Populate your twitter API details below, replacing
# CONSUMER_KEY_HERE etc with your details from Twitter
consumer_key = '*******************'
consumer_secret = '*******************'
access_token_key = '********************'
access_token_secret = '*******************'

api = twitter.Api(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token_key=access_token_key,
    access_token_secret=access_token_secret
)
tweet_index = 0
text = PapirusTextPos(False, rotation=0)
statuses = api.GetHomeTimeline(count=20)


def home_timeline(Home):
    name = statuses[tweet_index].user.screen_name
    status = statuses[tweet_index].text
    return status, name;


def next_tweet():
    status, name = home_timeline(sys.argv[1] if len(sys.argv) > 1 else 0)
    twitter_name = "@" + name

    text.UpdateText("start", twitter_name)
    text.UpdateText("tweet", status)
    text.WriteAll()


# Display first tweet
status, name = home_timeline(sys.argv[1] if len(sys.argv) > 1 else 0)
twitter_name = "@" + name

text.AddText(twitter_name, 0, 0, Id="start")
text.AddText(status, 0, 20, Id="tweet")
text.WriteAll()

while True:
    if (GPIO.input(SW1) is False) and (GPIO.input(SW2) is False):
        write_text(papirus, "Exiting ...", EPD_SIZE)
        sleep(0.2)
        papirus.clear()
        sys.exit()

    if GPIO.input(SW4) is False and tweet_index < 19:
            tweet_index = tweet_index + 1
            next_tweet()
    if GPIO.input(SW3) is False and tweet_index > 0:
            tweet_index = tweet_index - 1
            next_tweet()
    if GPIO.input(SW1) is False:
            statuses = api.GetHomeTimeline(count=20)
            tweet_index = 0
            next_tweet()
    sleep(0.1)
