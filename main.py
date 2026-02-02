import os
import discord
from discord import app_commands
from discord import Embed
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    print('[-] CRITICAL: Missing DISCORD_TOKEN in environment.')
    exit(1)

class MyBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        # Enable message content if you want to log message text from others (requires toggle in dev portal)
        # intents.message_content = True 
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        print(f'[+] Syncing slash commands...')
        await self.tree.sync()
        print(f'[+] Slash commands synced globally.')

client = MyBot()

@client.event
async def on_ready():
    print(f'='*30)
    print(f'BOT ONLINE')
    print(f'User: {client.user}')
    print(f'ID:   {client.user.id}')
    print(f'Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'='*30)

@client.tree.command(name="chat", description="Bot sends an embed message to the current channel")
@app_commands.describe(message="The content to send")
async def chat(interaction: discord.Interaction, message: str):
    # Console Log
    print(f'[COMMAND] /chat | User: {interaction.user} | Message: {message}')

    if interaction.guild is None:
        await interaction.response.send_message("❌ This command can only be used in a server.", ephemeral=True)
        return

    me = interaction.guild.me
    permissions = interaction.channel.permissions_for(me)
    
    if not permissions.send_messages or not permissions.embed_links:
        await interaction.response.send_message("❌ Bot needs 'Send Messages' and 'Embed Links' permissions.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)

    try:
        # Create an attractive Embed
        embed = Embed(
            description=message,
            color=0x00ff00, # Green
            timestamp=datetime.now()
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.set_footer(text=f"Sent via GODBOT")

        await interaction.channel.send(embed=embed)
        
        # Log success in console
        print(f'[SUCCESS] Embed sent to #{interaction.channel.name} in {interaction.guild.name}')
        await interaction.followup.send("✅ Embed message sent!")
    except Exception as e:
        print(f'[ERROR] Failed to send embed: {e}')
        await interaction.followup.send(f"❌ Failed to send: {e}")

if __name__ == "__main__":
    client.run(TOKEN)
