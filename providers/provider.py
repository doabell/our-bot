from abc import ABC, abstractmethod
from dataclasses import dataclass
import io


@dataclass
class ProcessedResult:
    """Result of processing a message"""

    type: str  # "link" or "math"
    clean_link: str | None = None  # for links
    file: io.BytesIO | None = None  # for math
    filename: str | None = None  # for math
    privacy_link: str | None = None
    success: bool = True


class LinkProvider(ABC):
    """Abstract base class for link providers
    delete_original: str
        - "never": reply to message (current behavior)
        - "link-only": delete if the message only has the link (don't reply)
        - "always": always delete (don't reply)
    """

    delete_original: str = "link-only"  # Options: "never", "link-only", "always"

    @property
    @abstractmethod
    def has_privacy_link(self) -> bool:
        """Whether there is a privacy-preserving version of the link"""
        pass

    @abstractmethod
    def has_link(self, link: str) -> bool:
        """Checks if the message contains a link from the provider"""
        pass

    @abstractmethod
    def rewrite_link(self, link: str) -> str | None:
        """Rewrites the provider's link to a format that displays the image thumbnail. Returns None on failure."""
        pass

    def rewrite_privacy_link(self, link: str) -> str | None:
        """Rewrites the provider's link to a privacy-preserving version. Returns None on failure."""
        return None

    def process_link(self, link: str) -> ProcessedResult | None:
        """Process a link and return a ProcessedResult"""
        clean_link = self.rewrite_link(link)
        if not clean_link:
            return None

        privacy_link = None
        if self.has_privacy_link:
            privacy_link = self.rewrite_privacy_link(link)

        return ProcessedResult(
            type="link",
            clean_link=clean_link,
            privacy_link=privacy_link,
            success=True,
        )


class MathProvider(ABC):
    """Abstract base class for math providers"""

    @abstractmethod
    def evaluate(self, expression: str) -> tuple[bytes, str] | None:
        """Evaluate a math expression and return (image_bytes, filename) or None"""
        pass

    def process_math(self, expression: str) -> ProcessedResult | None:
        """Process a math expression and return a ProcessedResult"""
        result = self.evaluate(expression)
        if not result:
            return None

        if isinstance(result, tuple) and len(result) == 2:
            file_content, filename = result
            if isinstance(file_content, bytes):
                file_io = io.BytesIO(file_content)
            elif isinstance(file_content, io.BytesIO):
                file_io = file_content
            else:
                return None

            return ProcessedResult(
                type="math",
                file=file_io,
                filename=filename,
                success=True,
            )

        return None
