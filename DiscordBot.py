import os
import discord
from YoutubeManager import update, check

os.system("mkdir Source")
TOKEN = os.getenv("BOT_TOKEN")

class Bot(discord.Client):

    def __init__(self):
        self.source = ""
        self.gotSource = False
        self.text = ""
        self.gotText = False
        self.img = 0
        self.gotImage = False
        super().__init__()

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        # Get image
        elif message.attachments:
            try:    # Download image from message url
                url = str(message.attachments).split('=')[3].split('>')[0].replace('\'', '')
                dataFormat = url.split('.')[len(url.split('.')) - 1]
                os.system("rm Img*")
                os.system("wget {} -O Img.{}".format(url, ["png", "jpg"][dataFormat == "jpg"]))
                self.gotImage = True
                await message.channel.send("Got the image!")
            except:
                await message.channel.send("Did not get the image!")

        # Get source
        elif message.content.startswith("http"):
            self.source = message.content
            self.gotSource = True
            await message.channel.send("Got the source!")

        # Get text
        elif message.content.startswith("€"):
            self.text = message.content[1:len(message.content)]
            self.gotText = True
            await message.channel.send("Got the text!")

        # Check Youtube playlist
        elif message.content.startswith("$c"):
            await message.channel.send("Let's see...")
            (local, remote) = check()

            if len(local) > 0:
                await message.channel.send("New tracks:")
                localList = ""
                for entry in local:
                    localList += "{}".format(entry)
                await message.channel.send(localList + "\n")

            if len(remote) > 0:
                await message.channel.send("Missing tracks:")
                remoteList = ""
                for entry in remote:
                    remoteList += "{}".format(entry)
                await message.channel.send(remoteList)

            if len(local) + len(remote) == 0:
                await message.channel.send("Everything is up-to-date!")

        # Update Youtube playlist
        elif message.content.startswith("$u"):
            await message.channel.send("Updating your local playlist...")
            update()
            await message.channel.send("Updated your Youtube-Playlist!")

        # Check how many Tweets are remaining
        elif message.content.startswith("$s"):
            tweets = len(os.listdir("Source"))
            await message.channel.send("There are {} Tweets remaining!".format(str(tweets)))

        # Get description of a Tweet
        elif message.content.startswith("$g"):
            getNum = int(message.content[2:len(message.content)])
            try:
                with open("Source/{}/Desc.txt".format(str(getNum)), 'r') as file:
                    source = file.readline()
                    text = file.read()
                    await message.channel.send("Source: {}\n{}".format(source, text))
            except:
                await message.channel.send("Local tweet number {} was not found!".format(str(getNum)))

        # Delete one local tweet entry
        elif message.content.startswith("$d"):
            deleteNum = message.content[2:len(message.content)]
            try:
                os.system("rm -rf Source/{}".format(deleteNum))  # Remove first directory
                tweetQueue = os.listdir("Source")
                tweetQueue.sort()
                tweetQueue = filter(lambda x: x > deleteNum, tweetQueue)

                # Rearrange prepared tweets
                for tweet in tweetQueue:
                    os.system("mv Source/{} Source/{}".format(tweet, int(tweet) - 1))
                await message.channel.send("Local Tweet number {} deleted!".format(deleteNum))
            except:
                await message.channel.send("Local Tweet number {} was not found!".format(deleteNum))

        # Get help response
        elif message.content.startswith("$h"):
            helpText =  "[Post image]\t = Prepare an image for a Tweet \n" \
                        "[Post Link]\t  = Prepare source link for a Tweet \n" \
                        "[€...]\t       = Prepare text for a Tweet \n" \
                        "[$c]\t         = Check your Youtube playlist \n" \
                        "[$u]\t         = Update your Youtube playlist \n" \
                        "[$s]\t         = Get how many prepared Tweets remaining \n" \
                        "[$g(x)]\t      = Get description of local Tweet x \n" \
                        "[$d(x)]\t      = Delete local Tweet x"
            await message.channel.send(helpText)

        else:
            pass

        # Set up a Tweet when all conditions are met
        if self.gotImage and self.gotText and self.gotSource:
            index = len(os.listdir("Source"))
            os.system("mkdir Source/{}".format(str(index)))
            os.system("mv Img* Source/{}".format(str(index)))
            with open("Source/{}/Desc.txt".format(str(index)), "w") as descr:
                descr.write("{}\n{}".format(self.source, self.text))
            await message.channel.send("Tweet data {} created!".format(str(index)))
            self.gotImage = False
            self.gotSource = False
            self.gotText = False

b = Bot()
b.run(TOKEN)
