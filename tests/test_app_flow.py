from pathlib import Path
from io import BytesIO

from PIL import Image
import pytest

from streamlit.testing.v1 import AppTest


@pytest.fixture(autouse=True)
def disable_external_provider_key(monkeypatch):
    """Keep UI tests offline even when a developer has a local .env key."""
    monkeypatch.setenv("GEMINI_API_KEY", "")


def run_app():
    app_path = Path(__file__).resolve().parents[1] / "app.py"
    return AppTest.from_file(app_path, default_timeout=10).run()


def test_app_imports_and_renders_without_exceptions():
    at = run_app()
    assert not at.exception
    assert any("Gemini is not configured" in item.value for item in at.info)


def test_valid_image_upload_shows_preview_feedback_and_unlocks_demo_fill():
    buffer = BytesIO()
    Image.new("RGB", (8, 8), "white").save(buffer, format="PNG")
    at = run_app()
    at.file_uploader[0].upload("sample.png", buffer.getvalue(), "image/png").run()
    assert not at.exception
    assert any("Image validated: sample.png" in item.value for item in at.success)
    assert at.button(key="extract_demo").disabled is False


def test_replacing_image_clears_extracted_values_and_results():
    def make_png(color):
        buffer = BytesIO()
        Image.new("RGB", (8, 8), color).save(buffer, format="PNG")
        return buffer.getvalue()

    at = run_app()
    at.file_uploader[0].upload("first.png", make_png("white"), "image/png").run()
    at.button(key="extract_demo").click().run()
    assert "DEMO ONLY" in at.text_input(key="detail_medicine_name").value

    at.file_uploader[0].upload("second.png", make_png("black"), "image/png").run()
    assert at.text_input(key="detail_medicine_name").value == ""
    assert not any("SYNTHETIC DEMO DETAILS" in item.value for item in at.info)


def test_each_synthetic_result_state_renders_in_ui():
    at = run_app()
    for scenario, expected in (
        ("ALERT_MATCH", "ALERT MATCH"),
        ("VERIFICATION_REQUIRED", "VERIFICATION REQUIRED"),
        ("NO_MATCH_FOUND", "NO MATCH FOUND in the synthetic demo dataset"),
        ("ERROR", "The demo screening could not be completed"),
    ):
        at.selectbox[0].select(scenario).run()
        at.button(key="preview_screening").click().run()
        visible = "\n".join(
            item.value
            for group in (at.markdown, at.error, at.warning, at.info, at.success, at.caption)
            for item in group
        )
        assert expected in visible
        assert not at.exception


def test_editing_details_clears_old_screening_result():
    at = run_app()
    at.selectbox[0].select("NO_MATCH_FOUND").run()
    at.button(key="preview_screening").click().run()
    assert any("NO MATCH FOUND in the synthetic demo dataset" in item.value for item in at.info)

    at.text_input(key="detail_medicine_name").set_value("Edited after screening").run()
    assert any("Details changed after this result" in item.value for item in at.warning)
    assert not any("NO MATCH FOUND in the synthetic demo dataset" in item.value for item in at.info)


def test_screening_error_is_not_rendered_as_no_match():
    at = run_app()
    at.selectbox[0].select("ERROR").run()
    at.button(key="preview_screening").click().run()
    assert any("could not be completed" in item.value for item in at.error)
    assert not any("NO MATCH FOUND" in item.value for item in at.info)


def test_clear_workflow_removes_details_and_result():
    at = run_app()
    at.text_input(key="detail_medicine_name").set_value("Typed test value").run()
    at.selectbox[0].select("NO_MATCH_FOUND").run()
    at.button(key="preview_screening").click().run()
    at.button[0].click().run()

    assert not at.exception
    assert at.text_input(key="detail_medicine_name").value == ""
    assert not any("NO MATCH FOUND" in item.value for item in at.info)
