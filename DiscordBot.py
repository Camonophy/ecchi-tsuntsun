import os
import discord
from WebHandler import getYandere
from YoutubeManager import update, check
from Follower import handleFollowerList, follow

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
        os.system("rm run hold")
        super().__init__()

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        # Get attachment
        elif message.attachments:
            try:    # Download attachment from message url
                url = str(message.attachments).split('=')[3].split('\'')[1]
                dataFormat = url.split('.')[-1]
                if dataFormat in ["png", "jpg"]:
                    os.system("rm Img*")
                    os.system("wget {} -O Img.{}".format(url, dataFormat))
                    self.gotImage = True
                elif dataFormat == "py":
                    file = url.split("/")[-1]
                    os.system("rm {}".format(file))
                    os.system("wget {}".format(url))
                await message.channel.send("Got the file!")
            except:
                await message.channel.send("Did not get the file!")

        # Get source
        elif message.content.startswith("http"):
            if "yande.re" in message.content:
                self.text, self.img = getYandere(message.content)

                if not self.text:
                    self.gotText = False
                    await message.channel.send("Could not retrieve any character!")
                else:
                    self.gotText = True

                if not self.img:
                    self.gotImage = False
                    await message.channel.send("Could not retrieve any image!")
                else:
                    self.gotImage = True

                self.source = message.content
                self.gotSource = True
            else:
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
        elif message.content.startswith("$uy"):
            await message.channel.send("Updating your local playlist...")
            update()
            await message.channel.send("Updated your Youtube-Playlist!")

        # Update Follower text file
        elif message.content.startswith("$uf"):
            await message.channel.send("Updating your local follower list...")
            handleFollowerList()
            await message.channel.send("Updated your follower list!")

	# Start follow process
        elif message.content.startswith("$sf"):
            if os.path.exists("run"):
                await message.channel.send("I'm already following new users!")
            else:
                await message.channel.send("I'll start following new users now!")
                os.system("touch run")
                t = threading.Thread(target=follow)
                t.start()

	# Hold follow process
        elif message.content.startswith("$hf"):
            if os.path.exists("run"):
                await message.channel.send("I'll stop following new users!")
                os.system("touch hold")
            else:
                await message.channel.send("I'm not following new users atm!")

        # Check how many Tweets are remaining and what scripts are available
        elif message.content.startswith("$s"):
            tweets = len(os.listdir("Source"))
            await message.channel.send("There are {} Tweets remaining!".format(str(tweets)))

            files = os.listdir(".")
            scripts = [x for x in files if ".py" in x]
            if scripts:
                await message.channel.send("Scripts available: " + " , ".join(scripts))
            else:
                await message.channel.send("There are no scripts available!")

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

        # Edit autostart scripts
        elif message.content.startswith("$inject"):
            scripts = str(message.content).split(" ")[1:]
            os.system("cp .bashrc newbash")
            with open("newbash", 'a') as file:
                file.write("\n")
                for script in scripts:
                    file.write("nohup python3 {}.py & \n".format(script))
            os.system("cp newbash ~/.bashrc")
            await message.channel.send("Autostart scripts changed!")

        # Reboot to take changes into effect
        elif message.content.startswith("$r"):
            await message.channel.send("See you soon...hopefully!!")
            os.system("rm run hold")
            os.system("sudo reboot")

        # Get the next Follower
        elif message.content.startswith("$f"):
            with open("Follower.txt", 'r') as file:
                fol = file.readline()
                await message.channel.send("The next follower is {}".format(fol))

        # Get help response
        elif message.content.startswith("$h"):
            helpText =  "[Post image]\t     = Prepare an image for a Tweet \n" \
                        "[Post script]\t    = Add a new script to the collection \n" \
                        "[Post link]\t      = Prepare source link for a Tweet \n" \
                        "[€...]\t           = Prepare text for a Tweet \n" \
                        "[$c]\t             = Check your Youtube playlist \n" \
                        "[$uy]\t            = Update your Youtube playlist \n" \
                        "[$st]\t            = Get how many prepared Tweets remaining \n" \
                        "[$r]\t             = Reboot \n" \
                        "[$f]\t             = Get the next user to follow and how many remain \n" \
                        "[$uf]\t            = Update the follower list \n" \
                        "[$sf]\t            = Start follow process \n" \
                        "[$hf]\t            = Hold follow process \n" \
                        "[$inject(...)]\t   = Edit autostart scripts \n" \
                        "[$g(x)]\t          = Get description of local Tweet x \n" \
                        "[$d(x)]\t          = Delete local Tweet x"
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

# ID: 1005092786837663846
