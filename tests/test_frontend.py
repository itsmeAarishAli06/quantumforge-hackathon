from io import BytesIO

from PIL import Image

from app import validate_image
from common.schemas import MedicineDetails, VerificationStatus
from ui.demo_service import DemoServiceError, extract_demo_details, screen_demo


def image_bytes(image_format="PNG"):
    buffer = BytesIO()
    Image.new("RGB", (12, 12), "white").save(buffer, format=image_format)
    return buffer.getvalue()


def test_demo_extraction_is_fixed_and_explicitly_synthetic():
    first = extract_demo_details()
    second = extract_demo_details()
    assert first == second
    assert first.extraction_method == "demo_fixture"
    assert "DEMO ONLY" in first.medicine_name
    assert "not analyzed" in first.extraction_notes[0]


def test_demo_service_returns_all_four_schema_valid_scenarios():
    details = MedicineDetails(medicine_name="User entered example")
    for status in VerificationStatus:
        result = screen_demo(details, status.value)
        assert result.status is status
        if status == VerificationStatus.ALERT_MATCH:
            evidence = result.matching_alerts[0].alert
            assert "SYNTHETIC" in evidence.source_title
            assert "example.org" in str(evidence.source_url)
        else:
            assert not result.matching_alerts


def test_unknown_scenario_is_rejected():
    try:
        screen_demo(MedicineDetails(), "REAL_LOOKUP")
    except DemoServiceError:
        pass
    else:
        raise AssertionError("unknown scenarios must not be accepted")


def test_upload_validation_accepts_supported_image_and_rejects_invalid_bytes():
    valid, message, dimensions = validate_image(image_bytes("PNG"))
    assert valid and not message and dimensions == (12, 12)
    valid, message, dimensions = validate_image(b"not an image")
    assert not valid and message and dimensions is None


def test_empty_upload_is_rejected_without_exception():
    valid, message, dimensions = validate_image(b"")
    assert not valid
    assert "empty" in message
    assert dimensions is None


def test_upload_validation_rejects_unsupported_decoded_format():
    valid, message, _ = validate_image(image_bytes("GIF"))
    assert not valid
    assert "Unsupported" in message
