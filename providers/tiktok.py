from .provider import LinkProvider


class TikTokProvider(LinkProvider):
    """Substitutes tiktok.com domain to tnktok.com"""

    @property
    def has_privacy_link(self) -> bool:
        return False

    def has_link(self, link: str) -> bool:
        return "tiktok.com/" in link

    def rewrite_link(self, link: str) -> str | None:
        if link.startswith("https://www.tiktok.com/"):
            return link.replace("https://www.tiktok.com/", "https://tnktok.com/")
        elif link.startswith("https://tiktok.com/"):
            return link.replace("https://tiktok.com/", "https://tnktok.com/")
        return None
