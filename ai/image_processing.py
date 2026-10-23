"""Planned image validation boundary; no decoding or preprocessing yet.

Future responsibilities: enforce size/type/pixel limits, decode safely, and
prepare a temporary image without persisting user uploads by default.
"""

from pathlib import Path


def validate_and_prepare_image(image_path: str | Path) -> Path:
    """Validate and prepare an image. Implementation is deferred."""
    raise NotImplementedError("Image processing is planned, not implemented yet.")
