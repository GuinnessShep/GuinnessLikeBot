import aiohttp
import asyncio
import random
import json
import os
import re
from rich import print, box, layout
from rich.live import Live
from rich.table import Table
from rich.console import Console
from urllib.parse import urlencode
import hashlib
import time
import threading
from concurrent.futures import ThreadPoolExecutor

console = Console()
headers_table = Table(title="TikTok Viewbot", show_header=False, box=box.ASCII)

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

async def send(device):
    version = random.choice(__versions)
    params = {
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

    sig = Gorgon(params=params, cookies=None, data=None, unix=int(time.time())).get_value()

    proxy = random.choice(proxies) if config['proxy']['use-proxy'] else ""
    url = f"https://{random.choice(__domains)}/aweme/v1/aweme/stats/?{urlencode(params)}"

    headers = {
        'cookie': 'sessionid=90c38a59d8076ea0fbc01c8643efbe47',
        'x-gorgon': sig['X-Gorgon'],
        'x-khronos': sig['X-Khronos'],
        'user-agent': 'okhttp/3.10.0.1'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers, proxy=proxy) as response:
            json_response = await response.json()

            if json_response['status_code'] == 0:
                headers_table.add_row("[bold green]Success")
            else:
                headers_table.add_row("[bold red]Failure")

async def main():
    tasks = []
    for device in devices:
        task = asyncio.ensure_future(send(device))
        tasks.append(task)

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    with open('devices.txt', 'r') as f:
        devices = f.readlines()
    
    with open('config.json', 'r') as f:
        config = json.load(f)

    if config["proxy"]['proxyscrape']:
        fetch_proxies()

    proxy_format = f'{config["proxy"]["proxy-type"].lower()}://{config["proxy"]["credential"]+"@" if config["proxy"]["auth"] else ""}' if config['proxy']['use-proxy'] else ''
    
    if config['proxy']['use-proxy']:
        with open('proxies.txt', 'r') as f:
            proxies = f.readlines()

    console.clear()
    console.print("[bold blue on white]TikTok Viewbot by @guinnessgshep[/bold blue on white]\n")
    try:
        video = input('Enter Video URL -> ')
        num_threads = int(input('Threads -> '))

        __aweme_id = str(
            re.search(r"(\d{18,19})", video).group(1)
            if len(re.findall(r"(\d{18,19})", video)) == 1
            else re.search(
                r"(\d{18,19})",
                requests.head(video, allow_redirects=True, timeout=5).url
            ).group(1)
        )
    except:
        console.clear()
        console.print("[red]x - Invalid link, try inputting video id only[/red]")
        sys.exit(0)

    console.clear()
    console.print("[bold yellow]Loading...[/bold yellow]")

    reqs, success, fails, rpm, rps = 0, 0, 0, 0, 0
    threading.Thread(target=rpsm_loop).start()

    with alive_bar(len(devices), title='Processing', bar='smooth') as bar:
        def worker(device):
            if threading.active_count() < 100:
                did, iid, cdid, openudid = device.strip().split(':')
                send(did, iid, cdid, openudid)
            bar()

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            executor.map(worker, devices)
