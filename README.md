# Our Bot

A Python Discord bot that processes social media links and typst expressions in messages.

## Features

- **Link Processing**: Automatically converts social media links to embed-friendly formats
  - Instagram → ddinstagram.com
  - Twitter/X → fxtwitter.com/fixupx.com (with privacy alternatives via nitter.net)
  - TikTok → tnktok.com
  - Reddit → rxddit.com (with privacy alternatives via safereddit.com)
  - YouTube → normalized format
  - Bilibili → expanded short links
  - XiaoHongShu (XHS) → expanded and cleaned links
  - Google Maps → expanded and cleaned links

- **typst Detection**: Detects and renders Typst expressions in `$$` blocks

- **Privacy Links**: Some providers offer privacy-preserving alternatives

## Setup

1. Install dependencies using UV:
   ```bash
   uv sync
   ```

2. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and add your Discord bot token:
   ```
   DISCORD_TOKEN=your_discord_bot_token_here
   DISCORD_ACTIVITY_MESSAGE=with links
   ```

4. Run the bot:
   ```bash
   uv run python main.py
   ```

## Development

The bot is structured as follows:

- `main.py` - Main bot file with Discord event handlers
- `config.py` - Configuration management
- `engine.py` - Message processing engine
- `providers/` - Link provider implementations
  - `provider.py` - Abstract base class
  - Individual provider files for each service

## Requirements

- Python 3.13+
- discord.py
- python-dotenv
- requests

## License

MIT License