import time
import random
import logging
import requests
from bs4 import BeautifulSoup
from config import get_random_headers, get_proxy_dict, REQUEST_TIMEOUT, MAX_RETRIES

# Logging Configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class UniversalScraper:
    """A resilient HTTP web scraper featuring User-Agent rotation, proxy handling, and smart retries."""
    
    def __init__(self, delay_range=(1, 3)):
        self.delay_range = delay_range
        self.session = requests.Session()

    def fetch_page(self, url):
        """Executes a safe HTTP GET request with human-like delays and retry mechanisms."""
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                # Random delay to mimic human behavior
                time.sleep(random.uniform(*self.delay_range))
                
                headers = get_random_headers()
                proxies = get_proxy_dict()

                response = self.session.get(
                    url, 
                    headers=headers, 
                    proxies=proxies, 
                    timeout=REQUEST_TIMEOUT
                )

                if response.status_code == 200:
                    return BeautifulSoup(response.text, "html.parser")
                elif response.status_code == 429:
                    logging.warning(f"Rate limited (429). Retrying in 5 seconds... (Attempt {attempt}/{MAX_RETRIES})")
                    time.sleep(5)
                else:
                    logging.warning(f"Status Code {response.status_code} received for {url}")

            except requests.RequestException as e:
                logging.error(f"Request Error: {e} (Attempt {attempt}/{MAX_RETRIES})")

        return None

if __name__ == "__main__":
    # Test execution
    scraper = UniversalScraper()
    soup = scraper.fetch_page("https://httpbin.org/user-agent")
    if soup:
        logging.info("Scraper core initialized successfully!")
        print("Fetched data:", soup.text.strip())