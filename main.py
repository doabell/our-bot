"""
Discord bot that processes links and typst in messages
"""

import discord
from config import DISCORD_TOKEN, ACTIVITY
from engine import process_message, format_message
import logging
from dotenv import load_dotenv
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# Set up Discord intents
intents = discord.Intents.default()
intents.message_content = True


class RickRollRedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header("Location", RICK_ROLL_URL)
        self.end_headers()


def run_redirect_server():
    server_address = ("", 8080)
    httpd = HTTPServer(server_address, RickRollRedirectHandler)
    logging.info(
        f"Redirect server running on port 8080, redirecting to {RICK_ROLL_URL}"
    )
    httpd.serve_forever()


# Set up logging
load_dotenv()
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
RICK_ROLL_URL = os.getenv(
    "RICK_ROLL_URL", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
)

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

# Create Discord client
client = discord.Client(intents=intents, activity=ACTIVITY)


@client.event
async def on_ready():
    """Handle bot ready event"""
    if client.user:
        logging.info(f"Successfully logged in as: {client.user} (ID: {client.user.id})")
    else:
        logging.warning("Successfully logged in, but client.user is None.")
    logging.info(
        f"Connected to {len(client.guilds)} guild{'s' if len(client.guilds) != 1 else ''}."
    )
    for guild in client.guilds:
        logging.info(
            f"- Guild: {guild.name} (ID: {guild.id}), Members: {guild.member_count}, Channels: {len(guild.channels)}"
        )
    logging.info(
        f"Tracking a total of {len(client.users)} unique user{'s' if len(client.users) != 1 else ''} across all guilds."
    )
    logging.info(
        f"Total text channels: {sum(1 for guild in client.guilds for channel in guild.channels if getattr(channel, 'type', None) == discord.ChannelType.text)}"
    )
    logging.info(
        f"Total voice channels: {sum(1 for guild in client.guilds for channel in guild.channels if getattr(channel, 'type', None) == discord.ChannelType.voice)}"
    )
    logging.info(f"Bot latency: {round(client.latency * 1000)} ms")


@client.event
async def on_guild_join(guild):
    """Handle joining a new guild"""
    logging.info(f"Joined guild {guild.name} ({guild.id})")


@client.event
async def on_guild_remove(guild):
    """Handle leaving a guild"""
    logging.info(f"Left the guild {guild.name} ({guild.id})")


@client.event
async def on_message(message):
    """Handle message events"""
    # Ignore messages from bots
    if message.author.bot:
        return

    # Process the message content
    results = await process_message(message.content)

    # Find the first provider for the first link (if any)
    provider = None
    links = []
    words = message.content.split()
    for word in words:
        if word.startswith("http://") or word.startswith("https://"):
            if word.startswith("http://"):
                word = "https://" + word[7:]
            links.append(word)
    for link in links:
        for p in __import__("providers").__dict__.values():
            if hasattr(p, "has_link") and callable(getattr(p, "has_link")):
                try:
                    if p().has_link(link):
                        provider = p()
                        break
                except Exception:
                    pass
        if provider:
            break

    delete_original = (
        getattr(provider, "delete_original", "never") if provider else "never"
    )

    # Helper: check if message is link-only
    def is_link_only():
        # Only one link, and nothing else (except whitespace)
        return len(links) == 1 and message.content.strip() == links[0]

    if results:
        try:
            # Calculate should_delete as a single boolean
            should_delete = (
                client.user
                and message.author.id != client.user.id
                and (
                    delete_original == "always"
                    or (delete_original == "link-only" and is_link_only())
                )
            )

            for result in results:
                if result.type == "math" and result.file and result.filename:
                    # Handle math file upload
                    result.file.seek(0)  # Reset file pointer
                    file = discord.File(result.file, result.filename)

                    if should_delete:
                        await message.delete()
                        await message.channel.send(file=file)
                    else:
                        # Try to suppress embeds on the original message
                        try:
                            await message.edit(suppress=True)
                        except (discord.Forbidden, discord.HTTPException):
                            pass
                        await message.reply(file=file, mention_author=False)
                elif result.type == "link":
                    # Handle text content (links)
                    content = format_message(result)
                    if should_delete:
                        await message.delete()
                        await message.channel.send(f"**{message.author.display_name}**\n{content}")
                    else:
                        # Try to suppress embeds on the original message
                        try:
                            await message.edit(suppress=True)
                        except (discord.Forbidden, discord.HTTPException):
                            pass
                        await message.reply(content=content, mention_author=False)
        except Exception as error:
            logging.error(f"Error responding to message: {error}")


if __name__ == "__main__":
    if not DISCORD_TOKEN:
        logging.error("DISCORD_TOKEN environment variable is required")
        exit(1)

    # Start redirect server in a separate thread
    threading.Thread(target=run_redirect_server, daemon=True).start()

    client.run(DISCORD_TOKEN)
