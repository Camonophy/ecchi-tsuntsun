import os
import time
import tweepy
import random
from JSONLoader import getJSONFile

def unfollow():
    # Get credentials
    TOKEN = os.getenv("BOT_TOKEN")
    auth = tweepy.OAuthHandler(os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_SECRET"))
    auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))
    api = tweepy.API(auth)

    with open("Follower.txt", 'r') as file:
        lines = file.read().split("\n")
        while 1:
            for user in lines:
                wait = random.randint(600, 1800)
                if api.get_status(user):
                    pass

def follow():
    # Get credentials
    TOKEN = os.getenv("BOT_TOKEN")
    auth = tweepy.OAuthHandler(os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_SECRET"))
    auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))
    api = tweepy.API(auth)
    usernames = []
    print("Start")

    with open("Follower.txt", 'r') as file:
        usernames = file.read().split("\n")

        while usernames:
            with open("Follower.txt", 'w') as file:
                user = usernames.pop(0)
                wait = random.randint(300, 900)
                try:
                    api.create_friendship(screen_name=user)
                    print("Added {}".format(user))
                except:
                    print("Failed")
                    wait = 100

                file.write("\n".join(usernames))
                time.sleep(wait)

    def createList():
        index = 1
        follower = []

        while 1:
            os.system("wget https://www.letsallfollowback.com/?p={} -O html.txt".format(index))
            html = ""

            with open("html.txt", 'r') as file:
                html = file.read().split("\n")

            potentialFollower = []

            for line in html:
                if "BLANK" in line and "retweet" not in line:
                    potentialFollower.append(line.split(">")[1].split("<")[0])

            potentialFollower.remove("--")

            if len(potentialFollower) < 10:
                break
            else:
                index += 1
                follower += potentialFollower

        os.system("touch Follower.txt")
        with open("Follower.txt", 'w') as file:
            for f in follower:
                file.write(f + "\n")
        os.system("cp Follower.txt FollowerVanilla.txt")

    def updateList():
        index = 1
        updatedContent = ""
        follower = []
        prevPotentialFollower = []

        # Get current potential follower from the website
        while 1:
            os.system("wget https://www.letsallfollowback.com/?p={} -O html.txt".format(index))
            html = ""

            with open("html.txt", 'r') as file:
                html = file.read().split("\n")

            potentialFollower = []

            for line in html:
                if "BLANK" in line and "retweet" not in line:
                    potentialFollower.append(line.split(">")[1].split("<")[0])

            potentialFollower.remove("--")

            if len(potentialFollower) < 10:
                break
            else:
                index += 1
                follower += potentialFollower

        # Load the previous potential follower list
        try:
            with open("FollowerVanilla.txt", 'r') as file:
                prevPotentialFollower = file.read().split("\n")
        except:
            pass

        print(len(prevPotentialFollower))
        print(len(follower))

        # Romove any duplicate
        follower = filter(lambda i: i not in prevPotentialFollower, follower)
        print(list(follower))

        try:
            with open("Follower.txt", "r") as file:
                updatedContent = file.read()
        except:
            pass

        updatedContent = "\n".join(follower) + "\n" + updatedContent

        # Set the newly generated Follower file as the new Vanilla file
        with open("Follower.txt", "w") as file:
            file.write(updatedContent)
        os.system("cp Follower.txt FollowerVanilla.txt")

'''
# Get credentials
twitterData = getJSONFile("TwitterKeys.json")
auth = tweepy.OAuthHandler(twitterData["CONSUMER_KEY"], twitterData["CONSUMER_SECRET"])
auth.set_access_token(twitterData["ACCESS_TOKEN"], twitterData["ACCESS_TOKEN_SECRET"])
api = tweepy.API(auth)

u = str(api.get_followers()[0]).split("_json=")[1].split(", protected")[0]
u = u.replace('\'', "\"")
#k = json.loads(u)
print(u)

c = input("c ; f ; u")

if c == "c":
    createList()
elif c == "f":
    follow()
else:
    unfollow() 
'''

follow()