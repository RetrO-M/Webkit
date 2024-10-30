import requests, re
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

def email2(url):
    try:
        response = requests.get(url, proxies=proxies)
        if response.status_code == 200:
            pattern = r'[\w\.-]+@[\w\.-]+'
            emails = set(re.findall(pattern, response.text))
            return list(emails)
    except requests.exceptions.RequestException as e:
        print(log.error + f" ERROR: {e}")


def grab_email(url):
    emails = email2(url)
    if emails:
        print(log.success + f" Email addresses found on {url}:")
        for email in emails:
            print(log.success + f' Email : {email}')
    else:
        print(log.error + f" No email address found on : {url}.")
