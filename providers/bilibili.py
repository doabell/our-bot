import requests
from urllib.parse import urlparse
from .provider import LinkProvider
import logging

BILIBILI_HEADERS = {
    "Host": "www.bilibili.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "DNT": "1",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i",
    "TE": "trailers",
}


class BilibiliProvider(LinkProvider):
    """Handles Bilibili short links by expanding them"""

    @property
    def has_privacy_link(self) -> bool:
        return False

    def has_link(self, link: str) -> bool:
        return "b23.tv/" in link

    def rewrite_link(self, link: str) -> str | None:
        if link.startswith("https://b23.tv/"):
            try:
                response = requests.get(
                    link, headers=BILIBILI_HEADERS, allow_redirects=True, timeout=5
                )
                expanded_link = response.url
                url = urlparse(expanded_link)
                # Remove query parameters
                return f"{url.scheme}://{url.netloc}{url.path}"
            except Exception as e:
                logging.error(f"Error expanding Bilibili link: {e}")
                return None
        return None
