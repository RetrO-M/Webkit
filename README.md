
<div align="center">
  <kbd>
  <a href="https://github.com/RetrO-M">
    <img src="img.png" alt="Logo" width="300" height="300">
  </a>
  </kbd>
  
  <h2 align="center">WEB KIT</h2>

  <p align="center">
    V1.0 - (<b> by Fatal r00ted </b>)
    <br />
    <br />
    <a href="https://github.com/RetrO-M/Webkit/issues/">⚠️ Report Bug</a>
  </p>
</div>

---------------------------------------

### ⚙️ Installation
* linux-py: `sudo apt install python3`
* win-py: `https://www.python.org/downloads/`

---------------------------------------

### ❗ Disclaimers
- No nonsense.
---------------------------------------

<h4 align="center">Languages ➜</h5>
<p align="center">
           <img src="https://skillicons.dev/icons?i=py"/>
</p>

---------------------------------------

### 🧵 Help

```bash
root:~# webkit -h

usage: webkit.py [-h] [-s SUBDOMAIN] [-q SQL] [-x XSS] [-c CLICKJACKING] [-i INFO]

options:
  -h, --help            show this help message and exit
  -s SUBDOMAIN, --subdomain SUBDOMAIN
  -q SQL, --sql SQL
  -x XSS, --xss XSS
  -c CLICKJACKING, --clickjacking CLICKJACKING
  -i INFO, --info INFO
```

```bash
root:~# webkit -s domain.com
==========================================
[+] http://domain.com/login
[+] http://domain.com/sms
[+] http://domain.com/ipv4
[+] http://domain.com/logout
[-] http://domain.com/admin
==========================================
root:~# webkit -q http://domain.com/
[*] Trying https://domain.com/"
[*] Trying https://domain.com/'
[+] Detected 0 forms on https://domain.com/.

root:~# webkit -x https://domain.com
[+] Detected 1 forms on https://domain.com.
[+] Submitting malicious payload to https://domain.com/search
[+] Data: {'CENSURED': 'CENSURED', 'CENSURED': 'CENSURED', 'CENSURED': 'CENSURED', 'CENSURED': 'CENSURED', 'CENSURED': 'CENSURED', 'CENSURED': 'CENSURED', 'CENSURED': 'CENSURED'}

root:~# webkit -c domain.com
[-] roblox.com is not vulnerable to clickjacking.
[*] Response Headers:
| BLABLALBA
| BLABLALBA
| BLABLALBA
| BLABLALBA
| BLABLALBA
| BLABLALBA

root:~# webkit -i domain.com
The IP <domain.com> is : [127.0.0.1]


WEB KIT                                       V.1.0
=====================================================
IP : 127.0.0.1
STATUS : success
COUNTRY : LOL
COUNTRY CODE : LOL
REGION : L
CITY : LOL
ZIP : LOL
LAT : 50.###
LON : 8.####
TIMEZONE : Hide
ISP NAME : Domain TEST
=====================================================

```

---------------------------------------

### 📜 ChangeLog

```diff
v1.0 ⋮ 29/06/2024
```

---------------------------------------

### 📣 Features

```diff
+ WEBKIT Information
Subdomain
Sql Injection Scanner
XSS vulnerability scanner
Clickjacking
Get information about a site
```

---------------------------------------

<p align="center">
  <img src="https://img.shields.io/github/stars/RetrO-M/Webkit.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA"/>
  <img src="https://img.shields.io/github/languages/top/RetrO-M/Webkit.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=python"/>
</p>


<a href="https://star-history.com/#RetrO-M/Webkit&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=RetrO-M/Webkit&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=RetrO-M/Webkit&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=RetrO-M/Webkit&type=Date" />
 </picture>
</a>
