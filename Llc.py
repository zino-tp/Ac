import discord
from discord.ext import commands
import asyncio

# Bot-Token eingeben
TOKEN = input("Bitte gib deinen Discord Bot Token ein: ")

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot ist eingeloggt als {bot.user.name}')

@bot.command()
async def create_channels(ctx, num_channels: int, name_prefix: str, num_messages: int, *, message_content: str):
    guild = ctx.guild

    if not guild:
        await ctx.send("Dieser Befehl kann nur in einem Server verwendet werden.")
        return

    # Channels erstellen
    for i in range(1, num_channels + 1):
        channel_name = f"{name_prefix}{i}"
        await guild.create_text_channel(channel_name)
        print(f'Channel {channel_name} erstellt.')
        
        # Nachrichten senden
        channel = discord.utils.get(guild.text_channels, name=channel_name)
        if channel:
            for _ in range(num_messages):
                await channel.send(message_content)
                await asyncio.sleep(1)  # Ein kleines Intervall zwischen den Nachrichten
            print(f'Nachrichten an Channel {channel_name} gesendet.')

    await ctx.send(f'{num_channels} Channels erstellt und Nachrichten gesendet.')

# Bot starten
bot.run(TOKEN)
