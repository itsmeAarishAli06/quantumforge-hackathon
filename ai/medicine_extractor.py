"""Validated medicine-package extraction service."""

from datetime import date
from typing import Protocol

from pydantic import ValidationError

from ai.config import get_extraction_settings
from ai.errors import ExtractionError, ProviderConfigurationError
from ai.extraction_schema import MedicineExtractionPayload
from ai.image_processing import validate_image_bytes
from ai.vision_provider import GeminiVisionProvider
from common.schemas import MedicineDetails


class PayloadProvider(Protocol):
    def extract_payload(self, image_bytes: bytes, mime_type: str) -> MedicineExtractionPayload: ...


DATE_FIELDS = ("manufacturing_date", "expiry_date")
KNOWN_FIELDS = set(MedicineExtractionPayload.model_fields)


def _to_date(value: str | None, field: str, notes: list[str], unreadable: list[str]) -> date | None:
    if value is None or not value.strip():
        return None
    original = value.strip()
    try:
        return date.fromisoformat(original)
    except ValueError:
        unreadable.append(field)
        notes.append(f"{field} was visible but could not be safely parsed as YYYY-MM-DD: {original}")
        return None


def _build_medicine_details(payload: MedicineExtractionPayload, model: str) -> MedicineDetails:
    values = payload.model_dump()
    notes = list(payload.extraction_notes)
    unreadable = list(payload.unreadable_fields)
    for field in DATE_FIELDS:
        values[field] = _to_date(values[field], field, notes, unreadable)
    unknown_unreadable = sorted(set(unreadable) - KNOWN_FIELDS)
    if unknown_unreadable:
        raise ExtractionError("invalid_provider_output", "The extraction response included an unknown field status. Please retry.")
    values["unreadable_fields"] = list(dict.fromkeys(unreadable))
    values["extraction_notes"] = notes
    values["extraction_method"] = f"gemini:{model}"
    values["requires_manual_review"] = True
    try:
        return MedicineDetails.model_validate(values)
    except ValidationError as exc:
        raise ExtractionError("invalid_provider_output", "The extracted details did not pass validation. Please retry or enter details manually.") from exc


def extract_medicine_details(
    image_bytes: bytes,
    *,
    provider: PayloadProvider | None = None,
    api_key: str | None = None,
    model: str | None = None,
    max_upload_bytes: int | None = None,
) -> MedicineDetails:
    """Extract visible package fields from image bytes; never verify medicine safety."""
    settings = get_extraction_settings()
    resolved_key = api_key if api_key is not None else settings.api_key
    resolved_model = model or settings.model
    resolved_max = max_upload_bytes or settings.max_upload_bytes
    validated = validate_image_bytes(image_bytes, resolved_max)
    if provider is None:
        if not resolved_key:
            raise ProviderConfigurationError(
                "missing_api_key",
                "Gemini is not configured. Add GEMINI_API_KEY to your local .env file, or use the clearly labelled demo details.",
            )
        provider = GeminiVisionProvider(api_key=resolved_key, model=resolved_model, timeout_ms=settings.timeout_ms)
    try:
        payload = provider.extract_payload(image_bytes, validated.mime_type)
    except ExtractionError:
        raise
    except Exception as exc:
        raise ExtractionError("provider_error", "The vision provider could not complete extraction. Check configuration or retry later.") from exc
    if not isinstance(payload, MedicineExtractionPayload):
        raise ExtractionError("invalid_provider_output", "The vision provider returned an invalid response. Please retry.")
    return _build_medicine_details(payload, resolved_model)
