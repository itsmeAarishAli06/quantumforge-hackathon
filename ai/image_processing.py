"""Safe in-memory image validation shared by the UI and extraction service."""

from dataclasses import dataclass
from io import BytesIO
import warnings

from PIL import Image, UnidentifiedImageError

from ai.errors import ImageValidationError


MAX_IMAGE_PIXELS = 20_000_000


@dataclass(frozen=True)
class ValidatedImage:
    mime_type: str
    width: int
    height: int


def validate_image_bytes(data: bytes, max_bytes: int = 10 * 1024 * 1024) -> ValidatedImage:
    """Validate actual encoded format and bounds without persisting image bytes."""
    if not data:
        raise ImageValidationError("empty_image", "The uploaded file is empty.")
    if max_bytes <= 0 or len(data) > max_bytes:
        raise ImageValidationError("image_too_large", f"Image exceeds the {max(1, max_bytes // (1024 * 1024))} MB upload limit.")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(BytesIO(data)) as image:
                if image.format not in {"JPEG", "PNG"}:
                    raise ImageValidationError("unsupported_format", "Use a JPG or PNG image.")
                width, height = image.size
                if width < 1 or height < 1 or width * height > MAX_IMAGE_PIXELS:
                    raise ImageValidationError("image_dimensions", "Image dimensions exceed the safe processing limit.")
                image_format = image.format
                image.verify()
    except ImageValidationError:
        raise
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError, Image.DecompressionBombWarning, ValueError) as exc:
        raise ImageValidationError("invalid_image", "This image could not be decoded. Try a clear JPG or PNG.") from exc
    mime_type = "image/jpeg" if image_format == "JPEG" else "image/png"
    return ValidatedImage(mime_type=mime_type, width=width, height=height)


def validate_and_prepare_image(image_path):
    """Legacy path interface; validates a path without copying or modifying it."""
    from pathlib import Path

    path = Path(image_path)
    if not path.is_file():
        raise ImageValidationError("image_not_found", "The selected image is no longer available. Upload it again.")
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise ImageValidationError("image_read_error", "The selected image could not be read.") from exc
    validate_image_bytes(data)
    return path
