from rgbprint import Color, gradient_print
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs
from pprint import pprint
import time
from bs4 import BeautifulSoup
import socket
import re
import hashlib

green = Color.pale_green
yellow = Color.yellow
white = Color.ghost_white
red = Color.indian_red
gray = Color.gray
lime = Color.lime
yg = Color.yellow_green

success = f"{green}[+]{white}"
error = f"{red}[-]{white}"
wait = f"{yellow}[*]{white}"


s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"

###########################################################################################################
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

###########################################################################################################

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

###########################################################################################################


def check_paths(base_url, wordlist_file):
    with open(wordlist_file, 'r') as f:
        paths_to_check = [line.strip() for line in f.readlines() if line.strip()]

    for path in paths_to_check:
        time.sleep(0.2)
        url = urljoin(base_url, path)
        response = requests.get(url)
        if response.status_code == 200:
            print(f"{success} {yellow}► {gray}[ {lime}{url}{gray} ]")
        else:
            print(f"{error} {yellow}► {gray}[ {red}{url}{gray} ]")


###########################################################################################################



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


###########################################################################################################


def port_scan(target_host):
    start_port = 1
    end_port = 65535

    print(f"{wait} Scanning ports on{red} {target_host}{white}...")
    
    for port in range(start_port, end_port + 1):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(0.1) 

        try:
            client.connect((target_host, port))
            print(f"{success} Port{yellow} ►{white} {port} {yellow}►{lime} open")
            client.close()
        except socket.error:
            print(f"{error} Port{yellow} ►{white} {port}{yellow} ►{red} closed")



###########################################################################################################

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
        print(f"{success} Flag found in robots.txt {yellow}►{lime} {flag}{white}")
    else:
        flag = find_flag_in_source(url)
        if flag:
            print(f"{success} Flag found in page source  {yellow}►{red} {flag}{white}")
        else:
            print(f"{error} Flag not found.")

###########################################################################################################

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

###########################################################################################################


banner = f"""{lime}         ████
       ██────██
      █────────█
     █─▄▀█──█▀▄─█
    ▐▌──────────▐▌
    █▌▀▄──▄▄──▄▀▐█
   ▐██──▀▀──▀▀──██▌
  ▄████▄──▐▌──▄████▄
██████████████████████
█    {gray} Version{white} 3.0 {lime}   █
██████████████████████"""



help = f"""{lime}
█████████████████████████████████████████████████████████████████████████████████████████████████
█                                           {white} Scanner  {lime}                                          █
{green}█████████████████████████████████████████████████████████████████████████████████████████████████{lime}
█ {white}sql {gray}<URL>              {yellow}►{green} SQL Injection Scanner {lime}                                               █
█ {white}xss {gray}<URL>              {yellow}►{green} XSS Vulnerability Scanner   {lime}                                         █
█ {white}subdomain {gray}<URL>        {yellow}►{green} Subdomain Scanner                 {lime}                                   █
█ {white}clickjacking {gray}<URL>     {yellow}►{green} Clickjacking Scanner                    {lime}                             █
█ {white}portscan {gray}<domain>      {yellow}►{green} Port Scanner                                  {lime}                       █    
█████████████████████████████████████████████████████████████████████████████████████████████████
█                                           {white} Finder{lime}                                             █
{green}█████████████████████████████████████████████████████████████████████████████████████████████████{lime}
█ {white}admin {gray}<URL>            {yellow}►{green} Admin Finder{lime}                                                         █
█ {white}file {gray}<URL>             {yellow}►{green} show files        {lime}                                                   █
█ {white}flag {gray}<URL>             {yellow}►{green} See the hidden flags on the source code of the site or in robots.txt {lime}█
█ {white}search {gray}<URL>           {yellow}►{green} Search fields                                                       {lime} █
█ {white}email {gray}<URL>            {yellow}►{green} Email recovery                                                      {lime} █
█████████████████████████████████████████████████████████████████████████████████████████████████ 
█                                            {white} Spy{lime}                                               █
{green}█████████████████████████████████████████████████████████████████████████████████████████████████{lime}
█ {white}spy {gray}<URL>              {yellow}►{green} monitor a website                                                   {lime} █
█████████████████████████████████████████████████████████████████████████████████████████████████ 

"""

print(banner)

def main():
    while True:
        print(f'{white}┌───({green}webkit{gray}@{yg}3.0{white})─[{yellow}~{white}]')
        choice = input(f'{white}└─{gray}${lime} ')

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
                scan_xss(word)

            else:
                print(f"{error} Try again, you forgot the URL for the XSS Scanner")

        if choice.startswith("subdomain"):
            if len(w0rd) > 1:
                word = w0rd[-1]
                base_url = word
                wordlist_file = 'wordlist/rockyou.txt'
                check_paths(base_url, wordlist_file)
            else:
                print(f"{error} Try again, you forgot the URL for the Subdomain")

        if choice.startswith("clickjacking"):
            if len(w0rd) > 1:
                word = w0rd[-1]
                url = word
                is_vulnerable = check_clickjacking(url)
                if is_vulnerable:
                   print(f"{success} {yellow}►{white} {url} may be vulnerable to clickjacking.")
                else:
                    print(f"{error} {yellow}►{white} {url} is not vulnerable to clickjacking.")

                if not url.startswith('http://') and not url.startswith('https://'):
                   url = url
                print(f"{wait} Response Headers:")
                response = requests.get(url)
                for header, value in response.headers.items():
                   print(f"|{green} {header}{yellow} ► {green} {value}{white}")   
            else:
                print(f"{error} Try again, you forgot the URL for the Clickjacking")

        if choice.startswith("portscan"):
            if len(w0rd) > 1:
                word = w0rd[-1] 
                target = word
                ip_address = socket.gethostbyname(target)
                print(f"{wait} Target IP address: {ip_address}")
                port_scan(ip_address) 
            else:
                print(f"{error} Try again, you forgot the URL for the Port scanner")

        if choice.startswith("admin"):
            if len(w0rd) > 1:
                word = w0rd[-1] 
                url2 = word
                wordlist = 'wordlist/admin.txt'
                check_paths(url2, wordlist) 

            else:
                print(f"{error} Try again for Admin Finder")

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
                               print(f'{success} URL {yellow}►{white} FILE {yellow}►{white} {href}')
                else:
                    print(f'{error} URL {yellow}►{white} FILE {yellow}►{white} {href}')

            else:
                print(f"{error} Try again, put a url to find the files")

        if choice.startswith("flag"):
            if len(w0rd) > 1:
                word = w0rd[-1]
                site_url = word
                main_robot(site_url)

            else:
                print(f"{error} try again, to find the flags")

        if choice.startswith("search"):
            if len(w0rd) > 1:
                word = w0rd[-1]
                url = word
                response = requests.get(url)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    input_fields = soup.find_all('input')

                    for field in input_fields:
                        field_type = field.get('type')
                        field_name = field.get('name')
                        field_id = field.get('id')
                        field_placeholder = field.get('placeholder')
                        print(f"{success} Type: {lime}{field_type}{white}     {yellow}►{white}     Name: {lime}{field_name}{white}     {yellow}►{white}     ID: {lime}{field_id}{white}     {yellow}►{white}     Placeholder: {lime}{field_placeholder}{white}")
                else:
                    print(f"{error} Failed to retrieve the page. Status code : {response.status_code}")

            else:
                print(f"{error} try again to find the fields")

        if choice.startswith("email"):
            if len(w0rd) > 1:
                word = w0rd[-1] 
                url = word
                emails = email2(url)
                if emails:
                    print(f"{success} Email addresses found on {url}:")
                    for email in emails:
                       print(f'|{green} Found :{red} {email} {white}')
                else:
                    print(f"{error} No email address found on : {url}.")

            else:
                print(f"{error} Try again to receive all emails")

        if choice.startswith("spy"):
            if len(w0rd) > 1:
                word = w0rd[-1] 
                url = word

                etat_fichiers = {}

                while True:
                    try:
                        response = requests.get(url)
                        soup = BeautifulSoup(response.content, 'html.parser')
         
                        liens_fichiers = soup.find_all('a', href=True)
        
                        nouvel_etat = {}
        
                        for lien in liens_fichiers:
                            url_fichier = lien['href']
                            nom_fichier = lien.text.strip()
            
                            hash_fichier = hashlib.md5(url_fichier.encode()).hexdigest()
            
                            nouvel_etat[nom_fichier] = hash_fichier
        
                        if nouvel_etat != etat_fichiers:
                            print(f"{wait} Modification detected on {url} - {time.strftime('%Y-%m-%d %H:%M:%S')}")
                            for fichier, hash_val in nouvel_etat.items():
                                if fichier not in etat_fichiers or etat_fichiers[fichier] != hash_val:
                                   print(f"    {yellow}►{lime} {fichier} {gray}({hash_val})")

                            etat_fichiers = nouvel_etat
    
                    except requests.exceptions.RequestException as e:
                         print(f"{error} ERROR : {e}")

                    time.sleep(60)  
            else:
                print(f"{error} try again to monitor a website")

if __name__ == '__main__':
    main()