from pathlib import Path

from streamlit.testing.v1 import AppTest


def run_app():
    app_path = Path(__file__).resolve().parents[1] / "app.py"
    return AppTest.from_file(app_path, default_timeout=10).run()


def test_app_imports_and_renders_without_exceptions():
    at = run_app()
    assert not at.exception
    assert any("DEMO MODE" in item.value for item in at.info)


def test_each_synthetic_result_state_renders_in_ui():
    at = run_app()
    for scenario, expected in (
        ("ALERT_MATCH", "ALERT MATCH"),
        ("VERIFICATION_REQUIRED", "VERIFICATION REQUIRED"),
        ("NO_MATCH_FOUND", "NO MATCH FOUND in the synthetic demo dataset"),
        ("ERROR", "The demo screening could not be completed"),
    ):
        at.selectbox[0].select(scenario).run()
        at.button[2].click().run()
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
    at.button[2].click().run()
    assert any("NO MATCH FOUND in the synthetic demo dataset" in item.value for item in at.info)

    at.text_input(key="detail_medicine_name").set_value("Edited after screening").run()
    assert any("details changed after screening" in item.value for item in at.warning)
    assert not any("NO MATCH FOUND in the synthetic demo dataset" in item.value for item in at.info)


def test_screening_error_is_not_rendered_as_no_match():
    at = run_app()
    at.selectbox[0].select("ERROR").run()
    at.button[2].click().run()
    assert any("could not be completed" in item.value for item in at.error)
    assert not any("NO MATCH FOUND" in item.value for item in at.info)


def test_clear_workflow_removes_details_and_result():
    at = run_app()
    at.text_input(key="detail_medicine_name").set_value("Typed test value").run()
    at.selectbox[0].select("NO_MATCH_FOUND").run()
    at.button[2].click().run()
    at.button[0].click().run()

    assert not at.exception
    assert at.text_input(key="detail_medicine_name").value == ""
    assert not any("NO MATCH FOUND" in item.value for item in at.info)
