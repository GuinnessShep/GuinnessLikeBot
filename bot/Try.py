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
from rich.console import Console
from rich.progress import Progress, BarColumn
from colorama import Fore, Back, Style, init

init(autoreset=True)  # For Colorama

console = Console()

class BlockCookies(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

r = requests.Session()
r.cookies.set_policy(BlockCookies())

__domains = ["api22-core-c-useast1a.tiktokv.com", "api19-core-c-useast1a.tiktokv.com",
             "api16-core-c-useast1a.tiktokv.com", "api21-core-c-useast1a.tiktokv.com"]

__devices = ["SM-G9900", "SM-A136U1", "SM-M225FV", "SM-E426B", "SM-M526BR", "SM-M326B", "SM-A528B",
             "SM-F711B", "SM-F926B", "SM-A037G", "SM-A225F", "SM-M325FV", "SM-A226B", "SM-M426B",
             "SM-A525F", "SM-N976N"]

__versions = ["190303", "190205", "190204", "190103", "180904", "180804", "180803", "180802",  "270204"]

class Gorgon:
	def __init__(self,params:str,data:str,cookies:str,unix:int)->None:self.unix=unix;self.params=params;self.data=data;self.cookies=cookies
	def hash(self,data:str)->str:
		try:_hash=str(hashlib.md5(data.encode()).hexdigest())
		except Exception:_hash=str(hashlib.md5(data).hexdigest())
		return _hash
	def get_base_string(self)->str:base_str=self.hash(self.params);base_str=base_str+self.hash(self.data)if self.data else base_str+str('0'*32);base_str=base_str+self.hash(self.cookies)if self.cookies else base_str+str('0'*32);return base_str
	def get_value(self)->json:base_str=self.get_base_string();return self.encrypt(base_str)
	def encrypt(self,data:str)->json:
		unix=self.unix;len=20;key=[223,119,185,64,185,155,132,131,209,185,203,209,247,194,185,133,195,208,251,195];param_list=[]
		for i in range(0,12,4):
			temp=data[8*i:8*(i+1)]
			for j in range(4):H=int(temp[j*2:(j+1)*2],16);param_list.append(H)
		param_list.extend([0,6,11,28]);H=int(hex(unix),16);param_list.append((H&4278190080)>>24);param_list.append((H&16711680)>>16);param_list.append((H&65280)>>8);param_list.append((H&255)>>0);eor_result_list=[]
		for (A,B) in zip(param_list,key):eor_result_list.append(A^B)
		for i in range(len):C=self.reverse(eor_result_list[i]);D=eor_result_list[(i+1)%len];E=C^D;F=self.rbit_algorithm(E);H=(F^4294967295^len)&255;eor_result_list[i]=H
		result=''
		for param in eor_result_list:result+=self.hex_string(param)
		return{'X-Gorgon':'0404b0d30000'+result,'X-Khronos':str(unix)}
	def rbit_algorithm(self,num):
		result='';tmp_string=bin(num)[2:]
		while len(tmp_string)<8:tmp_string='0'+tmp_string
		for i in range(0,8):result=result+tmp_string[7-i]
		return int(result,2)
	def hex_string(self,num):
		tmp_string=hex(num)[2:]
		if len(tmp_string)<2:tmp_string='0'+tmp_string
		return tmp_string
	def reverse(self,num):tmp_string=self.hex_string(num);return int(tmp_string[1:]+tmp_string[:1],16)

def rainbow_text(text):
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
    rainbow = ''.join([colors[i % len(colors)] + char for i, char in enumerate(text)])
    return rainbow

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
            sig     = Gorgon(params=params, cookies=None, data=None, unix=int(time.time())).get_value()

            proxy = random.choice(proxies) if config['proxy']['use-proxy'] else ""

            response = r.post(
                url = (
                    "https://"
                    +  random.choice(__domains)  +
                    "/aweme/v1/aweme/stats/?" + params
                ),
                data    = payload,
                headers = {'cookie':'sessionid=90c38a59d8076ea0fbc01c8643efbe47','x-gorgon':sig['X-Gorgon'],'x-khronos':sig['X-Khronos'],'user-agent':'okhttp/3.10.0.1'},
                verify  = False,
                proxies = {"http": proxy_format+proxy, "https": proxy_format+proxy} if config['proxy']['use-proxy'] else {}
            )            
            reqs += 1
            if response.json()['status_code'] == 0:
                success += 1
                progress.update(task1, advance=1)
            else:
                fails += 1

        except Exception as e:
            pass

def rpsm_loop():
    global rps, rpm
    while True:
        initial = reqs
        time.sleep(1.5)
        rps = round((reqs - initial) / 1.5, 1)
        rpm = round(rps * 60, 1)

def main():
    global reqs, _lock, success, fails, rps, rpm

    console.print(rainbow_text("[TikTok] Bulk Device Register Tool by @ctrndk"), style="bold")

    if len(sys.argv) < 2:
        console.print("[red]Usage:[/red] python " + sys.argv[0] + " <threads> <times>")
        sys.exit(1)

    threads = int(sys.argv[1])
    times = int(sys.argv[2])
    console.print("[green]Threads:[/green] " + str(threads) + "\n[green]Times per thread:[/green] " + str(times))
    
    for _ in range(threads):
        threading.Thread(target=send, args=(
            ''.join(random.choice('0123456789abcdef') for _ in range(16)),
            ''.join(random.choice('0123456789abcdef') for _ in range(16)),
            ''.join(random.choice('0123456789abcdef') for _ in range(32)),
            ''.join(random.choice('0123456789abcdef') for _ in range(16))
        )).start()

    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.1f}%",
        "•",
        "[progress.completed]{task.completed} of {task.total} [bold cyan]Succeed[/bold cyan]",
        "•",
        "RPS: [bold cyan]{rps}[/bold cyan]",
        "•",
        "RPM: [bold cyan]{rpm}[/bold cyan]",
        transient=True,
    ) as progress:
        task1 = progress.add_task("[cyan]Sending...", total=times)
        while not progress.finished:
            progress.update(task1, rps=rps, rpm=rpm)
            time.sleep(0.5)
    
    console.print("[green]Completed![/green]")

if __name__ == "__main__":
    main()
