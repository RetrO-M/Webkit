# SharkWeb

SharkWeb is a lightweight and customizable web crawler designed to explore websites, extract metadata, detect sensitive paths, and perform basic OSINT (Open Source Intelligence) tasks. Built in Python, it emphasizes efficiency, readability, and ease of use.

---------------

<p align="center">
   <a href="https://github.com/RetrO-M/SharkWeb">
      <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Tor-logo-2011-flat.svg/langfr-1920px-Tor-logo-2011-flat.svg.png" width="160" title="TOR">
   </a>
   <br>
</p>


-----------------

<a href="https://github.com/RetrO-M/SharkWeb/issues">⚠️ Report Bug</a>

**WARNING**: Don't forget to install TOR for this to work.
---

## Features
- **Metadata Extraction**: Retrieves website titles and descriptions.
- **Sensitive Path Detection**: Scans for common paths like `/admin` or `/config.php` etc.
- **Customizable User Agents**: Mimics different browsers to avoid detection. 
- **TOR Proxies**: Use TOR to hide our IP address by a proxy.
- **Dynamic Headers**: Randomized language and browser settings to mimic real users.

---

## Disclaimer

- **IMPORTANT**: 
  - This tool is designed for educational and research purposes only. **Do not use this crawler for any illegal activities**, including but not limited to unauthorized data collection, scraping websites without consent, or accessing restricted areas of websites. 

  - By using this tool, you acknowledge and agree that you are responsible for ensuring that any actions taken with this crawler comply with all applicable laws and regulations in your jurisdiction. The creator of this tool is not responsible for any misuse or damage caused by the improper or unauthorized use of this software.

- **Respect Privacy** 
  - Always respect the privacy and security of the websites you crawl. Ensure you have explicit permission to crawl or scrape any site, and follow the site's `robots.txt` file guidelines or any terms of service provided by the website owner.

- **Ethical Use** 
  - This tool is intended to help security professionals, researchers, and developers to understand and test websites for common vulnerabilities in a legal and ethical manner. Unauthorized scanning of websites or systems may violate laws and policies and could result in legal consequences.

- If you are unsure about the legality of using this tool, **consult a legal professional** before using it in any way that might violate laws or terms of service agreements.

By using this crawler, you agree to use it responsibly and ethically.

## ChangeLog
```ssh
v1.0 ⋮ 10/12/2024
```

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/RetrO-M/SharkWeb
    cd SharkWeb
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

---

## Usage
Run SharkWeb with customizable options:

```bash
python main.py <start_url> --depth <max_depth>
