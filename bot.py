import tweepy
import time
import os
import requests
import json
from nums import *
from PIL import Image


#imported all the access tokens, if you want to make your own you need to generate them

def retrieve_last_seen_id(file_name):
    fr = open(file_name, 'r')
    lsi = int(fr.read().strip())
    fr.close()
    return lsi

def store_last_seen_id(lsi, file_name):
    fw = open(file_name, 'w')
    fw.write(str(lsi))
    fw.close()
    return



auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def reply_to_tweet():
    print('Responding to tweets...')
    lsi = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(lsi, tweet_mode='extended')


    for mention in reversed(mentions):
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        # m = mention._json
        # api.update_status('@' + mention.user.screen_name + 'Hi!', mention.id)
        print(last_seen_id)
        if 'media' in mention.entities:

            link = mention.entities['media'][0]['media_url']
            print(link)
            response = requests.get(link)

            file = open("image.png", "wb")
            file.write(response.content)
            file.close()

            img = Image.open('image.png').convert('L')
            img.save('grayscale.png')

            message = "Here's your grayscale image! "
            api.update_with_media('grayscale.png', '@' + mention.user.screen_name + ' ' + message, in_reply_to_status_id = mention.id, auto_populate_reply_metadata=True)


while True:
    reply_to_tweet()
    time.sleep(15)
