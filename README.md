
<div align="center">
  <kbd>
  <a href="https://github.com/RetrO-M">
    <img src="img/img.png" alt="Logo" width="300" height="300">
  </a>
  </kbd>
  
  <h2 align="center">WEB KIT</h2>

  <p align="center">
    V1.5 - (<b> by Fatal r00ted </b>)
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
- 
---------------------------------------

<h4 align="center">Languages ➜</h5>
<p align="center">
           <img src="https://skillicons.dev/icons?i=py"/>
</p>

---------------------------------------

### 🧵 Help


```bash
• sql <URL>             -   SQL Injection Scanner
• xss <URL>             -   XSS Scanner
• subdomain <URL>       -   Subdomain Website
• clickjacking <URL>    -   Clickjacking Scanner
• get <domain.com>      -   Website Information
• proxy <ip:port>       -   Proxy HTTP check
• portscan <domain.com> -   Port Scanner
• scrape <URL>          -   Web Scraper
• file <URL>            -   show files
• read <URL>            -   see all files
```

```
webkit:~$ sql http://google.com/
[*] Trying http://google.com/"
[*] Trying http://google.com/'
[+] Detected 1 forms on http://google.com/.

webkit:~$ xss http://google.com/
[+] Detected 1 forms on http://google.com/.
[+] Submitting malicious payload to http://google.com/search
[+] Data: {'NULL': 'Google NULL', 'NULL': 'NULL', 'NULL': 'NULL', 'source': 'NULL', 'NULL': 'NULL', 'NULL': 'NULL'}

webkit:~$ subdomain http://google.com/
[-] http://google.com/signup
[-] http://google.com/login
[-] http://google.com/logout
[-] http://google.com/database
[-] http://google.com/secret
[-] http://google.com/app
[+] http://google.com/sms
[-] http://google.com/ipv4

webkit:~$ clickjacking http://google.com/
[-] http://google.com/ is not vulnerable to clickjacking.
[*] Response Headers:
| Date:
| Expires: 
| Cache-Control:
| Content-Type: 
| Content-Security-Policy-Report-Only: 
| Content-Encoding: 
| Server: 
| Content-Length: 
| X-XSS-Protection: 0
| X-Frame-Options: 
| Set-Cookie: 

webkit:~$ get gooogle.com
[+] NULL
IP : ###.###.##.##
STATUS : success
COUNTRY :
COUNTRY CODE : 
REGION :
CITY : 
ZIP : 
LAT : 
LON : 
TIMEZONE : 
ISP NAME : Google LLC

webkit:~$ proxy 127.0.0.1:80 <--- HTTP PROXY
{
  'httpbin': '127.0.0.1'
}

webkit:~$ portscan google.com
[*] Target IP address: 
[*] Scanning ports on 
[+] Port   |   1   |   open
[+] Port   |   2   |   open
[-] Port   |   3   |   closed
[+] Port   |   4   |   open
[+] Port   |   5   |   open
[+] Port   |   6   |   open
[+] Port   |   7   |   open

webkit:~$ scrape http://google.com/
CODE HERE

webkit:~$ file http://google.com/
[+] URL  |  FILE  |  CENSURED
[+] URL  |  FILE  |  http://maps.google.nl/maps?########
[+] URL  |  FILE  |  CENSURED
[+] URL  |  FILE  |  https://www.youtube.com/#####
[+] URL  |  FILE  |  CENSURED
[+] URL  |  FILE  |  CENSURED
[+] URL  |  FILE  |  CENSURED
[+] URL  |  FILE  |  CENSURED
[+] URL  |  FILE  |  CENSURED
[+] URL  |  FILE  |  CENSURED
[+] URL  |  FILE  |  CENSURED
[+] URL  |  FILE  |  CENSURED
[+] URL  |  FILE  |  CENSURED
[+] URL  |  FILE  |  CENSURED
[+] URL  |  FILE  |  CENSURED

webkit:~$ read http://google.com/
[+] URL  |  FILE  |  https://www.google.com/##############
[*] Content of https://www.google.com/##############
<h1>Hello world</h1>
```


---------------------------------------

### 📜 ChangeLog

```diff
v1.0 ⋮ 29/06/2024
v1.5 ⋮ 4/07/2024
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
Proxy HTTP
Port Scanner
Web Scraper
show files
see all files
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
