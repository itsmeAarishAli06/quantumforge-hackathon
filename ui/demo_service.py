"""Deterministic synthetic fixtures for the frontend phase only.

This module never calls an external provider, reads the uploaded image, or
implements product/batch matching. All generated results are demo scenarios.
"""

from datetime import date

from common.schemas import (
    AlertRecord,
    AlertType,
    MatchedAlert,
    MedicineDetails,
    VerificationResult,
    VerificationStatus,
)


class DemoServiceError(ValueError):
    """Raised when an unsupported demo scenario is selected."""


def extract_demo_details() -> MedicineDetails:
    """Return fixed synthetic values unrelated to any uploaded image."""
    return MedicineDetails(
        medicine_name="DEMO ONLY — Sample Medicine",
        generic_name="DEMO ONLY — Example ingredient",
        strength="DEMO ONLY — 250 mg",
        dosage_form="DEMO ONLY — tablet",
        manufacturer_name="DEMO ONLY — Example Manufacturer",
        manufacturer_address="DEMO ONLY — Example address",
        batch_number="DEMO ONLY — SAMPLE-000",
        manufacturing_date=date(2025, 1, 1),
        expiry_date=date(2027, 1, 1),
        registration_number="DEMO ONLY — NOT A REGISTRATION NUMBER",
        barcode_value=None,
        packaging_observations=["Synthetic fixture; not extracted from the uploaded image."],
        unreadable_fields=[],
        extraction_notes=["Demo values only. The uploaded image was not analyzed."],
        extraction_method="demo_fixture",
        requires_manual_review=True,
    )


def screen_demo(details: MedicineDetails, scenario: str) -> VerificationResult:
    """Build a schema-valid synthetic scenario; no comparison is performed."""
    try:
        status = VerificationStatus(scenario)
    except ValueError as exc:
        raise DemoServiceError("Unknown demo scenario.") from exc

    result_values = {
        "status": status,
        "medicine_details": details,
        "recommended_next_step": "Demo only: confirm packaging details and consult a qualified pharmacist if concerned.",
        "manual_review_required": True,
        "dataset_record_count": 1 if status == VerificationStatus.ALERT_MATCH else 0,
    }
    if status == VerificationStatus.ALERT_MATCH:
        synthetic_alert = AlertRecord(
            alert_id="SYNTHETIC-DEMO-ONLY",
            alert_type=AlertType.RAPID_ALERT,
            product_name="SYNTHETIC DEMO PRODUCT",
            source_title="SYNTHETIC DEMO EVIDENCE — not a DRAP document",
            source_url="https://example.org/synthetic-demo-only",
            supporting_excerpt="Synthetic UI fixture only. No real alert or affected product is represented.",
            validation_status="validated",
            reviewed_at=date(2026, 1, 1),
        )
        result_values["matching_alerts"] = [
            MatchedAlert(alert=synthetic_alert, match_reasons=["Synthetic scenario selected by user; no matching was performed."])
        ]
        result_values["match_reasons"] = ["Synthetic scenario selected; not a real match."]
    elif status == VerificationStatus.VERIFICATION_REQUIRED:
        result_values["missing_or_uncertain_information"] = ["batch_number", "manual review"]
    elif status == VerificationStatus.ERROR:
        result_values["error_code"] = "DEMO_SIMULATED_ERROR"
    elif status == VerificationStatus.NO_MATCH_FOUND:
        result_values["recommended_next_step"] = (
            "No match in this synthetic demo dataset. This does not confirm authenticity, approval, or safety."
        )
    return VerificationResult(**result_values)
