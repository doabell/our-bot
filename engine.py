from providers.typst import TypstProvider
from providers.provider import ProcessedResult
from typing import List

from providers import (
    InstagramProvider,
    TwitterProvider,
    TikTokProvider,
    RedditProvider,
    YouTubeProvider,
    BilibiliProvider,
    XHSProvider,
    GoogleMapsProvider,
)

MAX_REPLIES = 2


# Initialize all providers
providers = [
    InstagramProvider(),
    TikTokProvider(),
    GoogleMapsProvider(),
    TwitterProvider(),
    RedditProvider(),
    BilibiliProvider(),
    XHSProvider(),
    YouTubeProvider(),
]


def extract_links(text: str) -> List[str]:
    """Extract links using string search, not regex"""
    words = text.split()
    links = []
    for word in words:
        if word.startswith("http://") or word.startswith("https://"):
            # Convert http to https
            if word.startswith("http://"):
                word = "https://" + word[7:]
            links.append(word)
    return links


def extract_typst_math(text: str) -> str | None:
    """Detect Typst math blocks that start with '$$ ' and end with ' $$'
    Returns: The full math expression if valid, None otherwise
    """
    text = text.strip()

    # Check if message starts with "$$ " and ends with " $$"
    if text.startswith("$$ ") and text.endswith(" $$"):
        return text

    return None


async def process_message(text: str) -> List[ProcessedResult]:
    """Process a message and return all transformations"""
    results = []

    # Link processing
    for link in extract_links(text):
        replies = 0
        for provider in providers:
            if replies >= MAX_REPLIES:
                break
            try:
                if provider.has_link(link):
                    result = provider.process_link(link)
                    if result:
                        results.append(result)
                        replies += 1
            except Exception:
                continue

    # Typst math processing
    typst_math = extract_typst_math(text)
    if typst_math:
        provider = TypstProvider()
        try:
            result = provider.process_math(typst_math)
            if result:
                results.append(result)
        except Exception:
            pass

    # Only return successful results
    return [r for r in results if r.success]


def format_message(result: ProcessedResult) -> str:
    """Format a link result for Discord"""
    if result.privacy_link:
        return f"🔏 [Privacy Link]({result.privacy_link})\n- [Embed Link]({result.clean_link})"
    else:
        return f"🔗 [Clean Link]({result.clean_link})"
