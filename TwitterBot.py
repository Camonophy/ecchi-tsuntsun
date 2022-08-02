import os
import time
import tweepy

# Get credentials
TOKEN = os.getenv("BOT_TOKEN")
auth = tweepy.OAuthHandler(os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_SECRET"))
auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))
api = tweepy.API(auth)
os.system("mkdir Source")

while(1):
    text = ""
    source = ""
    with open("Source/0/Desc.txt", 'r') as file:
        source = file.readline()
        text += file.read()

    try:        # Tweet jpg
        media = api.update_status_with_media("{}\n\nSource: {}".format(text, source), "Source/0/Img.jpg")
    except:     # Tweet png
        media = api.update_status_with_media("{}\n\nSource: {}".format(text, source), "Source/0/Img.png")

    os.system("rm -rf Source/0")    # Remove first directory
    tweetQueue = os.listdir("Source")
    tweetQueue.sort()

    # Rearrange prepared tweets
    for tweet in tweetQueue:
        os.system("mv Source/{} Source/{}".format(tweet, int(tweet)-1))

    time.sleep(43200)               # Next tweet in 12h
