import requests
from urllib.parse import urlparse, parse_qs
from .provider import LinkProvider

GOOGLE_MAPS_HEADERS = {
    "Host": "www.google.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers",
}


class GoogleMapsProvider(LinkProvider):
    """Handles Google Maps links by expanding and cleaning them"""

    @property
    def has_privacy_link(self) -> bool:
        return False

    def has_link(self, link: str) -> bool:
        return "maps.app.goo.gl/" in link or "maps.google.com/maps" in link

    def rewrite_link(self, link: str) -> str | None:
        if (
            link.startswith("https://maps.app.goo.gl/")
            or "maps.google.com/maps" in link
        ):
            try:
                response = requests.get(
                    link, headers=GOOGLE_MAPS_HEADERS, allow_redirects=True, timeout=5
                )
                expanded_link = response.url
                url = urlparse(expanded_link)

                # Keep only the 'q' parameter if present
                query_params = parse_qs(url.query)
                q = query_params.get("q", [None])[0]

                if q:
                    return f"{url.scheme}://{url.netloc}{url.path}?q={q}"
                else:
                    return f"{url.scheme}://{url.netloc}{url.path}"

            except Exception as e:
                import logging

                logging.error(f"Error expanding Google Maps link: {e}")
                return None
        return None
