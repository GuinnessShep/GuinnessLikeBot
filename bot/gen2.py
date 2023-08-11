import random
import uuid
import sys
import re
from time import time
from random import randint

class TikTokURL:
    def __init__(self, url):
        self.video_id = self.extract_video_id(url)

    def extract_video_id(self, url):
        pattern = r'/video/(\d+)/'
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        else:
            raise ValueError("Invalid TikTok URL")

    def generate_line(self):
        action_time = round(time())
        device_id = randint(100000000000000, 999999999999999)
        id = uuid.uuid4()
        hex_val = "%016x" % random.randint(0, 2**64-1)
        return f"{action_time}:{device_id}:{id}:{hex_val}"

# Check for command line argument for URL or ask for one
if len(sys.argv) > 2:
    tiktok_url = sys.argv[2]
else:
    tiktok_url = input("Please provide the TikTok URL: ")

tiktok = TikTokURL(tiktok_url)

# Check if a command line argument for number of lines is given
if len(sys.argv) > 1:
    try:
        num_lines = int(sys.argv[1])
    except ValueError:
        print("The given argument is not a valid number. Using default input method.")
        num_lines = int(input("How many lines do you want to generate? "))
else:
    num_lines = int(input("How many lines do you want to generate? "))

with open("devices.txt", "w") as f:
    for _ in range(num_lines):
        line = tiktok.generate_line()
        f.write(f"{line}\n")

print("File 'devices.txt' has been successfully generated.")
