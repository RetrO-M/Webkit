import os, time
class BACK:
    success = "\033[0m[ \033[32m✓ \033[0m]"
    error = "\033[0m[ \033[31mX \033[0m]"
def setup_option():
    ans = input('Do you want to install the modules Y/N : ')
    if ans == 'Y' or ans == 'y':
        setup()
    elif ans == 'N' or ans == 'n':
        exit
def setup():
    try:
        from colorama import Fore, init
        print(BACK.success + " The 'colorama' library is already installed and ready to use.")
    except ImportError:
        print(BACK.error + " The 'colorama' library is not installed. Installing now...")
        os.system('pip3 install colorama')
    try:
        import requests
        print(BACK.success + " The 'requests' library is already installed and ready to use.")
    except ImportError:
        print(BACK.error + " The 'requests' library is not installed. Installing now...")
        os.system('pip3 install requests[socks]')
    try:
        from bs4 import BeautifulSoup
        print(BACK.success + " The 'beautifulsoup4' library is already installed and ready to use.")
    except ImportError:
       print(BACK.error + " The 'beautifulsoup4' library is not installed. Installing now...")
       os.system('pip3 install beautifulsoup4')
    time.sleep(2)