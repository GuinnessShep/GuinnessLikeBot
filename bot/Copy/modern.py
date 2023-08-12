import os
import sys
import ssl
import re
import time
import random
import threading
import requests
import hashlib
import json
from urllib.parse import urlencode
from concurrent.futures import ThreadPoolExecutor
from urllib3.exceptions import InsecureRequestWarning
from http import cookiejar
from colorama import init, Fore
from alive_progress import alive_bar
from rich.console import Console
from rich.progress import track

console = Console()

init(autoreset=True)  # Initializes colorama for Windows

class BlockCookies(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

r = requests.Session()
r.cookies.set_policy(BlockCookies())


__domains = ["api22-core-c-useast1a.tiktokv.com",
	     "api19-core-c-useast1a.tiktokv.com",
             "api16-core-c-useast1a.tiktokv.com", 
	     "api21-core-c-useast1a.tiktokv.com",
	     "api16-normal-useast5.us.tiktokv.com",
	    ]

__devices = ["SM-G9900", "SM-A136U1", "SM-M225FV", "SM-E426B", "SM-M526BR", "SM-M326B", 
             "SM-A528B", "SM-F711B", "SM-F926B", "SM-A037G", "SM-A225F", "SM-M325FV", 
             "SM-A226B", "SM-M426B", "SM-A525F", "SM-N976N"]

__versions = ["190303", "190205", "190204", "190103", "180904", "180804", "180803", "180802", "270204"]

class Gorgon:
    def __init__(self, params: str, data: str = None, cookies: str = None) -> None:
        self.params = params
        self.data = data
        self.cookies = cookies

    def _hash(self, data: str) -> str:
        return hashlib.md5(data.encode()).hexdigest()

    def _calc_gorgon(self) -> str:
        gorgon = self._hash(self.params)
        gorgon += self._hash(self.data) if self.data else "0" * 32
        gorgon += self._hash(self.cookies) if self.cookies else "0" * 32
        gorgon += "0" * 32
        return gorgon

    def get_value(self):
        return self._encrypt(self._calc_gorgon())

    def _encrypt(self, data: str) -> dict:
        unix = int(time.time())
        len_key = 0x14
        key = [
            0xDF, 0x77, 0xB9, 0x40, 0xB9, 0x9B, 0x84, 0x83,
            0xD1, 0xB9, 0xCB, 0xD1, 0xF7, 0xC2, 0xB9, 0x85,
            0xC3, 0xD0, 0xFB, 0xC3,
        ]
        param_list = []
        for i in range(0, 12, 4):
            temp = data[8 * i : 8 * (i + 1)]
            for j in range(4):
                H = int(temp[j * 2 : (j + 1) * 2], 16)
                param_list.append(H)
        param_list.extend([0x0, 0x6, 0xB, 0x1C])
        H = int(hex(unix), 16)
        param_list.append((H & 0xFF000000) >> 24)
        param_list.append((H & 0x00FF0000) >> 16)
        param_list.append((H & 0x0000FF00) >> 8)
        param_list.append((H & 0x000000FF) >> 0)
        eor_result_list = []
        for A, B in zip(param_list, key):
            eor_result_list.append(A ^ B)
        for i in range(len_key):
            C = self._reverse(eor_result_list[i])
            D = eor_result_list[(i + 1) % len_key]
            E = C ^ D
            F = self._rbit(E)
            H = ((F ^ 0xFFFFFFFF) ^ len_key) & 0xFF
            eor_result_list[i] = H
        result = "".join([self._hex_string(param) for param in eor_result_list])
        return {"X-Gorgon": ("0404b0d30000" + result), "X-Khronos": str(unix)}

    def _rbit(self, num):
        result = "".join(reversed(bin(num)[2:].zfill(8)))
        return int(result, 2)

    def _hex_string(self, num):
        return hex(num)[2:].zfill(2)

    def _reverse(self, num):
        tmp_string = self._hex_string(num)
        return int(tmp_string[1:] + tmp_string[:1], 16)

def send(__device_id, __install_id, cdid, openudid):
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
                                    "iid": __install_id,
                                    "build_number": "27.2.4",
                                    "locale": "vi",
                                    "op_region": "VN",
                                    "version_code": version,
                                    "timezone_name": "Asia/Ho_Chi_Minh",
                                    "device_id": __device_id,
                                    "sys_region": "VN",
                                    "app_language": "vi",
                                    "resolution": "720*1280",
                                    "device_brand": "samsung",
                                    "language": "vi",
                                    "os_version": "7.1.2",
                                    "aid": "1340"
                                }
        )
            payload = f"item_id={__aweme_id}&play_delta=1"
            sig = Gorgon(params=params, cookies=None, data=None, unix=int(time.time())).get_value()

            proxy = random.choice(proxies) if config['proxy']['use-proxy'] else ""

            response = r.post(
                url=(
                    "https://"
                    + random.choice(__domains) +
                    "/aweme/v1/aweme/stats/?" + params
                ),
                data=payload,
                headers={'cookie': 'sessionid=90c38a59d8076ea0fbc01c8643efbe47', 'x-gorgon': sig['X-Gorgon'], 'x-khronos': sig['X-Khronos'], 'user-agent': 'okhttp/3.10.0.1'},
                verify=False,
                proxies={"http": proxy_format+proxy, "https": proxy_format+proxy} if config['proxy']['use-proxy'] else {}
            )
            reqs += 1

            if response.json()['status_code'] == 0:
                success += 1
                console.print(f"[bold green]Success:[/bold green] {success} [bold red]Fails:[/bold red] {fails} [bold yellow]Reqs:[/bold yellow] {reqs} RPS: {rps} RPM: {rpm}")
            else:
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
    url_list =[
        "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxy-list/data.txt",
        "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks5.txt"
        
    ]
    for url in url_list :
        response = requests.get(
            url=url
        )
        if response.ok:
            with open("proxies.txt", "a+") as f:
                f.write(response.text)
                f.close()
        else:
            pass

if __name__ == "__main__":
    with open('devices.txt', 'r') as f:
        devices = f.read().splitlines()
    
    with open('config.json', 'r') as f:
        config = json.load(f)

    if config["proxy"]['proxyscrape']:
        fetch_proxies()

    proxy_format = f'{config["proxy"]["proxy-type"].lower()}://{config["proxy"]["credential"]+"@" if config["proxy"]["auth"] else ""}' if config['proxy']['use-proxy'] else ''
    
    if config['proxy']['use-proxy']:
        with open('proxies.txt', 'r') as f:
            proxies = f.read().splitlines()

    os.system("cls" if os.name == "nt" else "clear")
    print("\033]0;Guinness Shepherd\007")
    #set_title("Guinness Shepherd")

    #txt = "\n\nTikTok Viewbot by @guinnessgshep \n"
    #print(Colorate.Vertical(Colors.DynamicMIX((Col.light_blue, Col.purple)), Center.XCenter(txt)))
    console.print("\n\n[bold blue on white]TikTok Viewbot by @guinnessgshep[/bold blue on white]\n")
    try:
        video = input('Enter Video URL -> ')
        num_threads = int(input('Threads -> '))

        __aweme_id = str(
            re.findall(r"(\d{18,19})", video)[0]
            if len(re.findall(r"(\d{18,19})", video)) == 1
            else re.findall(
                r"(\d{18,19})",
                requests.head(video, allow_redirects=True, timeout=5).url
            )[0]
        )
    except:
        os.system("cls" if os.name == "nt" else "clear")
        console.print("[red]x - Invalid link, try inputting video id only[/red]")
        sys.exit(0)

    os.system("cls" if os.name == "nt" else "clear")
    console.print("[bold yellow]Loading...[/bold yellow]")

    _lock = threading.Lock()
    reqs = 0
    success = 0
    fails = 0
    rpm = 0
    rps = 0

    threading.Thread(target=rpsm_loop).start()

    with alive_bar(len(devices), title='Processing', bar='smooth') as bar:
        def worker(device):
            if threading.active_count() < 100:
                did, iid, cdid, openudid = device.split(':')
                send(did, iid, cdid, openudid)
            bar()

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            executor.map(worker, devices)
