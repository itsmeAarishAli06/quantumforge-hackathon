"""Unit tests for elite UI/UX enhancements and medical safety components."""

from datetime import date
from io import BytesIO
from pathlib import Path
from PIL import Image
import pytest

from common.schemas import (
    AlertRecord,
    AlertType,
    MatchedAlert,
    MedicineDetails,
    VerificationResult,
    VerificationStatus,
)
from streamlit.testing.v1 import AppTest
from ui.demo_service import screen_demo
from ui.components import (
    render_about_page,
    render_alert_intelligence,
    render_overview_dashboard,
    render_result,
    render_safety_guidance,
    render_top_navbar,
)


def sample_details() -> MedicineDetails:
    return MedicineDetails(
        medicine_name="Augmentin 625mg",
        generic_name="Co-Amoxiclav",
        strength="625 mg",
        batch_number="YT9D",
        expiry_date=date(2027, 1, 1),
    )


def test_screening_report_content_integrity():
    details = sample_details()
    result = screen_demo(details, "ALERT_MATCH")

    # Verify result invariants
    assert result.status == VerificationStatus.ALERT_MATCH
    assert len(result.matching_alerts) > 0
    match = result.matching_alerts[0]
    assert match.alert.validation_status == "validated"
    assert "example.org" in str(match.alert.source_url)


def test_no_match_preserves_safety_invariants():
    details = sample_details()
    result = screen_demo(details, "NO_MATCH_FOUND")

    assert result.status == VerificationStatus.NO_MATCH_FOUND
    assert not result.matching_alerts
    # Must not contain authentic or safe claims
    assert "safe" not in result.recommended_next_step.lower() or "not" in result.recommended_next_step.lower()


def test_verification_required_status_details():
    details = MedicineDetails(medicine_name="Incomplete medicine")
    result = screen_demo(details, "VERIFICATION_REQUIRED")

    assert result.status == VerificationStatus.VERIFICATION_REQUIRED
    assert result.manual_review_required is True


def test_navigation_views_render_in_apptest():
    app_path = Path(__file__).resolve().parents[1] / "app.py"
    at = AppTest.from_file(app_path, default_timeout=10).run()
    assert not at.exception

    # Default is Check Medicine
    assert any("Upload medicine packaging" in item.value for item in at.markdown)

    # Switch to Overview via top nav radio
    at.radio(key="top_nav_radio").set_value("Overview").run()
    assert not at.exception
    assert any("A clearer way to check medicine alerts" in item.value for item in at.markdown)

    # Switch to Alert Intelligence
    at.radio(key="top_nav_radio").set_value("Alert Intelligence").run()
    assert not at.exception
    assert any("DRAP Alert Intelligence" in item.value for item in at.markdown)

    # Switch to About Dawa-Muhafiz
    at.radio(key="top_nav_radio").set_value("About Dawa-Muhafiz").run()
    assert not at.exception
    assert any("About Dawa-Muhafiz" in item.value for item in at.markdown)
