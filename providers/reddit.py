from .provider import LinkProvider


class RedditProvider(LinkProvider):
    """Substitutes reddit.com domain to rxddit.com"""

    @property
    def has_privacy_link(self) -> bool:
        return True

    def has_link(self, link: str) -> bool:
        return "reddit.com/" in link

    def rewrite_link(self, link: str) -> str | None:
        if link.startswith("https://www.reddit.com/"):
            return link.replace("https://www.reddit.com/", "https://rxddit.com/")
        elif link.startswith("https://reddit.com/"):
            return link.replace("https://reddit.com/", "https://rxddit.com/")
        return None

    def rewrite_privacy_link(self, link: str) -> str | None:
        if link.startswith("https://www.reddit.com/"):
            return link.replace("https://www.reddit.com/", "https://safereddit.com/")
        elif link.startswith("https://reddit.com/"):
            return link.replace("https://reddit.com/", "https://safereddit.com/")
        return None
