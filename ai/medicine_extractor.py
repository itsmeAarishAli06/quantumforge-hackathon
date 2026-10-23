"""Future orchestration boundary for image processing and field extraction."""

from pathlib import Path

from common.schemas import MedicineDetails


def extract_medicine_details(image_path: str | Path) -> MedicineDetails:
    """Return schema-validated visible details; extraction is not implemented."""
    raise NotImplementedError("Medicine detail extraction is planned, not implemented yet.")
