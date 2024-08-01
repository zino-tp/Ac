import os
import random
import requests
from loguru import logger
from datetime import datetime
import time

# Einstellungen
website_url = "https://auth.roblox.com/v2/signup"
webhook_url = input("Enter your Discord webhook URL: ")

# Hardcodierter reCAPTCHA-Token
recaptcha_token = '5b2b525eab950b60e998fad423915543'

def get_xsrf_token(session):
    response = session.post("https://auth.roblox.com/v2/login", headers={"X-CSRF-TOKEN": ""})
    xsrf_token = response.headers.get('x-csrf-token')
    if xsrf_token:
        logger.debug(f'csrf-token: {xsrf_token}')
        return xsrf_token
    else:
        logger.error("Failed to fetch X-Csrf-Token")
        return None

def get_field_data(session, csrf_token):
    headers = {
        'authority': 'auth.roblox.com',
        'x-csrf-token': csrf_token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'content-type': 'application/json;charset=UTF-8',
        'accept': 'application/json, text/plain, */*',
    }
    response = session.post('https://auth.roblox.com/v2/signup', headers=headers, json={})
    if response.ok:
        return response.json()["failureDetails"][0]["fieldData"]
    else:
        logger.error(f"Failed to get field data: {response.text}")
        return None

def create_account(session, username, password):
    csrf_token = get_xsrf_token(session)
    if not csrf_token:
        logger.error("Failed to get X-Csrf-Token")
        return None

    field_data = get_field_data(session, csrf_token)
    if not field_data:
        logger.error("Failed to get field data")
        return None

    # Integrieren Sie den reCAPTCHA-Token hier
    captcha_token = recaptcha_token  # Verwenden Sie den bereitgestellten Token

    birthday = generate_birthday()
    registration_payload = {
        "username": username,
        "password": password,
        "birthday": birthday,
        "gender": random.choice(["male", "female"]),
        "captchaToken": captcha_token,
    }

    headers = {
        'authority': 'auth.roblox.com',
        'x-csrf-token': csrf_token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'content-type': 'application/json;charset=UTF-8',
        'accept': 'application/json, text/plain, */*',
    }
    response = session.post('https://auth.roblox.com/v2/signup', headers=headers, json=registration_payload)
    if response.ok:
        logger.success("Account created successfully")
        return {"username": username, "password": password, "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    else:
        logger.error(f"Failed to create account: {response.text}")
        return None

def generate_birthday():
    day = str(random.randint(1, 25))
    month = 'Mar'
    year = str(random.randint(1980, 2006))
    return f"{day} {month} {year}"

def send_to_discord(filename, webhook_url):
    with open(filename, 'rb') as file:
        response = requests.post(
            webhook_url,
            files={'file': (filename, file)}
        )
    if response.status_code == 200:
        logger.success("File sent to Discord webhook successfully")
    else:
        logger.error(f"Failed to send file to Discord webhook: {response.status_code}")

def main():
    num_accounts = int(input("How many accounts do you want to generate (1-10000)? "))
    session = requests.Session()
    accounts = []

    for _ in range(num_accounts):
        username = f"user_{random.randint(1000, 9999)}"
        password = f"pass_{random.randint(1000, 9999)}"
        account = create_account(session, username, password)
        if account:
            accounts.append(account)
        time.sleep(5)  # Wartezeit auf 5 Sekunden erhöht

    if accounts:  # Überprüfen, ob tatsächlich Accounts generiert wurden
        filename = 'acc.txt'
        with open(filename, 'w') as file:
            for account in accounts:
                file.write(f"_______________\n")
                file.write(f"Username: {account['username']}\n")
                file.write(f"Password: {account['password']}\n")
                file.write(f"Date: {account['date']}\n")
                file.write(f"________________\n")

        send_to_discord(filename, webhook_url)
    else:
        logger.error("No accounts were generated.")

if __name__ == "__main__":
    main()
