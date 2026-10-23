from datetime import date

import pytest
from pydantic import ValidationError

from common.schemas import (
    AlertRecord,
    AlertType,
    MatchedAlert,
    MedicineDetails,
    VerificationResult,
    VerificationStatus,
)


def alert_record(**overrides):
    values = {
        "alert_id": "test-only-001",
        "alert_type": AlertType.RAPID_ALERT,
        "product_name": "Synthetic Example Product",
        "source_title": "Synthetic test fixture — not a DRAP alert",
        "source_url": "https://example.org/synthetic-test-fixture",
        "supporting_excerpt": "Synthetic fixture for schema tests only.",
        "validation_status": "validated",
        "reviewed_at": date(2026, 1, 1),
    }
    values.update(overrides)
    return AlertRecord(**values)


def test_medicine_details_accepts_optional_unknowns():
    details = MedicineDetails(medicine_name="Example", batch_number=None)
    assert details.medicine_name == "Example"
    assert details.batch_number is None


def test_alert_match_requires_validated_traceable_evidence():
    match = MatchedAlert(alert=alert_record(), match_reasons=["Synthetic exact batch match"])
    result = VerificationResult(
        status=VerificationStatus.ALERT_MATCH,
        medicine_details=MedicineDetails(medicine_name="Synthetic Example Product"),
        matching_alerts=[match],
        recommended_next_step="Review the cited synthetic fixture.",
        manual_review_required=True,
        dataset_record_count=1,
    )
    assert result.status is VerificationStatus.ALERT_MATCH
    assert "example.org" in str(result.matching_alerts[0].alert.source_url)


def test_alert_match_without_evidence_is_rejected():
    with pytest.raises(ValidationError, match="requires at least one validated alert"):
        VerificationResult(
            status=VerificationStatus.ALERT_MATCH,
            medicine_details=MedicineDetails(),
            recommended_next_step="Manual review.",
            manual_review_required=True,
            dataset_record_count=0,
        )


def test_unvalidated_alert_cannot_be_returned_as_match():
    candidate = alert_record(validation_status="candidate")
    with pytest.raises(ValidationError, match="only validated alert records"):
        MatchedAlert(alert=candidate, match_reasons=["candidate"])


def test_no_match_status_is_valid_and_not_a_safety_claim():
    result = VerificationResult(
        status="NO_MATCH_FOUND",
        medicine_details=MedicineDetails(),
        recommended_next_step="No match in available records; this does not confirm safety or authenticity.",
        manual_review_required=True,
        dataset_record_count=0,
    )
    assert result.status is VerificationStatus.NO_MATCH_FOUND


def test_invalid_status_and_missing_required_fields_are_rejected():
    with pytest.raises(ValidationError):
        VerificationResult(
            status="SAFE",
            medicine_details=MedicineDetails(),
            recommended_next_step="Review.",
            manual_review_required=True,
            dataset_record_count=0,
        )
    with pytest.raises(ValidationError):
        AlertRecord(alert_id="missing-required-fields")
