import requests
from urllib.parse import urlparse
from .provider import LinkProvider
import logging

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
                response = requests.head(
                    link, allow_redirects=True, timeout=5
                )
                expanded_link = response.url
                url = urlparse(expanded_link)
                # Remove query parameters
                return f"{url.scheme}://{url.netloc}{url.path}"
            except Exception as e:
                logging.error(f"Error expanding Bilibili link: {e}")
                return None
        return None
