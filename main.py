import discord
from discord.ext import tasks, commands

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
GUILD_ID = 'YOUR_GUILD_ID'
CHANNEL_ID = 'YOUR_CHANNEL_ID'
USER_ID = 'STREAMING_USER_ID'
STREAMING_PLATFORM = 'Twitch'  # or any other platform

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

def check_if_user_is_live(user_id):
    # Replace this function with actual API call to check if the user is live
    # For example, you can use Twitch API to check if a user is live on Twitch
    return True  # Placeholder for actual live status

@tasks.loop(minutes=1)
async def check_live_status():
    is_live = check_if_user_is_live(USER_ID)
    if is_live:
        guild = discord.utils.get(bot.guilds, id=int(GUILD_ID))
        channel = discord.utils.get(guild.text_channels, id=int(CHANNEL_ID))
        await channel.send(f"{USER_ID} Has Gone Live On {STREAMING_PLATFORM}")

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    check_live_status.start()

bot.run(TOKEN)