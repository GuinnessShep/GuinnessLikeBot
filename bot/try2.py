import os
import re
import time
import random
import threading
import requests
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode
from rich.console import Console
from rich.progress import Progress
from colorama import Fore, init
from itertools import cycle
init(autoreset=True)

# ... [rest of the import and class definitions are unchanged]

def print_rainbow_text(text):
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
    color_cycle = cycle(colors)
    rainbow_text = ''.join([next(color_cycle) + char for char in text])
    console.print(rainbow_text, end='\r')

console = Console()

def send(__device_id, __install_id, cdid, openudid):
    global reqs, _lock, success, fails, rps, rpm
    for x in range(10):
        # ... [rest of the send function remains unchanged]
        try:
            if response.json()['status_code'] == 0:
                _lock.acquire()
                print_rainbow_text(f'TikTok Viewbot | success: {success} | fails: {fails} | reqs: {reqs} | rps: {rps} | rpm: {rpm}')
                success += 1
                _lock.release()
            else:
                fails += 1
        except:
            if _lock.locked():
                _lock.release()
            fails += 1

# ... [rest of the functions remain unchanged]

if __name__ == "__main__":
    # ... [rest of the main function remains unchanged]
    with Progress() as progress:
        task1 = progress.add_task("[cyan]Loading...", total=100)
        while not progress.finished:
            time.sleep(0.05)
            progress.update(task1, advance=2.5)

    # ... [rest of the main function remains unchanged]
