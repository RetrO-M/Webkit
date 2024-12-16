from requests                       import get, head, RequestException
from colorama                       import Fore, init
from json                           import loads, JSONDecodeError
from bs4                            import BeautifulSoup as BSoup
from time                           import sleep
from os                             import system
from random                         import choice
from bs4                            import BeautifulSoup
from urllib.parse                   import urlencode, urljoin

init(autoreset=True)

class TokTook:
    def extract_video_id(self, link):
        try:
            if "vm.tiktok.com" in link or "vt.tiktok.com" in link:
                resolved_url = head(link, allow_redirects=True, timeout=5).url
                video_id = resolved_url.split("/")[5].split("?", 1)[0]
                print(f"{Fore.LIGHTGREEN_EX}[++]{Fore.LIGHTWHITE_EX} Shortened link resolved: {Fore.LIGHTMAGENTA_EX}{video_id}{Fore.LIGHTWHITE_EX}")
            else:
                video_id = link.split("/")[5].split("?", 1)[0]
                print(f"{Fore.LIGHTGREEN_EX}[++]{Fore.LIGHTWHITE_EX} Extracted video ID:{Fore.LIGHTMAGENTA_EX} {video_id}{Fore.LIGHTWHITE_EX}")
            return video_id
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}[++]{Fore.LIGHTWHITE_EX} Error while extracting video ID: {e}")
            raise

    def scrape_comments(self, video_id):
        cursor = 0
        total_comments = 0
        headers = {
            'User-Agent': choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"
            ]),
            'referer': f'https://www.tiktok.com/@x/video/{video_id}',
        }

        print(f"{Fore.LIGHTCYAN_EX}[++]{Fore.LIGHTWHITE_EX} Starting comment scraping for video:{Fore.LIGHTMAGENTA_EX} {video_id}{Fore.LIGHTWHITE_EX}")

        while True:
            try:
                response = get(
                    f"https://www.tiktok.com/api/comment/list/"
                    f"?aid=1988&aweme_id={video_id}&count=50&cursor={cursor}",
                    headers=headers
                ).json()

                comments = response.get("comments", [])
                if not comments:
                    print(f"{Fore.LIGHTRED_EX}[++]{Fore.LIGHTWHITE_EX} No more comments found.")
                    break

                for comment in comments:
                    print(f"{Fore.LIGHTGREEN_EX}[++]{Fore.LIGHTWHITE_EX} COMMENT{Fore.LIGHTMAGENTA_EX} ->{Fore.LIGHTGREEN_EX} {comment['text']}")
                    sleep(0.05)
                    total_comments += 1

                cursor += len(comments)
            except Exception as e:
                print(f"{Fore.LIGHTRED_EX}[++]{Fore.LIGHTWHITE_EX} Error during scraping: {e}")
                break

        print(f"{Fore.LIGHTGREEN_EX}[++]{Fore.LIGHTWHITE_EX} Scraping completed. Total comments retrieved: {total_comments}")

    def get_tiktoker(self, username: str):
        headers = {
            'User-Agent': choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"
            ]),
        }

        tiktok_url = 'https://www.tiktok.com/@'

        try:
            response = get(tiktok_url + username, headers=headers)
            response.raise_for_status()
        except RequestException as e:
            print(f"{Fore.LIGHTRED_EX}Failed to retrieve data for {username}. Error: {e}")
            return

        soup = BSoup(response.text, 'html.parser')
        script_tag = soup.find('script', id='__UNIVERSAL_DATA_FOR_REHYDRATION__', type='application/json')

        if script_tag:
            try:
                json_data = loads(script_tag.string)
                user_data = json_data['__DEFAULT_SCOPE__']['webapp.user-detail']
                self.parse_tiktoker_data(username, user_data)
            except JSONDecodeError as error:
                print(f"{Fore.LIGHTRED_EX}Error parsing JSON: {error}")
        else:
            print(f'{Fore.LIGHTRED_EX}No script tag with id="__UNIVERSAL_DATA_FOR_REHYDRATION__" found.')

    def parse_tiktoker_data(self, username, field: dict):
        user_data = field["userInfo"]["user"]
        user_stats = field["userInfo"]["stats"]
        user_share_meta = field["shareMeta"]

        profile_pic_url = user_data.get("avatarLarger", "")

        print(f'{Fore.LIGHTGREEN_EX}[++]{Fore.LIGHTWHITE_EX} Profile Picture URL: {profile_pic_url}')
        print(f'{Fore.LIGHTGREEN_EX}[++]{Fore.LIGHTWHITE_EX} Account ID:       {user_data["id"]}')
        print(f'{Fore.LIGHTGREEN_EX}[++]{Fore.LIGHTWHITE_EX} Unique ID:        {user_data["uniqueId"]}')
        print(f'{Fore.LIGHTGREEN_EX}[++]{Fore.LIGHTWHITE_EX} Nickname:         {user_data["nickname"]}')
        signature = user_data["signature"].replace('\n', ' ')
        print(f'{Fore.LIGHTGREEN_EX}[++]{Fore.LIGHTWHITE_EX} Bios:             {signature}')
        print(f'{Fore.LIGHTGREEN_EX}[++]{Fore.LIGHTWHITE_EX} Private Account:  {user_data["privateAccount"]}')
        print(f'{Fore.LIGHTGREEN_EX}[++]{Fore.LIGHTWHITE_EX} User Country:     {user_data["region"]}')
        print(f'{Fore.LIGHTGREEN_EX}[++]{Fore.LIGHTWHITE_EX} Account Language: {user_data["language"]}')
        
        print(f'\n{Fore.LIGHTGREEN_EX}[++]{Fore.LIGHTWHITE_EX} Total Followers:  {user_stats["followerCount"]}')
        print(f'{Fore.LIGHTGREEN_EX}[++]{Fore.LIGHTWHITE_EX} Total Following:  {user_stats["followingCount"]}')
        print(f'{Fore.LIGHTGREEN_EX}[++]{Fore.LIGHTWHITE_EX} Total Hearts     {user_stats["heartCount"]}')
        print(f'{Fore.LIGHTGREEN_EX}[++]{Fore.LIGHTWHITE_EX} Total Posts:      {user_stats["videoCount"]}')
        
        print(f'\n{Fore.LIGHTGREEN_EX}[++]{Fore.LIGHTWHITE_EX} Title:            {user_share_meta["title"]}')
        print(f'{Fore.LIGHTGREEN_EX}[++]{Fore.LIGHTWHITE_EX} Description:      {user_share_meta["desc"]}\n')

    def scrape_tiktok_video(self, video_url):
        headers = {
            'User-Agent': choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"
            ]),
        }
        api_url = f"https://www.tiktok.com/oembed?url={video_url}"
        
        response = get(api_url, headers=headers)
        if response.status_code == 200:
            video_data = response.json()
            print(f"{Fore.LIGHTGREEN_EX}[++]{Fore.LIGHTWHITE_EX} Title:", video_data.get("title"))
            print(f"{Fore.LIGHTGREEN_EX}[++]{Fore.LIGHTWHITE_EX} Author:", video_data.get("author_name"))
            print(f"{Fore.LIGHTGREEN_EX}[++]{Fore.LIGHTWHITE_EX} Author URL:", video_data.get("author_url"))
            print(f"{Fore.LIGHTGREEN_EX}[++]{Fore.LIGHTWHITE_EX} Thumbnail:", video_data.get("thumbnail_url"))

    def tiktok_search(self, text):
        query = f"{text} site:tiktok.com"
        url = "https://www.google.com/search?"
        params = {
            'q': query,
            'hl': 'en', 
            'num': 10    
        }
        headers = {
            'User-Agent': choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
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
            ]),
        }
        url_with_params = url + urlencode(params)
        
        try:
            response = get(url_with_params, headers=headers)
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if 'tiktok.com' in link and not any(sub in link for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                        links.append(link)
                elif 'tiktok.com' in href and href.startswith('http') and not any(sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
            
            return links
        
        except RequestException as e:
            print(f"{Fore.LIGHTRED_EX}[++]{Fore.LIGHTWHITE_EX} Error : {e}")
            return None
        
    def title(self):
        system('cls || clear')
        print(
            f'''

██████╗ ███████╗███████╗██████╗ ████████╗ ██████╗ ██╗  ██╗
██╔══██╗██╔════╝██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██║ ██╔╝
██║  ██║█████╗  █████╗  ██████╔╝   ██║   ██║   ██║█████╔╝ 
██║  ██║██╔══╝  ██╔══╝  ██╔═══╝    ██║   ██║   ██║██╔═██╗ 
██████╔╝███████╗███████╗██║        ██║   ╚██████╔╝██║  ██╗
╚═════╝ ╚══════╝╚══════╝╚═╝        ╚═╝    ╚═════╝ ╚═╝  ╚═╝
{Fore.LIGHTWHITE_EX} [{Fore.LIGHTMAGENTA_EX}01{Fore.LIGHTWHITE_EX}] TikTok Comment Scraper
{Fore.LIGHTWHITE_EX} [{Fore.LIGHTMAGENTA_EX}02{Fore.LIGHTWHITE_EX}] Tiktok Profile Scraper
{Fore.LIGHTWHITE_EX} [{Fore.LIGHTMAGENTA_EX}03{Fore.LIGHTWHITE_EX}] Tiktok Video Scraper
{Fore.LIGHTWHITE_EX} [{Fore.LIGHTMAGENTA_EX}04{Fore.LIGHTWHITE_EX}] Google Dorking FullName Tiktok
{Fore.LIGHTWHITE_EX} [{Fore.LIGHTMAGENTA_EX}05{Fore.LIGHTWHITE_EX}] Google Dorking Email Tiktok
            '''.replace("█", f"{Fore.LIGHTMAGENTA_EX}█{Fore.LIGHTWHITE_EX}")
        )

if __name__ == "__main__":
    tok = TokTook()
    try:
        while True:
            tok.title()
            command = input(f'{Fore.LIGHTWHITE_EX}[{Fore.LIGHTMAGENTA_EX}>{Fore.LIGHTWHITE_EX}] Choice?: ')
            
            if command == "01" or command == "1":
                video_url = input(f"{Fore.LIGHTWHITE_EX}Enter the TikTok link: ").strip()
                video_id = tok.extract_video_id(video_url)
                tok.scrape_comments(video_id)
                input(f'{Fore.LIGHTWHITE_EX}[{Fore.LIGHTMAGENTA_EX}>{Fore.LIGHTWHITE_EX}] Type "enter" to continue')
            elif command == "02" or command == "2":
                username = input(f"{Fore.LIGHTWHITE_EX}Enter TikTok username (without '@'): ")
                if username:
                    tok.get_tiktoker(username)
                    input(f'{Fore.LIGHTWHITE_EX}[{Fore.LIGHTMAGENTA_EX}>{Fore.LIGHTWHITE_EX}] Type "enter" to continue')
            elif command == "03" or command == "3":
                video_url = input(f"{Fore.LIGHTWHITE_EX}Enter the TikTok link: ")
                tok.scrape_tiktok_video(video_url)
                input(f'{Fore.LIGHTWHITE_EX}[{Fore.LIGHTMAGENTA_EX}>{Fore.LIGHTWHITE_EX}] Type "enter" to continue')
            elif command == "04" or command == "4":
                fullname = input(f"{Fore.LIGHTWHITE_EX}Full Name: ")
                tiktok_results = tok.tiktok_search(fullname)
                if tiktok_results:
                    print(f'{Fore.LIGHTCYAN_EX}[++]{Fore.LIGHTWHITE_EX} Found{Fore.LIGHTMAGENTA_EX} {len(tiktok_results)}{Fore.LIGHTWHITE_EX} URLs of tiktok.com')
                    for link in tiktok_results:
                        if 'tiktok.com' in link:
                            print(f"{Fore.LIGHTGREEN_EX}[++]{Fore.LIGHTWHITE_EX} tiktok.com{Fore.LIGHTMAGENTA_EX} :{Fore.LIGHTGREEN_EX} {link}")
                input(f'{Fore.LIGHTWHITE_EX}[{Fore.LIGHTMAGENTA_EX}>{Fore.LIGHTWHITE_EX}] Type "enter" to continue')
            elif command == "05" or command == "5":
                email = input(f"{Fore.LIGHTWHITE_EX}Email: ")
                tiktok_results = tok.tiktok_search(email)
                if tiktok_results:
                    print(f'{Fore.LIGHTCYAN_EX}[++]{Fore.LIGHTWHITE_EX} Found{Fore.LIGHTMAGENTA_EX} {len(tiktok_results)}{Fore.LIGHTWHITE_EX} URLs of tiktok.com')
                    for link in tiktok_results:
                        if 'tiktok.com' in link:
                            print(f"{Fore.LIGHTGREEN_EX}[++]{Fore.LIGHTWHITE_EX} tiktok.com{Fore.LIGHTMAGENTA_EX} :{Fore.LIGHTGREEN_EX} {link}")
                input(f'{Fore.LIGHTWHITE_EX}[{Fore.LIGHTMAGENTA_EX}>{Fore.LIGHTWHITE_EX}] Type "enter" to continue')

    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}[++]{Fore.LIGHTWHITE_EX} Program failed: {e}")