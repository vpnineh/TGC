import requests
import threading
import json
import os 
import time
import random
import re
import base64
import argparse

from bs4 import BeautifulSoup
from datetime import datetime, timedelta

requests.post = lambda url, **kwargs: requests.request(
    method="POST", url=url, verify=False, **kwargs
)
requests.get = lambda url, **kwargs: requests.request(
    method="GET", url=url, verify=False, **kwargs
)

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

os.system('cls' if os.name == 'nt' else 'clear')

if not os.path.exists('sub'):
    with open('sub', 'w'): pass

def json_load(path):
    with open(path, 'r', encoding="utf-8") as file:
        list_content = json.load(file)
    return list_content

def substring_del(string_list):
    string_list.sort(key=lambda s: len(s), reverse=True)
    out = []
    for s in string_list:
        if not any([s in o for o in out]):
            out.append(s)
    return out

tg_name_json = json_load('telegramchannels.json')
inv_tg_name_json = json_load('invalidtelegramchannels.json')

inv_tg_name_json[:] = [x for x in inv_tg_name_json if len(x) >= 5]
inv_tg_name_json = list(set(inv_tg_name_json)-set(tg_name_json))

# Get the environment variable
thrd_pars = os.getenv('THRD_PARS')

# Convert to integer if not None, else assign None
thrd = int(thrd_pars) if thrd_pars is not None else None

# Check if thrd is an integer
if isinstance(thrd, int):
    sem_pars = threading.Semaphore(thrd)
else:
    print("Invalid input! Please set THRD_PARS to an integer.")

# Print the integer value
print("Threads:", thrd)

pars_dp = os.getenv('PARS_DP')
pars_dp = int(pars_dp) if pars_dp is not None else None
print("Parsing depth where 1dp equals 20 last tg posts:", pars_dp)

print(f'\nTotal channel names in telegramchannels.json         - {len(tg_name_json)}')
print(f'Total channel names in invalidtelegramchannels.json - {len(inv_tg_name_json)}')


use_inv_tc = os.getenv('USE_INV_TC')
# Validate the value
if use_inv_tc not in {"y", "n"}:
    raise ValueError("Invalid value. Expected 'y' or 'n'.")
print()

start_time = datetime.now()

config_all = list()
tg_name = list()


print(f'\nSearch for new names is over - {str(datetime.now() - start_time).split(".")[0]}')

print(f'\nStart Parsing...\n')

def process(i_url):
    sem_pars.acquire()
    html_pages = list()
    cur_url = i_url
    god_tg_name = False
    for itter in range(1, pars_dp+1):
        while True:
            try:
                response = requests.get(f'https://t.me/s/{cur_url}')
            except:
                time.sleep(random.randint(5,25))
                pass
            else:
                if itter == pars_dp:
                    print(f'{tg_name_json.index(i_url)+1} of {walen} - {i_url}')
                html_pages.append(response.text)
                last_datbef = re.findall(pattern_datbef, response.text)
                break
        if not last_datbef:
            break
        cur_url = f'{i_url}?before={last_datbef[0]}'
    for page in html_pages:
        soup = BeautifulSoup(page, 'html.parser')
        code_tags = soup.find_all(class_='tgme_widget_message_text')
        for code_tag in code_tags:
            code_content2 = str(code_tag).split('<br/>')
            for code_content in code_content2:
                if "vless://" in code_content or "ss://" in code_content or "vmess://" in code_content or "trojan://" in code_content or "tuic://" in code_content or "hysteria://" in code_content or "hy2://" in code_content or "hysteria2://" in code_content or "juicity://" in code_content or "nekoray://" in code_content or "socks4://" in code_content or "socks5://" in code_content or "socks://" in code_content or "naive+" in code_content:
                    codes.append(re.sub(htmltag_pattern, '', code_content))
                    god_tg_name = True                    
    if not god_tg_name:
        inv_tg_name_json.append(i_url)
    sem_pars.release()

htmltag_pattern = re.compile(r'<.*?>')

codes = list()

walen = len(tg_name_json)
for url in tg_name_json:
    threading.Thread(target=process, args=(url,)).start()
    
while threading.active_count() > 1:
    time.sleep(1)

print(f'\nParsing completed - {str(datetime.now() - start_time).split(".")[0]}')

print(f'\nStart check and remove duplicate from parsed configs...')

codes = list(set(codes))

processed_codes = list()

for part in codes:
    part = re.sub('%0A', '', part)
    part = re.sub('%250A', '', part)
    part = re.sub('%0D', '', part)
    part = requests.utils.unquote(requests.utils.unquote(part)).strip()
    part = re.sub('amp;', '', part)
    part = re.sub('�', '', part)
    part = re.sub('fp=firefox', 'fp=chrome', part)
    part = re.sub('fp=safari', 'fp=chrome', part)
    part = re.sub('fp=edge', 'fp=chrome', part)
    part = re.sub('fp=360', 'fp=chrome', part)
    part = re.sub('fp=qq', 'fp=chrome', part)
    part = re.sub('fp=ios', 'fp=chrome', part)
    part = re.sub('fp=android', 'fp=chrome', part)
    part = re.sub('fp=randomized', 'fp=chrome', part)
    part = re.sub('fp=random', 'fp=chrome', part)
    if "vmess://" in part:
        part = f'vmess://{part.split("vmess://")[1]}'
        processed_codes.append(part.strip())
        continue
    elif "vless://" in part:
        part = f'vless://{part.split("vless://")[1]}'
        if "@" in part and ":" in part[8:]:
            processed_codes.append(part.strip())
        continue
    elif "ss://" in part:
        part = f'ss://{part.split("ss://")[1]}'
        processed_codes.append(part.strip())
        continue
    elif "trojan://" in part:
        part = f'trojan://{part.split("trojan://")[1]}'
        if "@" in part and ":" in part[9:]:
            processed_codes.append(part.strip())
        continue
    elif "tuic://" in part:
        part = f'tuic://{part.split("tuic://")[1]}'
        if ":" in part[7:] and "@" in part:
            processed_codes.append(part.strip())
        continue
    elif "hysteria://" in part:
        part = f'hysteria://{part.split("hysteria://")[1]}'
        if ":" in part[11:] and "=" in part:
            processed_codes.append(part.strip())
        continue
    elif "hysteria2://" in part:
        part = f'hysteria2://{part.split("hysteria2://")[1]}'
        if "@" in part and ":" in part[12:]:
            processed_codes.append(part.strip())
        continue
    elif "hy2://" in part:
        part = f'hy2://{part.split("hy2://")[1]}'
        if "@" in part and ":" in part[6:]:
            processed_codes.append(part.strip())
        continue
    elif "juicity://" in part:
        part = f'juicity://{part.split("juicity://")[1]}'
        processed_codes.append(part.strip())
        continue
    elif "nekoray://" in part:
        part = f'nekoray://{part.split("nekoray://")[1]}'
        processed_codes.append(part.strip())
        continue
    elif "socks4://" in part:
        part = f'socks4://{part.split("socks4://")[1]}'
        if ":" in part[9:]:
            processed_codes.append(part.strip())
        continue
    elif "socks5://" in part:
        part = f'socks5://{part.split("socks5://")[1]}'
        if ":" in part[9:]:
            processed_codes.append(part.strip())
        continue
    elif "socks://" in part:
        part = f'socks://{part.split("socks://")[1]}'
        if ":" in part[8:]:
            processed_codes.append(part.strip())
        continue
    elif "naive+" in part:
        part = f'naive+{part.split("naive+")[1]}'
        if ":" in part[13:] and "@" in part:
            processed_codes.append(part.strip())
        continue

print(f'\nTrying to delete corrupted configurations...') 

processed_codes = list(set(processed_codes))
processed_codes = [x for x in processed_codes if (len(x)>13) and (("…" in x and "#" in x) or ("…" not in x))]
new_processed_codes = list()
for x in processed_codes:
    if x[-2:] == '…»':
        x=x[:-2]
    if x[-1:] == '…':
        x=x[:-1]
    if x[-1:] == '»':
        x=x[:-1]
    if x[-2:-1] == '%':
        x=x[:-2]
    if x[-1:] == '%':
        x=x[:-1]
    if x[-1:] == '`':
        x=x[:-1]        
    new_processed_codes.append(x.strip())
processed_codes = list(set(new_processed_codes))

#processed_codes = substring_del(processed_codes)
#processed_codes = list(set(processed_codes))
processed_codes = sorted(processed_codes)


with open("sub", "w", encoding="utf-8") as file:
    for code in processed_codes:
        file.write(code.encode("utf-8").decode("utf-8") + "\n")

print(f'\nTime spent - {str(datetime.now() - start_time).split(".")[0]}')
#print(f'\nTime spent - {timedelta(seconds=int((datetime.now() - start_time).total_seconds()))}')
