import os
import sys
import requests
import hashlib
import time
import threading
import json
import re

requests.packages.urllib3.disable_warnings()


class Gorgon:
    def __init__(self, params: str, unix: int) -> None:
        self.unix = unix
        self.params = params

    @staticmethod
    def hash(data: str) -> str:
        return hashlib.md5(data.encode()).hexdigest()

    def get_base_string(self) -> str:
        base_str = self.hash(self.params)
        base_str += '0' * 32
        base_str += '0' * 32
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
            param_list.extend([(H & 4278190080) >> 24, (H & 16711680) >> 16, (H & 65280) >> 8, H & 255])
        eor_result_list = [A ^ B for A, B in zip(param_list, key)]
        for i in range(length):
            D = eor_result_list[(i + 1) % length]
            E = 255 ^ D
            H = (E ^ 4294967295 ^ length) & 255
            eor_result_list[i] = H
        result = ''.join([format(param, '02x') for param in eor_result_list])
        return {'X-Gorgon': '0404b0d30000' + result, 'X-Khronos': str(unix)}


class TikTokBot:
    def __init__(self):
        self._lock = threading.Lock()
        self.reqs = 0
        self.success = 0
        self.fails = 0

    def send(self, did, iid, cdid, openudid):
        session = requests.Session()
        for _ in range(10):
            try:
                params = f"device_id={did}&iid={iid}&device_type=SM-G973N&..."
                sig = Gorgon(params=params, unix=int(time.time())).get_value()
                with open('config.json', 'r') as f:
                    config = json.load(f)
                proxy = random.choice(proxies) if config['proxy']['use-proxy'] else ""
                response = session.post(
                    url=("https://api16-va.tiktokv.com/aweme/v1/aweme/stats/?" + params),
                    data=f"item_id={self.__aweme_id}&play_delta=1",
                    headers={'cookie': 'sessionid=90c38a59d8076ea0fbc01c8643efbe47',
                             'x-gorgon': sig['X-Gorgon'], 'x-khronos': sig['X-Khronos'],
                             'user-agent': 'okhttp/3.10.0.1'},
                    verify=False,
                    proxies={"http": proxy, "https": proxy} if config['proxy']['use-proxy'] else {}
                )
                self.reqs += 1
                print(f"+ - sent views {response.json()['log_pb']['impr_id']} {self.__aweme_id} {self.reqs}")
                self.success += 1
            except:
                self.fails += 1
                continue

    @staticmethod
    def fetch_aweme_id(link: str) -> str:
        aweme_search = re.findall(r"(\d{18,19})", link)
        if aweme_search:
            return aweme_search[0]
        return re.findall(r"(\d{18,19})", requests.head(link, allow_redirects=True, timeout=5).url)[0]

    def run(self, link, thread_count):
        self.__aweme_id = self.fetch_aweme_id(link)
        with open('devices.txt', 'r') as f:
            devices = f.read().splitlines()
        while True:
            device = random.choice(devices)
            if threading.active_count() < thread_count:
                did, iid, cdid, openudid = device.split(':')
                threading.Thread(target=self.send, args=[did, iid, cdid, openudid]).start()


def main():
    os.system("cls" if os.name == "nt" else "clear")
    # Placeholder for title display
    print(r"""
                                         do. 
                                        :NOX 
                                       ,NOM@: 
                                       :NNNN: 
                                       :XXXON 
                                       :XoXXX. 
                                       MM;ONO: 
  .oob..                              :MMO;MOM 
 dXOXYYNNb.                          ,NNMX:MXN 
 Mo"'  '':Nbb                        dNMMN MNN: 
 Mo  'O;; ':Mb.                     ,MXMNM MNX: 
 @O :;XXMN..'X@b.                  ,NXOMXM MNX: 
 YX;;NMMMM@M;;OM@o.                dXOOMMN:MNX: 
 'MOONM@@@MMN:':NONb.            ,dXONM@@MbMXX: 
  MOON@M@@MMMM;;:OOONb          ,MX'"':ONMMMMX: 
  :NOOM@@MNNN@@X;""XNN@Mb     .dP"'   ,..OXM@N: 
   MOON@@MMNXXMMO  :M@@M...@o.oN"0MQOOOXNNXXOo:
   :NOX@@@MNXXXMNo :MMMM@K"`,:;NNM@@NXM@MNO;.'N. 
    NO:X@@MNXXX@@O:'X@@@@MOOOXMM@M@NXXN@M@NOO ''b 
    `MO.'NMNXXN@@N: 'XXM@NMMXXMM@M@XO"'"XM@X;.  :b 
     YNO;'"NXXXX@M;;::"XMNN:""ON@@MO: ,;;.:Y@X: :OX. 
      Y@Mb;;XNMM@@@NO: ':O: 'OXN@@MO" ONMMX:`XO; :X@. 
      '@XMX':OX@@MN:    ;O;  :OX@MO" 'OMM@N; ':OO;N@N 
       YN;":.:OXMX"': ,:NNO;';XMMX:  ,;@@MNN.'.:O;:@X: 
       `@N;;XOOOXO;;:O;:@MOO;:O:"" ,oMP@@K"YM.;NMO;`NM 
        `@@MN@MOX@@MNMN;@@MNXXOO: ,d@NbMMP'd@@OX@NO;.'bb. 
       .odMX@@XOOM@M@@XO@MMMMMMNNbN"YNNNXoNMNMO"OXXNO.."";o. 
     .ddMNOO@@XOOM@@XOONMMM@@MNXXMMo;."' .":OXO ':.'"'"'  '""o. 
    'N@@X;,M@MXOOM@OOON@MM@MXOO:":ONMNXXOXX:OOO               ""ob. 
   ')@MP"';@@XXOOMMOOM@MNNMOO""   '"OXM@MM: :OO.        :...';o;.;Xb. 
  .@@MX" ;X@@XXOOM@OOXXOO:o:'      :OXMNO"' ;OOO;.:     ,OXMOOXXXOOXMb 
 ,dMOo:  oO@@MNOON@N:::"      .    ,;O:."'  .dMXXO:    ,;OX@XO"":ON@M@ 
:Y@MX:.  oO@M@NOXN@NO. ..: ,;;O;.       :.OX@@MOO;..   .OOMNMO.;XN@M@P 
,MP"OO'  oO@M@O:ON@MO;;XO;:OXMNOO;.  ,.;.;OXXN@MNXO;.. oOX@NMMN@@@@@M: 
`' "O:;;OON@@MN::XNMOOMXOOOM@@MMNXO:;XXNNMNXXXN@MNXOOOOOXNM@NM@@@M@MP 
   :XN@MMM@M@M:  :'OON@@XXNM@M@MXOOdN@@@MM@@@@MMNNXOOOXXNNN@@M@MMMM" 
   .oNM@MM@ONO'   :;ON@@MM@MMNNXXXM@@@@M@PY@@MMNNNNNNNNNNNM@M@M@@P' 
  ;O:OXM@MNOOO.   'OXOONM@MNNMMXON@MM@@b. 'Y@@@@@@@@@@@@@M@@MP"' 
 ;O':OOXNXOOXX:   :;NMO:":NMMMXOOX@MN@@@@b.:M@@@M@@@MMM@ 
 :: ;"OOOOOO@N;:  'ON@MO.'":""OOOO@@NNMN@@@. Y@@@MMM@@@@b 
 :;   ':O:oX@@O;;  ;O@@XO'   "oOOOOXMMNMNNN@MN""YMNMMM@@MMo. 
 :N:.   ''oOM@NMo.::OX@NOOo.  ;OOOXXNNNMMMNXNM@bd@MNNMMM@MM@bb    @GUINNESSGSHEP 
  @;O .  ,OOO@@@MX;;ON@NOOO.. ' ':OXN@NNN@@@@@M@@@@MNXNMM@MMM@, 
  M@O;;  :O:OX@@M@NXXOM@NOO:;;:,;;ON@NNNMM'`"@@M@@@@@MXNMMMMM@N 
  N@NOO;:oO;O:NMMM@M@OO@NOO;O;oOOXN@NNM@@'   `Y@NM@@@@MMNNMM@MM 
  ::@MOO;oO:::OXNM@@MXOM@OOOOOOXNMMNNNMNP      ""MNNM@@@MMMM@MP 
    @@@XOOO':::OOXXMNOO@@OOOOXNN@NNNNNNNN        '`YMM@@@MMM@P' 
    MM@@M:'''' O:":ONOO@MNOOOOXM@NM@NNN@P            "`SHEP' 
    ''MM@:     "' 'OOONMOYOOOOO@MM@MNNM" 
      YM@'         :OOMN: :OOOO@MMNOXM'
      `:P           :oP''  "'OOM@NXNM' 
       `'                    GUINNESS' 
                               '"'  """)

    try:
        link = input("\n\nPaste your TikTok URL for buff here ==> ")        
        thread_count = int(input("Enter the number of threads you'd like to run: "))

        bot = TikTokBot()
        bot.run(link, thread_count)
    except ValueError:
        os.system("cls" if os.name == "nt" else "clear")
        print("\x1b[31m" + "x - Please enter a valid number for thread count." + "\x1b[0m")
    except Exception as e:
        os.system("cls" if os.name == "nt" else "clear")
        print("\x1b[31m" + f"x - An error occurred: {e}" + "\x1b[0m")
        sys.exit(1)

if __name__ == "__main__":
    main()


