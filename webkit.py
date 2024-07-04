from rgbprint import Color, gradient_print
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs
from pprint import pprint
import time
import socket
import json
from bs4 import BeautifulSoup

green = Color.pale_green
red = Color.orange_red
magenta = Color.magenta
white = Color.ghost_white

success = f"{green}[+]{white}"
error = f"{red}[-]{white}"
wait = f"{magenta}[*]{white}"



s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"



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
        print(f"{wait} Trying", new_url)
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



def check_paths(base_url, wordlist_file):
    with open(wordlist_file, 'r') as f:
        paths_to_check = [line.strip() for line in f.readlines() if line.strip()]

    for path in paths_to_check:
        time.sleep(0.2)
        url = urljoin(base_url, path)
        response = requests.get(url)
        if response.status_code == 200:
            print(f"{success} {url}")
        else:
            print(f"{error} {url}")


def check_clickjacking(url):
    try:
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
        response = requests.get(url)
        headers = response.headers
        if 'X-Frame-Options' not in headers:
            return True
        x_frame_options = headers['X-Frame-Options'].lower()
        if x_frame_options != 'deny' and x_frame_options != 'sameorigin':
            return True
        return False
    except requests.exceptions.RequestException as e:
        print(f"{error} An error occurred while checking {url} - {e}")
        return False

def port_scan(target_host):
    start_port = 1
    end_port = 65535

    print(f"{wait} Scanning ports on{red} {target_host}{white}...")
    
    for port in range(start_port, end_port + 1):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(0.1) 

        try:
            client.connect((target_host, port))
            print(f"{success} Port   |   {port}   |   open")
            client.close()
        except socket.error:
            print(f"{error} Port   |   {port}   |   closed")





logo = f"""{green}
  /$$      /$$ /$$$$$$$$ /$$$$$$$  /$$   /$$ /$$$$$$ /$$$$$$$$
 | $$  /$ | $$| $$_____/| $$__  $$| $$  /$$/|_  $$_/|__  $$__/
 | $$ /$$$| $$| $$      | $$  \ $$| $$ /$$/   | $$     | $$   
 | $$/$$ $$ $$| $$$$$   | $$$$$$$ | $$$$$/    | $$     | $$   
 | $$$$_  $$$$| $$__/   | $$__  $$| $$  $$    | $$     | $$   
 | $$$/ \  $$$| $$      | $$  \ $$| $$\  $$   | $$     | $$   
 | $$/   \  $$| $$$$$$$$| $$$$$$$/| $$ \  $$ /$$$$$$   | $$   
 |__/     \__/|________/|_______/ |__/  \__/|______/   |__/  

 {white}•{green} Coded by Fatal r00ted
"""

help = f"""{white}• {green}sql <URL>             -   {red}SQL Injection Scanner
{white}• {green}xss <URL>             -   {red}XSS Scanner
{white}• {green}subdomain <URL>       -   {red}Subdomain Website
{white}• {green}clickjacking <URL>    -   {red}Clickjacking Scanner
{white}• {green}get <domain.com>      -   {red}Website Information
{white}• {green}proxy <ip:port>       -   {red}Proxy HTTP check
{white}• {green}portscan <domain.com> -   {red}Port Scanner
{white}• {green}scrape <URL>          -   {red}Web Scraper
{white}• {green}file <URL>            -   {red}show files
{white}• {green}read <URL>            -   {red}see all files"""

print(logo)

def main():

    while True:
        choice = input(f'{white}webkit:~{red}${green} ')

        w0rd = choice.split()
        if choice == "help":
            print(help)
        if choice.startswith("sql"):
            if len(w0rd) > 1:
                word = w0rd[-1]
                scan_sql_injection(word)
            else:
                print(f"{error} Try again, you forgot the URL for the SQL Injection Scanner")

        if choice.startswith("xss"):
            if len(w0rd) > 1:
                word = w0rd[-1]
                url = word
                scan_xss(url)
            else:
                print(f"{error} Try again, you forgot the URL for the XSS Scanner")

        if choice.startswith("subdomain"):
            if len(w0rd) > 1:
                word = w0rd[-1]
                base_url = word
                wordlist_file = 'rockyou.txt'
                check_paths(base_url, wordlist_file)
            else:
                print(f"{error} Try again, you forgot the URL for the Subdomain")

        if choice.startswith("clickjacking"):
            if len(w0rd) > 1:
                word = w0rd[-1]
                url = word
                is_vulnerable = check_clickjacking(url)
                if is_vulnerable:
                   print(f"{success} {url} may be vulnerable to clickjacking.")
                else:
                    print(f"{error} {url} is not vulnerable to clickjacking.")

                if not url.startswith('http://') and not url.startswith('https://'):
                   url = url
                print(f"{wait} Response Headers:")
                response = requests.get(url)
                for header, value in response.headers.items():
                   print(f"|{green} {header}{white}:{red} {value}{white}")   
            else:
                print(f"{error} Try again, you forgot the URL for the Clickjacking")

        if choice.startswith("get"):
            if len(w0rd) > 1:
                word = w0rd[-1]
                req = requests.get(f"http://{word}")
                print(f"{success} {red}"+str(req.headers))

                ip = socket.gethostbyname(word)
                response = requests.get("http://ip-api.com/json/" +ip)
                data = response.text
                values = json.loads(data)
                print(f"{white}IP :{red}", values.get('query','Not Available'))
                print(f"{white}STATUS :{red}",  values.get('status','Not Available'))
                print(f"{white}COUNTRY :{red}", values.get('country','Not Available'))
                print(f"{white}COUNTRY CODE :{red}", values.get('countryCode','Not Available'))
                print(f"{white}REGION :{red}", values.get('region','Not Available'))
                print(f"{white}CITY :{red}", values.get('city','Not Available'))
                print(f"{white}ZIP :{red}", values.get('zip','Not Available'))
                print(f"{white}LAT :{red}", str(values.get('lat','Not Available')))
                print(f"{white}LON :{red}", str(values.get('lon','Not Available')))
                print(f"{white}TIMEZONE :{red}", values.get('timezone','Not Available'))
                print(f"{white}ISP NAME :{red}", values.get('isp','Not Available'))
            else:
                print(f"{error} Try again to get the information on a website")

        if choice.startswith("proxy"):
            if len(w0rd) > 1:
                word = w0rd[-1] 
                proxy = word             
                proxies = {'http': proxy}

                r = requests.get('http://httpbin.org/get', proxies=proxies)

                print(r.text)
            else:
                print(f"{error} try again, you made a mistake, put a proxy with the port (example: 127.0.0.1:80)")

        if choice.startswith("portscan"):
            if len(w0rd) > 1:
                word = w0rd[-1] 
                target = word
                ip_address = socket.gethostbyname(target)
                print(f"{wait} Target IP address: {ip_address}")
                port_scan(ip_address) 
            else:
                print(f"{error} Try again, you forgot the URL for the Port scanner")

        if choice.startswith("scrape"):
            if len(w0rd) > 1:
                word = w0rd[-1] 
                target = word
                response = requests.get(target)
                print(response.text)
            else:
                print(f"{error} Try again, you forgot the URL for the Web Scraper")

        if choice.startswith("file"):
            if len(w0rd) > 1:
                word = w0rd[-1] 
                url = word           
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    links = soup.find_all('a') 
                    for link in links:
                           href = link.get('href')
                           if href and not href.endswith('/'):
                               print(f'{success} URL  |  FILE  |  {href}')
                else:
                    print(f'{error} URL  |  FILE  |  {href}')

            else:
                print(f"{error} Try again, put a url to find the files")

        if choice.startswith("read"):
            if len(w0rd) > 1:
                word = w0rd[-1] 
                base_url = word
                try:
                   response = requests.get(base_url)
                   response.raise_for_status()  
                   soup = BeautifulSoup(response.text, 'html.parser')
                   links = soup.find_all('a')
                   for link in links:
                        href = link.get('href')
                        if href and (href.startswith('http') or href.startswith('/')) and not href.endswith('/'):
                            full_url = href if href.startswith('http') else base_url.rstrip('/') + href
                            try:
                                file_response = requests.get(full_url)
                                file_response.raise_for_status()  
                                print(f'{success} URL  |  FILE  |  {full_url}')
                                print(f'{wait} Content of {full_url}:\n{file_response.text[:200]}...') 
                            except requests.RequestException as e:
                                  print(f'{error} URL  |  FILE  |  {full_url} | {e}')
                except requests.RequestException as e:
                       print(f'{error} Failed to access {base_url} | {e}')
            else:
                print(f"{error} Try again. Put a URL to read the files")


if __name__ == '__main__':
    main()