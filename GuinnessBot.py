import os
import sys
import re
import time
import random
import threading
import hashlib
import json
from urllib.parse import urlencode
from http import cookiejar

import requests
from console.utils import set_title
from urllib3.exceptions import InsecureRequestWarning
from pystyle import Colorate, Colors, Write

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class BlockCookies(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

class Gorgon:
    def __init__(self, params: str, data: str, cookies: str, unix: int):
        self.unix = unix
        self.params = params
        self.data = data
        self.cookies = cookies

    def hash(self, data: str) -> str:
        try:
            _hash = str(hashlib.md5(data.encode()).hexdigest())
        except Exception:
            _hash = str(hashlib.md5(data).hexdigest())
        return _hash

    def get_base_string(self) -> str:
        base_str = self.hash(self.params)
        base_str = base_str + self.hash(self.data) if self.data else base_str + str('0'*32)
        base_str = base_str + self.hash(self.cookies) if self.cookies else base_str + str('0'*32)
        return base_str

    def get_value(self) -> json:
        base_str = self.get_base_string()
        return self.encrypt(base_str)

    def encrypt(self, data: str) -> json:
        unix = self.unix
        length = 20
        key = [223, 119, 185, 64, 185, 155, 132, 131, 209, 185, 203, 209, 247, 194, 185, 133, 195, 208, 251, 195]
        param_list = []

        for i in range(0, 12, 4):
            temp = data[8 * i:8 * (i + 1)]
            for j in range(4):
                H = int(temp[j * 2:(j + 1) * 2], 16)
                param_list.append(H)

        param_list.extend([0, 6, 11, 28])
        H = int(hex(unix), 16)
        param_list.append((H & 4278190080) >> 24)
        param_list.append((H & 16711680) >> 16)
        param_list.append((H & 65280) >> 8)
        param_list.append((H & 255) >> 0)
        eor_result_list = []

        for (A, B) in zip(param_list, key):
            eor_result_list.append(A ^ B)

        for i in range(length):
            C = self.reverse(eor_result_list[i])
            D = eor_result_list[(i + 1) % length]
            E = C ^ D
            F = self.rbit_algorithm(E)
            H = (F ^ 4294967295 ^ length) & 255
            eor_result_list[i] = H

        result = ''
        for param in eor_result_list:
            result += self.hex_string(param)

        return {'X-Gorgon': '0404b0d30000' + result, 'X-Khronos': str(unix)}

    def rbit_algorithm(self, num):
        result = ''
        tmp_string = bin(num)[2:]
        while len(tmp_string) < 8:
            tmp_string = '0' + tmp_string
        for i in range(0, 8):
            result = result + tmp_string[7 - i]
        return int(result, 2)

    def hex_string(self, num):
        tmp_string = hex(num)[2:]
        if len(tmp_string) < 2:
            tmp_string = '0' + tmp_string
        return tmp_string

    def reverse(self, num):
        tmp_string = self.hex_string(num)
        return int(tmp_string[1:] + tmp_string[:1], 16)


def send(device_id, install_id, cdid, openudid, aweme_id, proxies, config):
    global reqs, _lock, success, fails, rps, rpm
    for x in range(10):
        try:
            version = random.choice(__versions)
            params = urlencode(
                {
                    "os_api": "25",
                    "device_type": random.choice(__devices),
                    "ssmix": "a",
                    "manifest_version_code": version,
                    "dpi": "240",
                    "region": "VN",
                    "carrier_region": "VN",
                    "app_name": "musically_go",
                    "version_name": "27.2.4",
                    "timezone_offset": "-28800",
                    "ab_version": "27.2.4",
                    "ac2": "wifi",
                    "ac": "wifi",
                    "app_type": "normal",
                    "channel": "googleplay",
                    "update_version_code": version,
                    "device_platform": "android",
                    "iid": install_id,
                    "build_number": "27.2.4",
                    "locale": "vi",
                    "op_region": "VN",
                    "version_code": version,
                    "timezone_name": "Asia/Ho_Chi_Minh",
                    "device_id": device_id,
                    "sys_region": "VN",
                    "app_language": "vi",
                    "resolution": "720*1280",
                    "device_brand": "samsung",
                    "language": "vi",
                    "os_version": "7.1.2",
                    "aid": "1340"
                }
            )
            payload = f"item_id={aweme_id}&play_delta=1"
            sig = Gorgon(params=params, cookies=None, data=None, unix=int(time.time())).get_value()

            proxy = random.choice(proxies) if config['proxy']['use-proxy'] else ""

            response = requests.post(
                url=(
                    "https://"
                    + random.choice(__domains) +
                    "/aweme/v1/aweme/stats/?" + params
                ),
                data=payload,
                headers={'cookie': 'sessionid=90c38a59d8076ea0fbc01c8643efbe47',
                         'x-gorgon': sig['X-Gorgon'], 'x-khronos': sig['X-Khronos'], 'user-agent': 'okhttp/3.10.0.1'},
                verify=False,
                proxies={"http": proxy_format + proxy, "https": proxy_format + proxy} if
                config['proxy']['use-proxy'] else {}
            )
            reqs += 1
            try:
                if response.json()['status_code'] == 0:
                    with _lock:
                        print(
                            Colorate.Horizontal(
                                Colors.purple_to_red,
                                f'TikTok Viewbot by HN TOOL^| success: {success} fails: {fails} reqs: {reqs} rps: {rps} rpm: {rpm}'
                            )
                        )
                    success += 1
            except:
                fails += 1
                continue

        except Exception as e:
            pass


def rpsm_loop():
    global rps, rpm
    while True:
        initial = reqs
        time.sleep(1.5)
        rps = round((reqs - initial) / 1.5, 1)
        rpm = round(rps * 60, 1)


def fetch_proxies():
    url_list = [
        "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxy-list/data.txt",
        "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks5.txt"
    ]
    for url in url_list:
        response = requests.get(
            url=url
        )
        if response.ok:
            with open("proxies.txt", "a+") as f:
                f.write(response.text)
        else:
            pass


def adjust_threading():
    global thread_count
    max_threads = threading.active_count()
    print(f"\nCurrent max thread count: {max_threads}")
    thread_count = int(input("Enter the new thread count (e.g., 20): "))
    if thread_count > max_threads:
        print(f"New thread count exceeds maximum allowed. Setting thread count to {max_threads}.")
        thread_count = max_threads


def adjust_speed():
    global sleep_time
    sleep_time = float(input("\nEnter the new sleep time between requests (in seconds, e.g., 0.5): "))


def adjust_processes():
    global process_count
    process_count = int(input("\nEnter the new process count (e.g., 2): "))


def adjust_proxy_settings():
    global proxy_format, proxies
    use_proxy = input("\nUse proxy? (y/n): ").lower()
    if use_proxy == "y":
        proxy_type = input("Enter proxy type (http/https/socks4/socks5): ").lower()
        credential = input("Enter proxy credentials (if any, format: username:password): ")
        auth = True if credential else False
        proxy_format = f'{proxy_type}://' + f'{credential}@' if auth else ''
        proxies = []
        proxy_file = input("Enter the path to the proxy file (e.g., proxies.txt): ")
        with open(proxy_file, 'r') as f:
            proxies = f.read().splitlines()
        print("Proxy settings updated successfully.")
    else:
        proxy_format = ''
        proxies = []
        print("Proxy settings cleared.")

import time
import os
from colorama import Fore, Back, Style, init

# Initialize colorama
init()

# Rainbow color codes.
color_list = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]

def print_rainbow_text(text):
    color_index = 0
    for ch in text:
        print(color_list[color_index % len(color_list)] + ch, end='', flush=True)
        color_index += 1
    print(Style.RESET_ALL)

def menu():
    os.system("cls" if os.name == "nt" else "clear")
    txt = """\n\n
    Guinness Like Bot by @guinnessgshep \n"""
    while True:
        print_rainbow_text(txt)
        time.sleep(1)
        os.system("cls" if os.name == "nt" else "clear")
        print("Select an option:")
        print("1. Adjust threading (current: {})".format(thread_count))
        print("2. Adjust speed (current: {})".format(sleep_time))
        print("3. Adjust number of processes (current: {})".format(process_count))
        print("4. Adjust proxy settings")
        print("5. Start viewbot")
        print("6. Quit")


if __name__ == "__main__":
    with open('devices.txt', 'r') as f:
        devices = f.read().splitlines()

    with open('config.json', 'r') as f:
        config = json.load(f)
    if config["proxy"]['proxyscrape']:
        fetch_proxies()
    proxy_format = ''
    proxies = []
    os.system("cls" if os.name == "nt" else "clear")
    set_title("Guinness Like Bot")
    thread_count = 10
    sleep_time = 1.5
    process_count = 1

    while True:
        menu()
        option = input("\nEnter your choice: ")
        if option == "1":
            adjust_threading()
        elif option == "2":
            adjust_speed()
        elif option == "3":
            adjust_processes()
        elif option == "4":
            adjust_proxy_settings()
        elif option == "5":
            break
        elif option == "6":
            sys.exit(0)
        else:
            print("Invalid option. Please try again.")

    _lock = threading.Lock()
    reqs = 0
    success = 0
    fails = 0
    rpm = 0
    rps = 0

    threading.Thread(target=rpsm_loop).start()

    for _ in range(process_count):
        threading.Thread(target=send, args=(random.choice(devices),)).start()

    while True:
        if threading.active_count() > process_count:
            time.sleep(1)
        else:
            print("\nViewbot process completed.")
            break
