from .provider import LinkProvider


class TwitterProvider(LinkProvider):
    """Substitutes twitter.com domain to fxtwitter.com and x.com to fixupx.com"""

    @property
    def has_privacy_link(self) -> bool:
        return True

    def has_link(self, link: str) -> bool:
        return "twitter.com/" in link or "x.com/" in link

    def rewrite_link(self, link: str) -> str | None:
        out = link
        if out.startswith("https://www.twitter.com/"):
            out = out.replace("https://www.twitter.com/", "https://fxtwitter.com/")
        elif out.startswith("https://twitter.com/"):
            out = out.replace("https://twitter.com/", "https://fxtwitter.com/")

        if out.startswith("https://www.x.com/"):
            out = out.replace("https://www.x.com/", "https://fixupx.com/")
        elif out.startswith("https://x.com/"):
            out = out.replace("https://x.com/", "https://fixupx.com/")

        if out == link:
            return None
        return out

    def rewrite_privacy_link(self, link: str) -> str | None:
        out = link
        if out.startswith("https://www.twitter.com/"):
            out = out.replace("https://www.twitter.com/", "https://nitter.net/")
        elif out.startswith("https://twitter.com/"):
            out = out.replace("https://twitter.com/", "https://nitter.net/")

        if out.startswith("https://www.x.com/"):
            out = out.replace("https://www.x.com/", "https://nitter.net/")
        elif out.startswith("https://x.com/"):
            out = out.replace("https://x.com/", "https://nitter.net/")

        if out == link:
            return None
        return out
