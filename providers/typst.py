import logging
from .provider import MathProvider
import hashlib
import typst

PPI = 300.0

TYPST_HEADER = """
#set page(
    width: auto,
    height: auto,
    margin: 2pt,
    fill: rgb("070709"),
)
#set text(fill: white)

"""

logger = logging.getLogger(__name__)


class TypstProvider(MathProvider):
    """MathProvider implementation for Typst rendering"""

    def evaluate(self, expression: str) -> tuple[bytes, str] | None:
        """Render typst expression to PNG using Typst"""

        try:
            logger.debug(f"Received expression: {expression!r}")
            # Remove $$ delimiters if present
            typst = expression.strip()
            if typst.startswith("$$") and typst.endswith("$$"):
                typst = typst[1:-1].strip()
            # Remove \n
            typst = typst.replace("\n", " ").strip()
            logger.debug(f"Sanitized typst: {typst!r}")

            # Prepend Typst header
            typst_with_header = TYPST_HEADER + typst
            # Convert typst to bytes
            typst_bytes = typst_with_header.encode()
            logger.debug(f"typst with header as bytes: {typst_bytes}")

            # Generate hash for filename
            formula_hash = hashlib.md5(typst.encode()).hexdigest()[:8]
            filename = f"typst-{formula_hash}.png"
            logger.debug(f"Generated filename: {filename}")

            # Compile Typst to PNG
            png_bytes = typst.compile(typst_bytes, output=None, format="png", ppi=PPI)
            if png_bytes:
                logger.debug(
                    f"PNG bytes generated for {filename}, size: {len(png_bytes)} bytes"
                )
                return (png_bytes, filename)
            logger.warning(f"No PNG bytes returned for expression: {typst!r}")
            return None
        except Exception as e:
            logger.error(f"Error rendering expression: {expression!r}", exc_info=e)
            return None
