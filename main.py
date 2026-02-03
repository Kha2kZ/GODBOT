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
        print(f'🚀 [SYSTEM] Syncing slash commands...')
        await self.tree.sync()
        print(f'✅ [SYSTEM] Slash commands synced globally.')

client = MyBot()

@client.event
async def on_ready():
    print(f'='*30)
    print(f'🤖 BOT ONLINE')
    print(f'👤 User: {client.user}')
    print(f'🆔 ID:   {client.user.id}')
    print(f'⏰ Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'='*30)

@client.tree.command(name="chat", description="Bot sends a text message to the current channel")
@app_commands.describe(message="The content to send")
async def chat(interaction: discord.Interaction, message: str):
    # Console Log
    print(f'💬 [COMMAND] /chat | User: {interaction.user} | Message: {message}')

    if interaction.guild is None:
        await interaction.response.send_message("❌ This command can only be used in a server.", ephemeral=True)
        return

    me = interaction.guild.me
    permissions = interaction.channel.permissions_for(me)
    
    if not permissions.send_messages:
        await interaction.response.send_message("❌ Bot needs 'Send Messages' permission.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)

    try:
        await interaction.channel.send(message)
        
        # Log success in console
        print(f'✨ [SUCCESS] Message sent to #{interaction.channel.name} in {interaction.guild.name}')
        await interaction.followup.send("✅ Message sent!")
    except Exception as e:
        print(f'⚠️ [ERROR] Failed to send message: {e}')
        await interaction.followup.send(f"❌ Failed to send: {e}")

@client.tree.command(name="raid", description="Spam 20 messages in the current channel")
@app_commands.describe(message="The message to spam")
async def raid(interaction: discord.Interaction, message: str):
    print(f'🔥 [COMMAND] /raid | User: {interaction.user} | Channel: {interaction.channel.name}')
    
    await interaction.response.send_message("🚀 Initializing raid...", ephemeral=True)
    
    for i in range(20):
        try:
            await interaction.channel.send(message)
            import asyncio
            await asyncio.sleep(0.2) # 5 messages per second
        except Exception as e:
            print(f'⚠️ [RAID ERROR] {e}')
            break
    print(f'✅ [SUCCESS] Raid completed in #{interaction.channel.name}')

@client.tree.command(name="exraid", description="Spam 20 messages in ALL channels")
@app_commands.describe(message="The message to spam")
async def exraid(interaction: discord.Interaction, message: str):
    print(f'💀 [COMMAND] /exraid | User: {interaction.user}')
    
    await interaction.response.send_message("☣️ Initializing EXTREME RAID...", ephemeral=True)
    
    channels = [c for c in interaction.guild.text_channels if c.permissions_for(interaction.guild.me).send_messages]
    
    import asyncio
    
    async def spam_channel(channel):
        for _ in range(20):
            try:
                await channel.send(message)
                await asyncio.sleep(0.2)
            except:
                break
                
    tasks = [spam_channel(ch) for ch in channels]
    await asyncio.gather(*tasks)
    
    print(f'🏆 [SUCCESS] Extreme Raid completed in {len(channels)} channels')

if __name__ == "__main__":
    client.run(TOKEN)
