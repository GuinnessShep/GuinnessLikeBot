import requests
import random
import time
import threading
import hashlib
from urllib.parse import urlencode
from requests.cookies import cookiejar
import ssl

requests.packages.urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context


class BlockCookies(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False


s = requests.Session()
s.cookies.set_policy(BlockCookies())

DOMAINS = [
    "api22-core-c-useast1a.tiktokv.com", "api19-core-c-useast1a.tiktokv.com",
    "api16-core-c-useast1a.tiktokv.com", "api21-core-c-useast1a.tiktokv.com"
]

DEVICES = [
    "SM-G9900", "SM-A136U1", "SM-M225FV", "SM-E426B", "SM-M526BR", "SM-M326B",
    "SM-A528B", "SM-F711B", "SM-F926B", "SM-A037G", "SM-A225F", "SM-M325FV",
    "SM-A226B", "SM-M426B", "SM-A525F", "SM-N976N"
]

VERSIONS = ["190303", "190205", "190204", "190103", "180904", "180804", "180803", "180802", "270204"]

devices = [f"{d}:{random.randint(100000000000,999999999999)}:{random.randint(100000000000,999999999999)}:{random.randint(100000000000,999999999999)}" for d in DEVICES]

__aweme_id = 'your_aweme_id_here'
reqs, success, fails, rps, rpm = 0, 0, 0, 0, 0
_lock = threading.Lock()


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

def send_request(__device_id, __install_id, cdid, openudid):
    global reqs, success, fails, rps, rpm
    for _ in range(10):
        try:
            version = random.choice(VERSIONS)
            params = urlencode({
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
                                })

            payload = f"item_id={__aweme_id}&play_delta=1"
            sig = Gorgon(params=params).get_value()

            response = s.post(
                url=f"https://{random.choice(DOMAINS)}/aweme/v1/aweme/stats/?{params}",
                data=payload,
                headers={
                    'cookie': 'sessionid=90c38a59d8076ea0fbc01c8643efbe47',
                    'x-gorgon': sig['X-Gorgon'],
                    'x-khronos': sig['X-Khronos'],
                    'user-agent': 'okhttp/3.10.0.1'
                },
                verify=False
            )

            reqs += 1
            if response.json()['status_code'] == 0:
                _lock.acquire()
                print(f'success: {success} fails: {fails} reqs: {reqs} rps: {rps} rpm: {rpm}')
                success += 1
                _lock.release()

        except:
            fails += 1
            continue


def main():
    while True:
        device = random.choice(devices)
        did, iid, cdid, openudid = device.split(':')
        threading.Thread(target=send_request, args=(did, iid, cdid, openudid)).start()


if __name__ == "__main__":
    main()
