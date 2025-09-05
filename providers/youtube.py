from urllib.parse import urlparse, parse_qs
from .provider import LinkProvider


class YouTubeProvider(LinkProvider):
    """Handles YouTube links, normalizing them to standard format"""

    @property
    def has_privacy_link(self) -> bool:
        return False

    def has_link(self, link: str) -> bool:
        return "youtube.com/" in link or "youtu.be/" in link

    def rewrite_link(self, link: str) -> str | None:
        try:
            url = urlparse(link)

            # Handle youtu.be format
            if "youtu.be" in url.netloc:
                video_id = url.path.strip("/")
                t = parse_qs(url.query).get("t", [None])[0]
                rewritten = f"https://www.youtube.com/watch?v={video_id}"
                if t:
                    rewritten += f"&t={t}"
                return rewritten

            # Handle youtube.com format
            elif "youtube.com" in url.netloc:
                query_params = parse_qs(url.query)
                video_id = query_params.get("v", [None])[0]
                t = query_params.get("t", [None])[0]

                if video_id:
                    rewritten = f"https://www.youtube.com/watch?v={video_id}"
                    if t:
                        rewritten += f"&t={t}"
                    return rewritten

            return None
        except Exception:
            return None
