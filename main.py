import os
import sqlite3
import json
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from utils import registercommands  # Import our command registrar

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_TOKEN not found in the .env file.")

# Set up bot intents (we need guild intents to track guild membership)
intents = discord.Intents.default()
intents.guilds = True

# Create the bot instance (a command prefix is still required even if using slash commands)
bot = commands.Bot(command_prefix="!", intents=intents)

# SQLite database file name
DATABASE = "guild_data.db"

def init_db():
    """Initialize the SQLite database with a table for guild data."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS guilds (
            guild_id INTEGER PRIMARY KEY,
            guild_data TEXT
        )
    """)
    conn.commit()
    conn.close()

async def update_guilds_in_db():
    """
    Update the local database:
      - Insert any new guilds (with default empty JSON data).
      - Remove guilds that the bot is no longer in.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Insert new guilds currently joined by the bot
    for guild in bot.guilds:
        cursor.execute("SELECT guild_id FROM guilds WHERE guild_id = ?", (guild.id,))
        result = cursor.fetchone()
        if not result:
            default_data = json.dumps({})  # Default guild-specific data as an empty dict
            cursor.execute("INSERT INTO guilds (guild_id, guild_data) VALUES (?, ?)", (guild.id, default_data))
            print(f"Added guild {guild.id} to the database.")
    
    # Remove guilds that the bot is no longer in
    cursor.execute("SELECT guild_id FROM guilds")
    db_guilds = {row[0] for row in cursor.fetchall()}
    current_guilds = {guild.id for guild in bot.guilds}
    for guild_id in db_guilds - current_guilds:
        cursor.execute("DELETE FROM guilds WHERE guild_id = ?", (guild_id,))
        print(f"Removed guild {guild_id} from the database.")
    
    conn.commit()
    conn.close()

@tasks.loop(minutes=5)
async def scheduled_db_update():
    """Periodically update the guilds stored in the database."""
    await update_guilds_in_db()

@bot.event
async def on_ready():
    """Event handler for when the bot is ready."""
    print(f"{bot.user} is now online!")
    # Initialize and update the database on boot
    init_db()
    await update_guilds_in_db()
    scheduled_db_update.start()
    
    # Dynamically load and register slash commands from utils/commands/
    registercommands.register_commands(bot)
    
    # Sync slash commands globally
    await bot.tree.sync()
    print("Slash commands have been synced.")

@bot.event
async def on_guild_join(guild):
    """When the bot joins a new guild, add it to the database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    default_data = json.dumps({})
    cursor.execute("INSERT OR IGNORE INTO guilds (guild_id, guild_data) VALUES (?, ?)", (guild.id, default_data))
    conn.commit()
    conn.close()
    print(f"Joined new guild: {guild.id}")

@bot.event
async def on_guild_remove(guild):
    """When the bot is removed from a guild, remove it from the database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM guilds WHERE guild_id = ?", (guild.id,))
    conn.commit()
    conn.close()
    print(f"Removed from guild: {guild.id}")

# Run the bot
bot.run(TOKEN)
