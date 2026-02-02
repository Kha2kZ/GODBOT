# GODBOT - Discord Bot (Python)

## Overview
A Discord bot built with `discord.py` that provides a `/chat` slash command allowing users to send messages through the bot.

## Project Structure
- `main.py` - Main bot code with slash command registration and handling
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (contains DISCORD_TOKEN)

## Setup
1. Add your Discord bot token as the `DISCORD_TOKEN` secret
2. Run the "Discord Bot" workflow

## Features
- `/chat message:<text>` - Bot sends the specified message in the current channel
- Uses global slash command registration

## Dependencies
- discord.py
- python-dotenv

## Running
The bot runs via `python main.py`
