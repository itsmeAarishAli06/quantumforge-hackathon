"""Provider-neutral contract for a future configurable vision integration."""

from pathlib import Path
from typing import Protocol

from common.schemas import MedicineDetails


class VisionProvider(Protocol):
    """Adapter contract. Implementations must return structured data only."""

    def extract(self, image_path: Path) -> MedicineDetails:
        """Read visible packaging fields; never infer safety or authenticity."""
        ...
