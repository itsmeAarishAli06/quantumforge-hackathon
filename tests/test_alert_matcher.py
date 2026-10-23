"""Unit tests for the deterministic DRAP alert verification engine."""

from datetime import date
from pathlib import Path
import pytest

from common.schemas import (
    AlertRecord,
    AlertType,
    MedicineDetails,
    VerificationStatus,
)
from verification.alert_matcher import (
    _check_conflicts,
    _token_match,
    check_drap_alerts,
    normalize_batch,
    normalize_strength,
    normalize_text,
)


def test_normalize_text():
    assert normalize_text("Brexin® Tablets 20mg") == "brexin tablets 20mg"
    assert normalize_text("  DANZEN   DS   ") == "danzen ds"
    assert normalize_text("Capsule / CARICEF-500") == "capsule caricef 500"
    assert normalize_text("") == ""
    assert normalize_text(None) == ""


def test_normalize_batch():
    assert normalize_batch("1207863") == "1207863"
    assert normalize_batch("  B.No. 4476 ") == "4476"
    assert normalize_batch("Batch: 518C27") == "518c27"
    assert normalize_batch("Lot# MT25-331") == "mt25-331"
    assert normalize_batch("") == ""
    assert normalize_batch(None) == ""


def test_normalize_strength():
    assert normalize_strength(" 20 mg ") == "20mg"
    assert normalize_strength("500 mg / 10 ml") == "500mg/10ml"
    assert normalize_strength("") == ""
    assert normalize_strength(None) == ""


def test_token_match():
    assert _token_match("Brexin Tablets 20mg", "Brexin Tablets 20 mg") is True
    assert _token_match("Danzen DS", "DANZEN DS Tablets") is True
    assert _token_match("Panadol", "Brexin Tablets") is False
    assert _token_match("", "Brexin") is False


def test_conflict_detection():
    alert = AlertRecord(
        alert_id="TEST-01",
        alert_type=AlertType.RAPID_ALERT,
        product_name="Sample Med",
        strength="500mg",
        dosage_form="Tablet",
        source_title="DRAP",
        source_url="https://dra.gov.pk/test",
        supporting_excerpt="Substandard sample",
        validation_status="validated",
        reviewed_at=date(2026, 1, 1),
    )

    # Matching details
    ok_details = MedicineDetails(medicine_name="Sample Med", strength="500mg", dosage_form="Tablet")
    assert not _check_conflicts(ok_details, alert)

    # Conflicting strength
    bad_strength = MedicineDetails(medicine_name="Sample Med", strength="250mg", dosage_form="Tablet")
    conflicts = _check_conflicts(bad_strength, alert)
    assert any("Strength mismatch" in c for c in conflicts)

    # Conflicting dosage form
    bad_form = MedicineDetails(medicine_name="Sample Med", strength="500mg", dosage_form="Syrup")
    conflicts = _check_conflicts(bad_form, alert)
    assert any("Dosage form mismatch" in c for c in conflicts)


def test_exact_batch_match_produces_alert_match():
    details = MedicineDetails(
        medicine_name="Brexin Tablets 20 mg",
        batch_number="1207863",
    )
    result = check_drap_alerts(details)
    assert result.status == VerificationStatus.ALERT_MATCH
    assert len(result.matching_alerts) >= 1
    match = result.matching_alerts[0]
    assert match.alert.alert_id == "DRAP-ALERT-2026-31"
    assert match.alert.validation_status == "validated"
    assert "dra.gov.pk" in str(match.alert.source_url)
    assert "quarantine" in result.recommended_next_step.lower() or "not consume" in result.recommended_next_step.lower()


def test_batch_mismatch_returns_no_match():
    # Brexin alert is for batch 1207863; testing with a different batch
    details = MedicineDetails(
        medicine_name="Brexin Tablets 20 mg",
        batch_number="DIFFERENT-BATCH-999",
    )
    result = check_drap_alerts(details)
    assert result.status == VerificationStatus.NO_MATCH_FOUND
    assert len(result.matching_alerts) == 0
    # Must preserve medical boundary: no match does NOT prove safety
    assert "not confirm" in result.recommended_next_step.lower() or "does not" in result.recommended_next_step.lower()


def test_missing_batch_on_batch_specific_alert_returns_verification_required():
    # Brexin has an alert for batch 1207863, but submitted packaging omits batch number
    details = MedicineDetails(
        medicine_name="Brexin Tablets 20 mg",
        batch_number=None,
    )
    result = check_drap_alerts(details)
    assert result.status == VerificationStatus.VERIFICATION_REQUIRED
    assert result.manual_review_required is True
    assert any("missing a batch number" in note for note in result.missing_or_uncertain_information)


def test_product_wide_alert_matches_regardless_of_batch():
    # Zetol Germ Protection Liquid has batch_number = None (all batches affected)
    details = MedicineDetails(
        medicine_name="Zetol Germ Protection Liquid",
        batch_number="ANY_BATCH_456",
    )
    result = check_drap_alerts(details)
    assert result.status == VerificationStatus.ALERT_MATCH
    assert any(m.alert.product_name == "Zetol Germ Protection Liquid" for m in result.matching_alerts)


def test_unrelated_medicine_returns_no_match():
    details = MedicineDetails(
        medicine_name="Completely Unrelated Safe Medicine 500mg",
        batch_number="XYZ12345",
    )
    result = check_drap_alerts(details)
    assert result.status == VerificationStatus.NO_MATCH_FOUND
    assert not result.matching_alerts
    assert result.dataset_record_count > 0


def test_empty_details_returns_verification_required():
    details = MedicineDetails(
        medicine_name=None,
        batch_number=None,
    )
    result = check_drap_alerts(details)
    assert result.status == VerificationStatus.VERIFICATION_REQUIRED
    assert "medicine_name" in result.missing_or_uncertain_information


def test_corrupted_database_returns_error_not_no_match(tmp_path):
    corrupt_db = tmp_path / "corrupt.db"
    corrupt_db.write_text("NOT A SQLITE DATABASE", encoding="utf-8")

    details = MedicineDetails(medicine_name="Brexin", batch_number="1207863")
    result = check_drap_alerts(details, db_path=corrupt_db)

    assert result.status == VerificationStatus.ERROR
    assert result.error_code == "DB_UNAVAILABLE"
    assert result.dataset_record_count == 0


def test_real_verification_flow_in_app():
    from streamlit.testing.v1 import AppTest

    app_path = Path(__file__).resolve().parents[1] / "app.py"
    at = AppTest.from_file(app_path, default_timeout=10).run()

    # Enter Brexin details with exact affected batch 1207863
    at.text_input(key="detail_medicine_name").set_value("Brexin Tablets 20mg").run()
    at.text_input(key="detail_batch_number").set_value("1207863").run()

    # Click the real verification button
    at.button(key="execute_real_verification").click().run()

    visible = "\n".join(
        item.value
        for group in (at.markdown, at.error, at.warning, at.info, at.success, at.caption)
        for item in group
    )

    assert "DRAP-ALERT-2026-31" in visible
    assert "ALERT MATCH" in visible
    assert not at.exception


def test_batch_prefix_and_case_insensitivity():
    details = MedicineDetails(
        medicine_name="BREXIN 20MG",
        batch_number="b.no. 1207863",
    )
    result = check_drap_alerts(details)
    assert result.status == VerificationStatus.ALERT_MATCH
    assert len(result.matching_alerts) == 1
    assert result.matching_alerts[0].alert.alert_id == "DRAP-ALERT-2026-31"


def test_dosage_form_conflict_yields_verification_required():
    # Brexin alert is for Tablets, but submission specifies Syrup
    details = MedicineDetails(
        medicine_name="Brexin",
        batch_number="1207863",
        dosage_form="Syrup",
    )
    result = check_drap_alerts(details)
    assert result.status == VerificationStatus.VERIFICATION_REQUIRED
    assert any("Dosage form mismatch" in note for note in result.missing_or_uncertain_information)


def test_active_ingredient_match():
    # Active ingredient matches alert generic_name
    details = MedicineDetails(
        generic_name="Piroxicam",
        batch_number="1207863",
    )
    result = check_drap_alerts(details)
    assert result.status == VerificationStatus.ALERT_MATCH
    assert result.matching_alerts[0].alert.alert_id == "DRAP-ALERT-2026-31"


def test_real_verification_no_match_in_app():
    from streamlit.testing.v1 import AppTest

    app_path = Path(__file__).resolve().parents[1] / "app.py"
    at = AppTest.from_file(app_path, default_timeout=10).run()

    at.text_input(key="detail_medicine_name").set_value("Unrelated Product").run()
    at.text_input(key="detail_batch_number").set_value("BATCH-SAFE-999").run()

    at.button(key="execute_real_verification").click().run()

    visible = "\n".join(
        item.value
        for group in (at.markdown, at.error, at.warning, at.info, at.success, at.caption)
        for item in group
    )

    assert "NO MATCH FOUND in the validated DRAP alert database" in visible
    assert "DOES NOT confirm that the medicine is genuine" in visible
    assert not at.exception
