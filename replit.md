# GODBOT - Discord Bot

## Overview
A Discord bot built with discord.js v14 that provides a `/chat` slash command allowing users to send messages through the bot.

## Project Structure
- `index.js` - Main bot code with slash command registration and handling
- `package.json` - Node.js dependencies
- `.env` - Environment variables (contains DISCORD_TOKEN)

## Setup
1. Add your Discord bot token as the `DISCORD_TOKEN` secret
2. Run the "Discord Bot" workflow

## Features
- `/chat message:<text>` - Bot sends the specified message in the current channel
- Auto-registers slash commands for all guilds the bot joins

## Dependencies
- discord.js v14.14.0
- dotenv
- @discordjs/rest
- discord-api-types

## Running
The bot runs via `npm start` which executes `node index.js`
