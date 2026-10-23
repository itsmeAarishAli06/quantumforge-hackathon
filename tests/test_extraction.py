from datetime import date
from io import BytesIO
from types import SimpleNamespace

from PIL import Image
import pytest

from ai.errors import ExtractionError, ImageValidationError, ProviderConfigurationError
from ai.extraction_schema import MedicineExtractionPayload
from ai.medicine_extractor import extract_medicine_details
from ai.vision_provider import GeminiVisionProvider
from common.schemas import MedicineDetails


class FixedProvider:
    def __init__(self, payload=None, error=None):
        self.payload = payload or MedicineExtractionPayload(
            medicine_name="Visible Product",
            generic_name="Visible ingredient",
            strength="250 mg",
            batch_number=None,
            expiry_date="2027-06-30",
            unreadable_fields=["batch_number"],
            extraction_notes=["Batch number is present but blurred."],
        )
        self.error = error
        self.calls = []

    def extract_payload(self, image_bytes, mime_type):
        self.calls.append((image_bytes, mime_type))
        if self.error:
            raise self.error
        return self.payload


def png_bytes():
    buffer = BytesIO()
    Image.new("RGB", (16, 12), "white").save(buffer, format="PNG")
    return buffer.getvalue()


def test_extraction_maps_valid_payload_and_keeps_missing_values_unknown():
    provider = FixedProvider()
    details = extract_medicine_details(png_bytes(), provider=provider, model="test-model")

    assert isinstance(details, MedicineDetails)
    assert details.medicine_name == "Visible Product"
    assert details.batch_number is None
    assert details.expiry_date == date(2027, 6, 30)
    assert details.unreadable_fields == ["batch_number"]
    assert details.extraction_method == "gemini:test-model"
    assert details.requires_manual_review is True
    assert provider.calls[0][1] == "image/png"
    assert not hasattr(details, "authenticity")


def test_unambiguous_fields_are_not_fabricated_when_payload_omits_them():
    payload = MedicineExtractionPayload(medicine_name="Only visible text")
    details = extract_medicine_details(png_bytes(), provider=FixedProvider(payload))
    assert details.batch_number is None
    assert details.expiry_date is None
    assert details.manufacturer_name is None


def test_ambiguous_date_stays_null_and_is_marked_for_review():
    payload = MedicineExtractionPayload(expiry_date="06/07/27")
    details = extract_medicine_details(png_bytes(), provider=FixedProvider(payload))
    assert details.expiry_date is None
    assert "expiry_date" in details.unreadable_fields
    assert "06/07/27" in details.extraction_notes[-1]


def test_missing_key_is_a_configuration_error_not_a_demo_fallback():
    with pytest.raises(ProviderConfigurationError, match="not configured"):
        extract_medicine_details(png_bytes(), api_key="")


@pytest.mark.parametrize("contents", [b"", b"not an image"])
def test_empty_or_corrupt_upload_is_rejected_before_provider(contents):
    provider = FixedProvider()
    with pytest.raises(ImageValidationError):
        extract_medicine_details(contents, provider=provider)
    assert not provider.calls


def test_unsupported_image_format_is_rejected():
    buffer = BytesIO()
    Image.new("RGB", (5, 5), "white").save(buffer, format="GIF")
    with pytest.raises(ImageValidationError, match="JPG or PNG"):
        extract_medicine_details(buffer.getvalue(), provider=FixedProvider())


def test_oversized_upload_is_rejected():
    with pytest.raises(ImageValidationError, match="upload limit"):
        extract_medicine_details(png_bytes(), provider=FixedProvider(), max_upload_bytes=20)


def test_malformed_provider_payload_is_an_error_not_partial_success():
    with pytest.raises(ExtractionError, match="invalid response"):
        extract_medicine_details(png_bytes(), provider=FixedProvider(payload={"unsafe_field": True}))


def test_provider_outage_is_returned_as_safe_extraction_error():
    with pytest.raises(ExtractionError, match="could not complete extraction") as error:
        extract_medicine_details(png_bytes(), provider=FixedProvider(error=ConnectionError("secret/raw response")))
    assert "secret/raw response" not in str(error.value)


def test_gemini_adapter_uses_structured_schema_and_inline_image_without_network():
    payload = MedicineExtractionPayload(medicine_name="Structured product")

    class Models:
        def __init__(self):
            self.kwargs = None

        def generate_content(self, **kwargs):
            self.kwargs = kwargs
            return SimpleNamespace(parsed=payload, text=payload.model_dump_json())

    class FakeClient:
        def __init__(self):
            self.models = Models()

        def close(self):
            raise AssertionError("injected clients are caller-owned")

    client = FakeClient()
    provider = GeminiVisionProvider("unit-test-key", "test-model", client=client)
    result = provider.extract_payload(png_bytes(), "image/png")

    assert result == payload
    assert client.models.kwargs["model"] == "test-model"
    assert client.models.kwargs["config"].response_schema is MedicineExtractionPayload
    assert client.models.kwargs["config"].response_mime_type == "application/json"


def test_gemini_adapter_maps_rate_limit_without_exposing_provider_details():
    class RateLimitError(Exception):
        code = 429

    class FakeClient:
        class Models:
            def generate_content(self, **kwargs):
                raise RateLimitError("sensitive provider response")

        models = Models()

    provider = GeminiVisionProvider("test-key", "test-model", client=FakeClient())
    with pytest.raises(ExtractionError, match="rate limited") as error:
        provider.extract_payload(png_bytes(), "image/png")
    assert error.value.code == "provider_rate_limit"
    assert "sensitive provider response" not in str(error.value)


@pytest.mark.parametrize(
    ("provider_exception", "expected_code", "message_fragment"),
    [
        (type("AuthFailure", (Exception,), {"code": 403}), "provider_auth", "authenticate"),
        (type("ServiceFailure", (Exception,), {"code": 503}), "provider_unavailable", "temporarily unavailable"),
        (TimeoutError("sensitive timeout details"), "provider_timeout", "too long"),
    ],
)
def test_gemini_adapter_classifies_common_provider_failures(provider_exception, expected_code, message_fragment):
    class FakeClient:
        class Models:
            def generate_content(self, **kwargs):
                exc = provider_exception() if isinstance(provider_exception, type) else provider_exception
                raise exc

        models = Models()

    provider = GeminiVisionProvider("test-key", "test-model", client=FakeClient())
    with pytest.raises(ExtractionError, match=message_fragment) as error:
        provider.extract_payload(png_bytes(), "image/png")
    assert error.value.code == expected_code
