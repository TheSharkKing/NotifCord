import main
import json
import time

# Replace with your YouTube API key
API_KEY = 'YOUR_YOUTUBE_API_KEY'
# Replace with the channel ID of the user you want to monitor
CHANNEL_ID = 'TARGET_CHANNEL_ID'
# Replace with the interval (in seconds) at which you want to check for new videos
CHECK_INTERVAL = 300

def get_latest_video(channel_id):
    url = f'https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={channel_id}&part=snippet,id&order=date&maxResults=1'
    response = main.get(url)
    data = response.json()
    if 'items' in data and len(data['items']) > 0:
        return data['items'][0]
    return None

def send_notification(video):
    title = video['snippet']['title']
    video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
    print(f"New video posted: {title}\nWatch it here: {video_url}")

def main():
    last_video_id = None
    while True:
        latest_video = get_latest_video(CHANNEL_ID)
        if latest_video:
            video_id = latest_video['id']['videoId']
            if video_id != last_video_id:
                send_notification(latest_video)
                last_video_id = video_id
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()