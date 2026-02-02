# GODBOT - Python Discord Bot

This is a **Discord Utility Bot** designed to facilitate messaging via slash commands. Based on its structure, it's likely a **Community Engagement Bot** or a **Moderator Utility** that allows users (or staff) to post formatted messages (Embeds) through the bot identity.

## 🚀 Features
- **Slash Commands**: Modern `/chat` command for interaction.
- **Embed Logging**: Beautifully formatted Discord Embeds for messages.
- **Activity Logs**: Detailed console output tracking command usage and errors.
- **Auto-Sync**: Automatically registers commands on startup.

## 🛠 Setup & Installation

### 1. Requirements
- Python 3.10+
- `discord.py`
- `python-dotenv`

### 2. Configuration
Create a **Secret** or `.env` file with your bot token:
```env
DISCORD_TOKEN=your_token_here
```

### 3. Permissions
Ensure the bot has the following permissions in your Discord Server:
- `Send Messages`
- `Embed Links`
- `Use Slash Commands`

### 4. Running the Bot
```bash
python main.py
```

## 📜 Commands
| Command | Description |
| --- | --- |
| `/chat <message>` | Sends a formatted Embed with your message to the channel. |

---
*Created with Replit Agent*
