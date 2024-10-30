import requests
from bs4 import BeautifulSoup
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

def advanced_scraper(url):
    try:
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        page_title = soup.title.string if soup.title else 'No title available'
        meta_description = soup.find('meta', attrs={'name': 'description'})
        description = meta_description['content'] if meta_description else 'No description available'
        paragraphs = [p.get_text(separator="\n", strip=True) for p in soup.find_all('p')]
        headers = []
        for i in range(1, 4):
            headers.extend([header.get_text(strip=True) for header in soup.find_all(f'h{i}')])
        lists = []
        for ul in soup.find_all('ul'):
            list_items = [li.get_text(strip=True) for li in ul.find_all('li')]
            if list_items:
                lists.append(list_items)
        results = {
            'title': page_title,
            'description': description,
            'paragraphs': paragraphs,
            'headers': headers,
            'lists': lists
        }
        return results
    except requests.exceptions.RequestException as e:
        print(f'Error during the request: {e}')
        return {}

def tor_scraper(url):
    data = advanced_scraper(url) 
    print(log.success + f" Page Title: {data['title']}")
    print(log.success + f" Description: {data['description']}\n")

    print(log.wait + " Headers and Subheaders:")
    for header in data['headers']:
        print(log.success + f" {header}")

    print(f"\n{log.wait} Paragraphs:")
    for idx, para in enumerate(data['paragraphs'], start=1):
        print(log.success + f" {idx}. {para}")

    print(f"\n{log.wait} Lists:")
    for idx, lst in enumerate(data['lists'], start=1):
        print(log.success + f" List {idx}: {', '.join(lst)}")