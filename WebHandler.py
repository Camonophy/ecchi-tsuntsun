import os

def getYandere(url):
    os.system("wget {} -O index.txt".format(url))
    image = ""
    characterList = []

    try:
        imageLine = ""
        imageText = ""
        gotImage = False
        gotText = False
        with open("index.txt", 'r') as file:
            for line in file.readlines():
                if ".jpg" in line and not gotImage:
                    imageLine = line
                    gotImage = True

                if "\"tags\":{" in line and not gotText:
                    imageText = line.replace("\"", "")
                    gotText = True

                if gotText and gotImage:
                    break

        # Create tuple list of tags and categories
        text = [(x.split(":")[1], x.split(":")[0]) for x in imageText.split("tags:{")[1].split("}")[0].split(",")]
        for category, tag in text:
            if category == 'character':
                tag = [x.capitalize() for x in tag.split("_")]
                characterList.append(" ".join(tag))
        text = "Character: " + ", ".join(characterList)
        image = "https:" + imageLine.split("https:")[1].split(".jpg")[0] + ".jpg"

    except:
        pass

    return text, image