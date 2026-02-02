import os
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    print('Missing DISCORD_TOKEN in environment (.env or Secrets).')
    exit(1)

class MyBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Syncing commands globally
        await self.tree.sync()

client = MyBot()

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

@client.tree.command(name="chat", description="Bot sends a message to the current channel")
@app_commands.describe(message="The content to send")
async def chat(interaction: discord.Interaction, message: str):
    if interaction.guild is None:
        await interaction.response.send_message("This command can only be used in a server channel.", ephemeral=True)
        return

    me = interaction.guild.me
    permissions = interaction.channel.permissions_for(me)
    
    if not permissions.send_messages:
        await interaction.response.send_message("Bot does not have permission to send messages in this channel.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)

    try:
        await interaction.channel.send(message)
        await interaction.followup.send("Message sent to channel.")
    except Exception as e:
        print(f"Error sending message: {e}")
        await interaction.followup.send("Failed to send message: error or missing permissions.")

if __name__ == "__main__":
    client.run(TOKEN)
