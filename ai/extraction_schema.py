"""Provider-response schema kept separate from shared application contracts."""

from pydantic import BaseModel, ConfigDict, Field


class MedicineExtractionPayload(BaseModel):
    """Constrained model response; source text is kept nullable and verbatim."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    medicine_name: str | None = None
    generic_name: str | None = None
    strength: str | None = None
    dosage_form: str | None = None
    manufacturer_name: str | None = None
    manufacturer_address: str | None = None
    batch_number: str | None = None
    manufacturing_date: str | None = None
    expiry_date: str | None = None
    registration_number: str | None = None
    barcode_value: str | None = None
    packaging_observations: list[str] = Field(default_factory=list)
    unreadable_fields: list[str] = Field(default_factory=list)
    extraction_notes: list[str] = Field(default_factory=list)
