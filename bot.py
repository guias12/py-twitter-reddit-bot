import praw
import json
import requests
from TwitterAPI import TwitterAPI
import urllib
import os
import glob
from random import randint
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(client_id = os.getenv("RE_APP_ID"),
                     client_secret = os.getenv("RE_API_SECRET"),
                     user_agent = 'reddit-twitter-bot1',
                     password = os.getenv("RE_PASSWORD"),
                     username = os.getenv("RE_USERNAME")
                    )

twitter = TwitterAPI(consumer_key = os.getenv("TW_CONSUMER_KEY"),
                      consumer_secret = os.getenv("TW_CONSUMER_SECRET"),
                      access_token_key = os.getenv("TW_ACCESS_TOKEN"),
                      access_token_secret = os.getenv("TW_ACCESS_TOKEN_SECRET")
                    )

subreddit = reddit.subreddit('blessedimages')

newPost = subreddit.new(limit=1)

for submission in newPost:
	if submission.url is not None:
		urlImagem = submission.url

files = glob.glob('./img/*')
for f in files:
    os.remove(f)


imgDir = "./img/00000001.jpg"
urllib.request.urlretrieve(urlImagem, imgDir)

randomNumber = randint(0, 9999)
statusMessage = 'blessed image ' + str(randomNumber)

file = open(imgDir, 'rb')
data = file.read()
r = twitter.request('statuses/update_with_media', {'status': statusMessage}, {'media[]':data})
print(r.status_code)