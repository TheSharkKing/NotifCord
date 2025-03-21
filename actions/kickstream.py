import main
import time

KICK_API_URL = "https://api.kick.com/v1/channels/"
CHANNEL_NAME = "your_channel_name"
CHECK_INTERVAL = 60  # in seconds

def is_live(channel_name):
    response = main.get(f"{KICK_API_URL}{channel_name}")
    if response.status_code == 200:
        data = response.json()
        return data['is_live']
    return False

def announce_live(channel_name):
    print(f"{channel_name} is now live on Kick!")

def main():
    was_live = False
    while True:
        try:
            currently_live = is_live(CHANNEL_NAME)
            if currently_live and not was_live:
                announce_live(CHANNEL_NAME)
            was_live = currently_live
        except Exception as e:
            print(f"Error checking live status: {e}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()