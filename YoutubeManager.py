from googleapiclient.discovery import build


def update():
    processed  = 0
    youtube    = build("youtube", "v3", developerKey=os.getenv("API_KEY"))
    me         = youtube.channels().list(id=os.getenv("CHANNEL_ID"), part="contentDetails").execute()

    video_list     = youtube.playlistItems().list(playlistId=os.getenv("PLAYLIST_ID"), part="snippet", maxResults=50).execute()

    with open("YoutubePlaylist.txt", "w") as file:
        while 1:
            
            for video in (video_list["items"]):
                title = video["snippet"]["title"]
                print(title)
                if title in ["Deleted video", "Private video"]:
                    continue
                file.write(title + "\n")
                processed += 1
            
            try:
                nextPage = video_list["nextPageToken"]
                video_list = youtube.playlistItems().list(playlistId=os.getenv("PLAYLIST_ID"), part="snippet",pageToken=nextPage, maxResults=50).execute()
            
            except:
                break
        

def check():
    client = getJSONFile("Client.json")
    processed  = 0
    missing_local  = 0
    missing_online = 0

    youtube    = build("youtube", "v3", developerKey=os.getenv("API_KEY"))
    me         = youtube.channels().list(id=os.getenv("CHANNEL_ID"), part="contentDetails").execute()
    video_list     = youtube.playlistItems().list(playlistId=os.getenv("PLAYLIST_ID"), part="snippet", maxResults=50).execute()

    file_content   = load_file("YoutubePlaylist.txt")
    online_content = load_videos(video_list["items"])
    local_missing_content  = []
    online_missing_content = []

    while 1:
        try:
            online_content_length = len(online_content)
            file_content_length   = len(file_content)

            video_name = online_content.pop(0)
            file_content.remove(video_name)
        
        except:
            if(online_content_length != 0):
                local_missing_content.append(video_name)
                missing_online += 1
            
            else:     
                try: 
                    nextPage       = video_list["nextPageToken"]
                    video_list = youtube.playlistItems().list(playlistId=client["playlist_ID"], part="snippet", maxResults=50).execute()
                    online_content = load_videos(video_list["items"])
                
                except:
                    if(file_content_length + online_content_length == 0):
                        break
                    
                    else:
                        for entry in file_content:
                            online_missing_content.append(entry)
                            missing_local += 1
                        file_content.clear()

        processed += 1

    return (local_missing_content, online_missing_content)


def load_videos(videos):
    content = []
    for video in videos:
        title = video["snippet"]["title"]
        if title not in ["Deleted video", "Private video"]:
            content.append(title + "\n")
    return content


def load_file(file_name):
    file_content = []
    with open(file_name) as local_file:
        for line in local_file.readlines():
            file_content.append(line)
    return file_content

