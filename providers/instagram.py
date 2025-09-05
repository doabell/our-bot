from .provider import LinkProvider


class InstagramProvider(LinkProvider):
    """Substitutes instagram.com domain to ddinstagram.com"""

    @property
    def has_privacy_link(self) -> bool:
        return False

    def has_link(self, link: str) -> bool:
        return "instagram.com/" in link

    def rewrite_link(self, link: str) -> str | None:
        if link.startswith("https://www.instagram.com/"):
            return link.replace(
                "https://www.instagram.com/", "https://ddinstagram.com/"
            )
        elif link.startswith("https://instagram.com/"):
            return link.replace("https://instagram.com/", "https://ddinstagram.com/")
        return None
