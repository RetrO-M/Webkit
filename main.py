from argparse           import ArgumentParser
from requests           import get, RequestException, exceptions
from bs4                import BeautifulSoup
from urllib.parse       import urljoin, urlparse
from collections        import deque
from colorama           import Fore, init
from random             import choice
from os                 import system

init()

class SharkWeb:
    def __init__(self):
        self.random_ua = choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.62",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.62",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
        ])

        self.headers = {
            "User-Agent": self.random_ua,
            "Accept-Language": choice([
                "en-US,en;q=0.9", "fr-FR,fr;q=0.9", "es-ES,es;q=0.9", "de-DE,de;q=0.9",
                "it-IT,it;q=0.9", "pt-PT,pt;q=0.9", "ru-RU,ru;q=0.9", "ja-JP,ja;q=0.9",
                "zh-CN,zh;q=0.9", "ko-KR,ko;q=0.9", "nl-NL,nl;q=0.9", "ar-SA,ar;q=0.9",
                "hi-IN,hi;q=0.9", "tr-TR,tr;q=0.9", "sv-SE,sv;q=0.9", "da-DK,da;q=0.9",
                "fi-FI,fi;q=0.9", "no-NO,no;q=0.9", "el-GR,el;q=0.9", "th-TH,th;q=0.9",
                "hu-HU,hu;q=0.9", "ro-RO,ro;q=0.9", "cs-CZ,cs;q=0.9", "sk-SK,sk;q=0.9",
                "bg-BG,bg;q=0.9", "lv-LV,lv;q=0.9", "lt-LT,lt;q=0.9", "sl-SI,sl;q=0.9",
                "et-EE,et;q=0.9", "ms-MY,ms;q=0.9", "vi-VN,vi;q=0.9", "bn-BD,bn;q=0.9",
                "sw-KE,sw;q=0.9", "tl-PH,tl;q=0.9", "iw-IL,iw;q=0.9", "pa-PK,pa;q=0.9",
                "fa-IR,fa;q=0.9", "ne-NP,ne;q=0.9", "sq-AL,sq;q=0.9", "km-KH,km;q=0.9",
                "is-IS,is;q=0.9", "hy-AM,hy;q=0.9", "az-AZ,az;q=0.9", "ka-GE,ka;q=0.9",
                "mt-MT,mt;q=0.9", "cy-GB,cy;q=0.9", "tk-TM,tk;q=0.9", "xh-ZA,xh;q=0.9",
                "zu-ZA,zu;q=0.9", "ar-AE,ar;q=0.9", "uk-UA,uk;q=0.9", "si-LK,si;q=0.9",
                "mn-MN,mn;q=0.9", "la-VN,la;q=0.9", "pa-IN,pa;q=0.9", "sw-TZ,sw;q=0.9",
                "te-IN,te;q=0.9", "ta-LK,ta;q=0.9", "ml-IN,ml;q=0.9", "kn-IN,kn;q=0.9",
                "or-IN,or;q=0.9", "gu-IN,gu;q=0.9", "mr-IN,mr;q=0.9", "as-IN,as;q=0.9",
                "my-MM,my;q=0.9", "bs-BA,bs;q=0.9", "hr-HR,hr;q=0.9", "sr-RS,sr;q=0.9",
                "ca-ES,ca;q=0.9", "eo-EO,eo;q=0.9", "oc-FR,oc;q=0.9", "se-NO,se;q=0.9",
                "ay-PE,ay;q=0.9", "qu-PE,qu;q=0.9", "fy-NL,fy;q=0.9", "jv-ID,jv;q=0.9",
                "su-ID,su;q=0.9", "sc-IT,sc;q=0.9", "gd-GB,gd;q=0.9", "wa-BE,wa;q=0.9",
                "sm-WS,sm;q=0.9", "so-SO,so;q=0.9", "ku-TR,ku;q=0.9", "na-NR,na;q=0.9",
                "fj-FJ,fj;q=0.9", "ht-HT,ht;q=0.9", "ti-ER,ti;q=0.9", "sg-CF,sg;q=0.9",
                "br-FR,br;q=0.9", "gn-PY,gn;q=0.9", "af-ZA,af;q=0.9", "csb-PL,csb;q=0.9",
                "hsb-DE,hsb;q=0.9", "yue-HK,yue;q=0.9", "to-TO,to;q=0.9", "dz-BT,dz;q=0.9",
                "qu-BO,qu;q=0.9", "sa-IN,sa;q=0.9", "rw-RW,rw;q=0.9", "mi-NZ,mi;q=0.9",
                "fo-FO,fo;q=0.9", "haw-US,haw;q=0.9", "gl-ES,gl;q=0.9", "nv-US,nv;q=0.9",
                "arn-CL,arn;q=0.9", "kl-GL,kl;q=0.9", "en-NG,en;q=0.9", "tg-TJ,tg;q=0.9",
                "ps-AF,ps;q=0.9", "prs-AF,prs;q=0.9", "am-ET,am;q=0.9", "ig-NG,ig;q=0.9",
                "yo-NG,yo;q=0.9", "ha-NE,ha;q=0.9", "sh-BA,sh;q=0.9", "sr-ME,sr;q=0.9",
                "tt-RU,tt;q=0.9", "ky-KG,ky;q=0.9", "uz-UZ,uz;q=0.9", "ba-RU,ba;q=0.9",
                "kk-KZ,kk;q=0.9", "be-BY,be;q=0.9", "mo-MD,mo;q=0.9", "ab-GE,ab;q=0.9",
                "os-RU,os;q=0.9", "tt-RU,tt;q=0.9", "ts-BW,ts;q=0.9", "st-LS,st;q=0.9"
            ]),
        }

        self.tor_proxy = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
    def title(self):
        system('cls || clear')
        print(
            f'''
{Fore.LIGHTBLUE_EX}███████ ██   ██  █████  ██████  ██   ██ ██     ██ ███████ ██████  
{Fore.BLUE}██      ██   ██ ██   ██ ██   ██ ██  ██  ██     ██ ██      ██   ██ 
{Fore.LIGHTBLUE_EX}███████ ███████ ███████ ██████  █████   ██  █  ██ █████   ██████  
{Fore.BLUE}     ██ ██   ██ ██   ██ ██   ██ ██  ██  ██ ███ ██ ██      ██   ██ 
{Fore.LIGHTBLUE_EX}███████ ██   ██ ██   ██ ██   ██ ██   ██  ███ ███  ███████ ██████ {Fore.LIGHTWHITE_EX}
            '''
        )
    def scan_common_paths(self, base_url):
        common_paths = [
            "/admin", "/login", "/.env", "/config.php", "/robots.txt",
            "/.git", "/backup.zip", "/database.sql", "/index.php.bak"
        ]
        print(f"{Fore.LIGHTBLUE_EX}[ + ]{Fore.LIGHTWHITE_EX} Checking for sensitive paths on : {base_url}")
        for path in common_paths:
            test_url = urljoin(base_url, path)
            try:
                response = get(test_url, headers=self.headers, proxies=self.tor_proxy, timeout=3)
                if response.status_code == 200:
                    print(f"{Fore.LIGHTWHITE_EX}    •{Fore.LIGHTCYAN_EX} {test_url}")
            except RequestException:
                pass


    def get_website_info(self, start_url):
        try:
            response = get(start_url, headers=self.headers, proxies=self.tor_proxy, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            title = soup.title.string if soup.title else "Title not found"
            
            meta_description = soup.find('meta', attrs={'name': 'description'})
            description = meta_description['content'] if meta_description else "Description not found"
            
            return {"Title": title, "Description": description}
        except exceptions.RequestException as e:
            return {"Error": f"Error fetching the page: {e}"}

    def crawl_website(self, start_url, max_depth):
        try:
            visited = set()
            queue = deque([(start_url, 0)])
            found_emails = set()
            base_domain = urlparse(start_url).netloc

            info = self.get_website_info(start_url)


            print(f"{Fore.LIGHTBLUE_EX}[ + ]{Fore.LIGHTWHITE_EX} Starting the crawler on{Fore.LIGHTCYAN_EX} {start_url}{Fore.LIGHTWHITE_EX}, maximum depth: {Fore.LIGHTCYAN_EX} {max_depth}")
            print(f"{Fore.LIGHTWHITE_EX}    •{Fore.LIGHTBLUE_EX} Title      {Fore.LIGHTCYAN_EX} : {Fore.LIGHTWHITE_EX}{info.get('Title', 'N/A')}")
            print(f"{Fore.LIGHTWHITE_EX}    •{Fore.LIGHTBLUE_EX} Description {Fore.LIGHTCYAN_EX}: {Fore.LIGHTWHITE_EX}{info.get('Description', 'N/A')}")

            while queue:
                url, depth = queue.popleft()
                if depth > max_depth:
                    continue

                if url in visited:
                    continue
                visited.add(url)

                try:
                    response = get(url, headers=self.headers, proxies=self.tor_proxy, timeout=5)
                    soup = BeautifulSoup(response.text, "html.parser")
                    print(f"{Fore.LIGHTWHITE_EX}    •{Fore.LIGHTBLUE_EX} Exploring:{Fore.LIGHTWHITE_EX} {url}{Fore.LIGHTCYAN_EX} (Depth {depth})")

                    for link in soup.find_all("a", href=True):
                        full_link = urljoin(url, link["href"])
                        if full_link not in visited and urlparse(full_link).netloc == base_domain:
                            queue.append((full_link, depth + 1))


                except RequestException as e:
                    print(f"{Fore.LIGHTBLUE_EX}[ + ]{Fore.LIGHTRED_EX} Unable to access {url}: {e} {url} : {e}")

            self.scan_common_paths(start_url)
        except KeyboardInterrupt:
            print(f"{Fore.LIGHTBLUE_EX}[ + ]{Fore.LIGHTWHITE_EX} SharkWeb process stopped.")
            exit(1)

if __name__ == "__main__":
    shark = SharkWeb()
    shark.title()
    parser = ArgumentParser(description="")
    parser.add_argument("url", help="URL")
    parser.add_argument("--depth", type=int, default=2, help="Maximum crawl depth")
    
    args = parser.parse_args()
    shark.crawl_website(args.url, args.depth)
