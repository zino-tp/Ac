import requests
import threading
import time
import os
from pyfiglet import figlet_format

# Color codes for "hacker-style" terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    title = figlet_format("𝚉𝙸𝙽𝙾", font="big")
    print(f"{Colors.HEADER}{Colors.BOLD}{title}{Colors.ENDC}")

def send_message(webhook_url, content):
    data = {'content': content}
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print(f"{Colors.OKGREEN}Message sent successfully.{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}Error sending message: {response.status_code} - {response.text}{Colors.ENDC}")

def send_messages_parallel(webhook_url, content, count, num_threads):
    def worker():
        for _ in range(count // num_threads):
            send_message(webhook_url, content)
            time.sleep(1)  # Delay to respect rate limits

    thread_list = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()

def get_webhook_info(webhook_url):
    response = requests.get(webhook_url)
    if response.status_code == 200:
        webhook_info = response.json()
        print(f"{Colors.OKBLUE}Webhook Information:{Colors.ENDC}")
        for key, value in webhook_info.items():
            print(f"{Colors.OKBLUE}{key}: {value}{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}Error retrieving webhook info: {response.status_code} - {response.text}{Colors.ENDC}")

def delete_webhook(webhook_url):
    response = requests.delete(webhook_url)
    if response.status_code == 204:
        print(f"{Colors.OKGREEN}Webhook successfully deleted.{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}Error deleting webhook: {response.status_code} - {response.text}{Colors.ENDC}")

def get_server_info(invite_code):
    response = requests.get(f'https://discord.com/api/v10/invites/{invite_code}?with_counts=true')
    if response.status_code == 200:
        server_info = response.json()
        guild = server_info.get('guild', {})
        print(f"{Colors.OKBLUE}Server Information:{Colors.ENDC}")
        print(f"{Colors.OKBLUE}ID: {guild.get('id', 'Unavailable')}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Name: {guild.get('name', 'Unavailable')}{Colors.ENDC}")
        icon = guild.get('icon', None)
        if icon:
            print(f"{Colors.OKBLUE}Icon URL: https://cdn.discordapp.com/icons/{guild.get('id')}/{icon}.png{Colors.ENDC}")
        else:
            print(f"{Colors.OKBLUE}Icon URL: Unavailable{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Owner ID: {guild.get('owner_id', 'Unavailable')}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Region: {guild.get('region', 'Unavailable')}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Member Count: {server_info.get('approximate_member_count', 'Unavailable')}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Online Count: {server_info.get('approximate_presence_count', 'Unavailable')}{Colors.ENDC}")
        created_at = guild.get('created_at', 'Unavailable')
        if created_at != 'Unavailable':
            created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(created_at, '%Y-%m-%dT%H:%M:%S.%fZ'))
        print(f"{Colors.OKBLUE}Created At: {created_at}{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}Error retrieving server info: {response.status_code} - {response.text}{Colors.ENDC}")

def get_bot_info(bot_token):
    headers = {
        'Authorization': f'Bot {bot_token}'
    }
    response = requests.get('https://discord.com/api/v10/users/@me', headers=headers)
    if response.status_code == 200:
        bot_info = response.json()
        print(f"{Colors.OKBLUE}Bot Information:{Colors.ENDC}")
        print(f"{Colors.OKBLUE}ID: {bot_info.get('id', 'Unavailable')}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Username: {bot_info.get('username', 'Unavailable')}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Discriminator: {bot_info.get('discriminator', 'Unavailable')}{Colors.ENDC}")
        avatar = bot_info.get('avatar', None)
        if avatar:
            print(f"{Colors.OKBLUE}Avatar URL: https://cdn.discordapp.com/avatars/{bot_info.get('id')}/{avatar}.png{Colors.ENDC}")
        else:
            print(f"{Colors.OKBLUE}Avatar URL: Unavailable{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Bot: {bot_info.get('bot', 'Unavailable')}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Public Flags: {bot_info.get('public_flags', 'Unavailable')}{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}Error retrieving bot info: {response.status_code} - {response.text}{Colors.ENDC}")

def main():
    print_header()
    print(f"{Colors.OKBLUE}1. Send Message{Colors.ENDC}")
    print(f"{Colors.OKBLUE}2. Get Webhook Info{Colors.ENDC}")
    print(f"{Colors.OKBLUE}3. Delete Webhook{Colors.ENDC}")
    print(f"{Colors.OKBLUE}4. Get Server Info{Colors.ENDC}")
    print(f"{Colors.OKBLUE}5. Bot Token Checker{Colors.ENDC}")
    
    choice = input(f"{Colors.BOLD}Select an option (1/2/3/4/5): {Colors.ENDC}")
    
    if choice == '1':
        webhook_url = input(f"{Colors.BOLD}Enter the Webhook URL: {Colors.ENDC}")
        content = input(f"{Colors.BOLD}Enter the message content: {Colors.ENDC}")
        count = int(input(f"{Colors.BOLD}How many messages to send? {Colors.ENDC}"))
        num_threads = int(input(f"{Colors.BOLD}Number of threads to use? {Colors.ENDC}"))
        send_messages_parallel(webhook_url, content, count, num_threads)
    elif choice == '2':
        webhook_url = input(f"{Colors.BOLD}Enter the Webhook URL: {Colors.ENDC}")
        get_webhook_info(webhook_url)
    elif choice == '3':
        webhook_url = input(f"{Colors.BOLD}Enter the Webhook URL: {Colors.ENDC}")
        delete_webhook(webhook_url)
    elif choice == '4':
        invite_code = input(f"{Colors.BOLD}Enter the Server Invite Code: {Colors.ENDC}")
        get_server_info(invite_code)
    elif choice == '5':
        bot_token = input(f"{Colors.BOLD}Enter the Bot Token: {Colors.ENDC}")
        get_bot_info(bot_token)
    else:
        print(f"{Colors.FAIL}Invalid selection.{Colors.ENDC}")

if __name__ == "__main__":
    main()
