import main
import time

# Replace these with your actual Twitch API credentials
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
ACCESS_TOKEN = 'your_access_token'
CHANNEL_NAME = 'your_channel_name'

def get_stream_status():
    url = f'https://api.twitch.tv/helix/streams?user_login={CHANNEL_NAME}'
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    response = main.get(url, headers=headers)
    data = response.json()
    if data['data']:
        return True
    return False

def announce_stream():
    print(f'{CHANNEL_NAME} is now live on Twitch!')

def main():
    was_live = False
    while True:
        is_live = get_stream_status()
        if is_live and not was_live:
            announce_stream()
            was_live = True
        elif not is_live:
            was_live = False
        time.sleep(60)  # Check every 60 seconds

if __name__ == '__main__':
    main()