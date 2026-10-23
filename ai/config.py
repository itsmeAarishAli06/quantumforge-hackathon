"""Environment-backed settings for the optional Gemini extraction provider."""

from dataclasses import dataclass
import os

from dotenv import load_dotenv


@dataclass(frozen=True)
class ExtractionSettings:
    api_key: str | None
    model: str
    timeout_ms: int
    max_upload_bytes: int


def get_extraction_settings() -> ExtractionSettings:
    """Load local .env values without printing or exposing credentials."""
    load_dotenv()
    return ExtractionSettings(
        api_key=os.getenv("GEMINI_API_KEY", "").strip() or None,
        model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip(),
        timeout_ms=int(os.getenv("GEMINI_TIMEOUT_MS", "30000")),
        max_upload_bytes=int(os.getenv("MAX_UPLOAD_BYTES", str(10 * 1024 * 1024))),
    )
