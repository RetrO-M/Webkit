#!/usr/bin/env python3

import argparse
import requests
from rgbprint import Color, gradient_print
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs
from pprint import pprint
import re
from requests_html import HTMLSession
import json
import socket

green = Color.pale_green
red = Color.indian_red
white = Color.ghost_white
violet = Color.blue_violet

success = f"{green}[+]{white}"
error = f"{red}[-]{white}"
wait = f"{violet}[*]{white}"

s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"

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

def scan_sql_injection(url):
    for c in "\"'":
        new_url = f"{url}{c}"
        print(f"{wait} Trying", new_url)
        res = s.get(new_url)
        if is_vulnerable(res):
            print(f"{success} SQL Injection vulnerability detected, link:", new_url)
            return
    forms = get_all_forms(url)
    print(f"{success} Detected {len(forms)} forms on {url}.")
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
            url = urljoin(url, form_details["action"])
            if form_details["method"] == "post":
                res = s.post(url, data=data)
            elif form_details["method"] == "get":
                res = s.get(url, params=data)
            if is_vulnerable(res):
                print(f"{success} SQL Injection vulnerability detected, link:", url)
                print(f"{wait} Form:")
                pprint(form_details)
                break


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
    



banner = f"""{red}
 _    _ ___________ _   _______ _____ 
| |  | |  ___| ___ \ | / /_   _|_   _|
| |  | | |__ | |_/ / |/ /  | |   | |  
| |/\| |  __|| ___ \    \  | |   | |  
\  /\  / |___| |_/ / |\  \_| |_  | |  
 \/  \/\____/\____/\_| \_/\___/  \_/  {white}
"""

print(banner)

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-s', '--subdomain', type=str, help='')
    parser.add_argument('-q', '--sql', type=str, help='')
    parser.add_argument('-x', '--xss', type=str, help='')
    parser.add_argument('-c', '--clickjacking', type=str, help='')
    parser.add_argument('-i', '--info', type=str, help='')

    args = parser.parse_args()

    if args.clickjacking:
        url = args.clickjacking
        is_vulnerable = check_clickjacking(url)
        if is_vulnerable:
            print(f"{success} {url} may be vulnerable to clickjacking.")
        else:
            print(f"{error} {url} is not vulnerable to clickjacking.")

        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
        print(f"{wait} Response Headers:")
        response = requests.get(url)
        for header, value in response.headers.items():
            print(f"| {header}: {value}")

    if args.xss:
        url = args.xss
        scan_xss(url)
        
    if args.sql:
        url = args.sql
        scan_sql_injection(url)


    if args.subdomain:
        base_url = f"http://{args.subdomain}"
        wordlist_file = "rockyou.txt"
        print('\nWEB KIT                                       V.1.0     ')
        print('=====================================================')
        print(f'''Url/Domain : {args.subdomain}
File name : {wordlist_file}''')
        print('=====================================================')
        check_paths(base_url, wordlist_file)
        print('=====================================================')

    if args.info:
        req = requests.get(f"http://{args.info}")
        print("\n"+str(req.headers))

        ip = socket.gethostbyname(args.info)
        print("\n\nThe IP <" +args.info+ "> is : [" +ip+ "]\n")
        response = requests.get("http://ip-api.com/json/" +ip)
        data = response.text
        values = json.loads(data)
        print('\nWEB KIT                                       V.1.0     ')
        print('=====================================================')
        print("IP :", values.get('query','Not Available'))
        print("STATUS :",  values.get('status','Not Available'))
        print("COUNTRY :", values.get('country','Not Available'))
        print("COUNTRY CODE :", values.get('countryCode','Not Available'))
        print("REGION :", values.get('region','Not Available'))
        print("CITY :", values.get('city','Not Available'))
        print("ZIP :", values.get('zip','Not Available'))
        print("LAT :", str(values.get('lat','Not Available')))
        print("LON :", str(values.get('lon','Not Available')))
        print("TIMEZONE :", values.get('timezone','Not Available'))
        print("ISP NAME :", values.get('isp','Not Available'))
        print('=====================================================')
        
if __name__ == '__main__':
    main()