import os
import random
import requests
from loguru import logger
from anticaptchaofficial.funcaptchaproxyless import funcaptchaProxyless
from datetime import datetime
import time

website_url = "https://auth.roblox.com/v2/signup"

def get_xsrf_token(session):
    try:
        response = session.post("https://auth.roblox.com/v2/login", headers={"X-CSRF-TOKEN": ""})
        response.raise_for_status()
        xsrf_token = response.headers.get('x-csrf-token')
        if xsrf_token:
            logger.debug(f'csrf-token: {xsrf_token}')
            return xsrf_token
        else:
            logger.error("Failed to fetch X-Csrf-Token")
            return None
    except requests.RequestException as e:
        logger.error(f"Request failed while getting X-Csrf-Token: {e}")
        return None

def get_field_data(session, csrf_token):
    headers = {
        'authority': 'auth.roblox.com',
        'x-csrf-token': csrf_token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'content-type': 'application/json;charset=UTF-8',
        'accept': 'application/json, text/plain, */*',
    }
    try:
        response = session.post('https://auth.roblox.com/v2/signup', headers=headers, json={})
        response.raise_for_status()
        return response.json()["failureDetails"][0]["fieldData"]
    except requests.RequestException as e:
        logger.error(f"Request failed while getting field data: {e}")
        return None

def parse_field_data(field_data):
    captcha_id, blob = field_data.split(',')
    return {'captcha_id': captcha_id, 'captcha_blob': blob}

def solve_captcha(blob_value):
    api_key = os.getenv('anticaptcha_api_key')
    if not api_key:
        logger.error("Anti-captcha API key is not set")
        return None

    solver = funcaptchaProxyless()
    solver.set_key(api_key)
    solver.set_website_url(website_url)
    try:
        website_key = requests.get("https://apis.rbxcdn.com/captcha/v1/metadata").json()["funCaptchaPublicKeys"]['ACTION_TYPE_WEB_SIGNUP']
        solver.set_website_key(website_key)
        solver.set_data_blob(str({"blob": blob_value}))

        captcha_response = solver.solve_and_return_solution()
        if captcha_response != 0:
            logger.success(f"Successful CAPTCHA response: {captcha_response}")
            return captcha_response
        else:
            logger.error(f"Failed CAPTCHA: {solver.error_code}")
            return None
    except requests.RequestException as e:
        logger.error(f"Request failed while solving CAPTCHA: {e}")
        return None

def generate_birthday():
    day = str(random.randint(1, 25))
    month = 'Mar'
    year = str(random.randint(1980, 2006))
    return f"{day} {month} {year}"

def create_account(session, username, password):
    csrf_token = get_xsrf_token(session)
    if not csrf_token:
        logger.error("Failed to get X-Csrf-Token")
        return None

    field_data = get_field_data(session, csrf_token)
    if not field_data:
        logger.error("Failed to get field data")
        return None

    captcha_data = parse_field_data(field_data)
    captcha_token = solve_captcha(captcha_data['captcha_blob'])
    if not captcha_token:
        logger.error("Failed to solve CAPTCHA")
        return None

    birthday = generate_birthday()
    registration_payload = {
        "username": username,
        "password": password,
        "birthday": birthday,
        "gender": 1,
        "isTosAgreementBoxChecked": True,
        "context": "MultiverseSignupForm",
        "referralData": None,
        "captchaId": captcha_data['captcha_id'],
        "captchaToken": captcha_token,
        "captchaProvider": "PROVIDER_ARKOSE_LABS",
        "agreementIds": [
            "848d8d8f-0e33-4176-bcd9-aa4e22ae7905",
            "54d8a8f0-d9c8-4cf3-bd26-0cbf8af0bba3"
        ]
    }

    headers = {
        'x-csrf-token': csrf_token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'content-type': 'application/json;charset=UTF-8',
        'accept': 'application/json, text/plain, */*',
    }

    try:
        response = session.post(website_url, json=registration_payload, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Registration request failed: {e}")
        return None

    if response.ok:
        logger.success('Successful Registration!')
        return username, password, birthday, response.cookies
    else:
        logger.error('Failed Registration!')
        logger.debug(f"Response headers: {response.headers}")
        logger.debug(f"Response text: {response.text}")
        logger.debug(f"Status code: {response.status_code}")
        return None

def save_and_send_file(webhook_url, account_info_list):
    file_path = 'acc.txt'
    with open(file_path, 'w') as file:
        for account_info in account_info_list:
            file.write(account_info + '\n')

    try:
        with open(file_path, 'rb') as file:
            response = requests.post(webhook_url, files={'file': file})
            response.raise_for_status()
            if response.status_code == 204:
                logger.success("File sent to Discord webhook successfully")
            else:
                logger.error(f"Unexpected response from Discord webhook: {response.status_code}")
    except requests.RequestException as e:
        logger.error(f"Failed to send file to Discord webhook: {e}")

def main():
    webhook_url = input("Enter your Discord webhook URL: ")
    num_accounts = int(input("How many accounts do you want to generate (1-10000)? "))
    if not (1 <= num_accounts <= 10000):
        logger.error("Number of accounts must be between 1 and 10000")
        return

    account_info_list = []
    with requests.Session() as session:
        for _ in range(num_accounts):
            username = f"user{random.randint(10000, 99999)}"
            password = f"pass{random.randint(10000, 99999)}"
            account = create_account(session, username, password)
            if account:
                username, password, birthday, _ = account
                date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                account_info = f"Username: {username}\nPassword: {password}\nDate: {date_created}\n"
                account_info_list.append(account_info)
                time.sleep(2)  # Increase sleep to avoid rate limiting

    save_and_send_file(webhook_url, account_info_list)

if __name__ == "__main__":
    main()
