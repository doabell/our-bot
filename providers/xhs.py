import requests

from urllib.parse import urlparse, parse_qs
from .provider import LinkProvider

XHS_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Cache-Control": "no-cache",
    "Origin": "https://www.xiaohongshu.com",
    "DNT": "1",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Referer": "https://www.xiaohongshu.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "TE": "trailers",
}


class XHSProvider(LinkProvider):
    delete_original = "always"
    """Handles XiaoHongShu (Little Red Book) links by expanding them"""

    @property
    def has_privacy_link(self) -> bool:
        return False

    def has_link(self, link: str) -> bool:
        return link.startswith("https://xhslink.com/")

    def rewrite_link(self, link: str) -> str | None:
        if link.startswith("https://xhslink.com/"):
            try:
                response = requests.get(
                    link, headers=XHS_HEADERS, allow_redirects=True, timeout=5
                )
                expanded_link = response.url
                url = urlparse(expanded_link)

                # Keep only xsec_token parameter if present
                query_params = parse_qs(url.query)
                xsec_token = query_params.get("xsec_token", [None])[0]

                if xsec_token:
                    return (
                        f"{url.scheme}://{url.netloc}{url.path}?xsec_token={xsec_token}"
                    )
                else:
                    return f"{url.scheme}://{url.netloc}{url.path}"

            except Exception as e:
                import logging

                logging.error(f"Error expanding XHS link: {e}")
                return None
        return None
