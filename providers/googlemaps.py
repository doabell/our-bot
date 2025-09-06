import requests
from urllib.parse import urlparse, parse_qs
from .provider import LinkProvider

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
                response = requests.head(
                    link, allow_redirects=True, timeout=5
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
