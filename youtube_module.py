from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()


YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


def extract_username(url):
    return url.split("@")[-1].strip("/")


def get_channel_id(username):
    request = youtube.search().list(
        q=username,
        part="snippet",
        type="channel",
        maxResults=5
    )
    
    response = request.execute()

    for item in response["items"]:
        title = item["snippet"]["title"].lower().replace(" ", "")
        uname = username.lower().replace(" ", "")

        if uname in title:
            return item["id"]["channelId"]

    return response["items"][0]["id"]["channelId"]


def get_videos(channel_id):
    channel_data = youtube.channels().list(
        id=channel_id,
        part="contentDetails"
    ).execute()

    playlist_id = channel_data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    videos_data = youtube.playlistItems().list(
        playlistId=playlist_id,
        part="snippet",
        maxResults=10
    ).execute()

    videos = []

    for item in videos_data["items"]:
        videos.append({
            "title": item["snippet"]["title"],
            "link": f"https://www.youtube.com/watch?v={item['snippet']['resourceId']['videoId']}",
            "time": item["snippet"]["publishedAt"]
        })

    return videos