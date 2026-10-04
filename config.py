import os
from dotenv import load_dotenv
from fake_useragent import UserAgent

# Load environment variables
load_dotenv()

# Environment Variables
PROXY_URL = os.getenv("PROXY_URL", "")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

# Initialize User Agent Generator
ua = UserAgent()

HEADERS_BASE = {
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

def get_random_headers():
    """Generates base headers with a fresh dynamic User-Agent."""
    headers = HEADERS_BASE.copy()
    headers["User-Agent"] = ua.random
    return headers

def get_proxy_dict():
    """Returns proxy configuration dictionary if PROXY_URL is set."""
    if PROXY_URL:
        return {"http": PROXY_URL, "https": PROXY_URL}
    return None