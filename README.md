# our bot

our bot for our server

## Features

- Clean links: remove tracking and preserve privacy

- Typst: detects and renders Typst expressions in `$$` blocks

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
