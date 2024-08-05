import requests

def send_discord_message(webhook_url, message, count):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "content": message
    }
    
    for _ in range(count):
        response = requests.post(webhook_url, json=data, headers=headers)
        if response.status_code == 204:
            print("Nachricht erfolgreich gesendet.")
        else:
            print(f"Fehler beim Senden der Nachricht: {response.status_code} - {response.text}")

def main():
    webhook_url = input("Gib den Webhook-URL ein: ").strip()
    message = input("Gib die Nachricht ein: ").strip()
    try:
        count = int(input("Wie viele Nachrichten möchtest du senden? ").strip())
        if count <= 0:
            raise ValueError("Die Anzahl der Nachrichten muss eine positive Zahl sein.")
    except ValueError as ve:
        print(f"Ungültige Eingabe für die Anzahl der Nachrichten: {ve}")
        return

    send_discord_message(webhook_url, message, count)

if __name__ == "__main__":
    main()
