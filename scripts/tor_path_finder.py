from urllib.parse import urljoin
import time, requests
from colorama import Fore, init

init()

class log:
    wait = f"{Fore.LIGHTWHITE_EX}({Fore.LIGHTCYAN_EX} * {Fore.LIGHTWHITE_EX})"
    success = f"{Fore.LIGHTWHITE_EX}({Fore.LIGHTGREEN_EX} ✓ {Fore.LIGHTWHITE_EX})"
    error = f"{Fore.LIGHTWHITE_EX}({Fore.LIGHTRED_EX} X {Fore.LIGHTWHITE_EX})"
    info = f"{Fore.LIGHTWHITE_EX}({Fore.LIGHTBLUE_EX} i {Fore.LIGHTWHITE_EX})"

proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}

def path_finder(url, wordlist):
    paths_to_check = [line.strip() for line in wordlist if line.strip()]

    for path in paths_to_check:
        url = urljoin(url, path)
        time.sleep(0.5)
        response = requests.get(url,proxies=proxies)
        if response.status_code == 200:
            print(log.success + f"{Fore.LIGHTGREEN_EX} {url}{Fore.LIGHTCYAN_EX}  ]→{Fore.LIGHTWHITE_EX}  Status :{Fore.LIGHTMAGENTA_EX} {response.status_code}")
