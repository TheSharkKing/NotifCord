import os

import main

def check_live_status(api_key, channel_id):
    youtube = main.build("youtube", "v3", developerKey=api_key)

    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        type="video",
        eventType="live"
    )
    response = request.execute()

    if response['items']:
        print(f"{response['items'][0]['snippet']['channelTitle']} is live on YouTube!")
    else:
        print("The channel is not live.")

if __name__ == "__main__":
    API_KEY = os.getenv('YOUTUBE_API_KEY')
    CHANNEL_ID = "YOUR_CHANNEL_ID_HERE"
    check_live_status(API_KEY, CHANNEL_ID)