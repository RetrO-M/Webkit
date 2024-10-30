import requests
from colorama import Fore, init
from bs4 import BeautifulSoup

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

def file_darkweb(url):
    response = requests.get(url, proxies=proxies)
    response.raise_for_status()
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href and not href.endswith('/'):
                print(log.success + f' {href}')
            else:
                print(log.error + f' {href}')