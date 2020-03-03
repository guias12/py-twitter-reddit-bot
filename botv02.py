import requests
import json
import time
import urllib
import os

import glob
from TwitterAPI import TwitterAPI
from random import randint
from dotenv import load_dotenv

load_dotenv()

last_id = None
twitter = TwitterAPI(consumer_key = os.getenv("TW_CONSUMER_KEY"),
                      consumer_secret = os.getenv("TW_CONSUMER_SECRET"),
                      access_token_key = os.getenv("TW_ACCESS_TOKEN"),
                      access_token_secret = os.getenv("TW_ACCESS_TOKEN_SECRET")
                    )

def make_request():
    r = requests.get('https://www.reddit.com/r/Blessed_Images.json', headers = {'User-agent': 'reddit-twitter-bot1'})
    return r    

def get_reddit_image():
    global last_id

    r = make_request()

    if r.status_code == 200:
        result = r.json()
        posts = result['data']['children']
        post = get_new_post(posts)        

        last_id = post['data']['id']
        return post['data']['url']

def get_new_post(posts):
    global last_id

    for post in posts[1:]:
        if post['data']['id'] != last_id:
            return post

def save_image(img_url):
    files = glob.glob('./img/*')
    for f in files:
        os.remove(f)

    img_dir = "./img/00000001.jpg"
    urllib.request.urlretrieve(img_url, img_dir)
    return img_dir

def make_tweet(img_dir):
    global twitter

    random_number = randint(0, 9999)
    tweet_message = 'blessed image {}'.format(random_number)

    file = open(img_dir, 'rb')
    data = file.read()
    r = twitter.request('statuses/update_with_media', {'status': tweet_message}, {'media[]':data})
    print(r.status_code)

def main():    
    while True:
        img_url = get_reddit_image()
        img_dir = save_image(img_url)
        make_tweet(img_dir)

        time.sleep(7200)

if __name__ == "__main__":
    main()