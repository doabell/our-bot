import os
from dotenv import load_dotenv
import discord

# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_ACTIVITY_MESSAGE = os.getenv("DISCORD_ACTIVITY_MESSAGE", "with links")

# Discord activity configuration
ACTIVITY = discord.Activity(
    type=discord.ActivityType.watching, name=DISCORD_ACTIVITY_MESSAGE
)
