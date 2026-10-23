"""Unit tests for the multilingual localization layer (English, Urdu, Sindhi)."""

import pytest
from ui.i18n import LANGUAGES, MESSAGES, is_rtl, t


def test_supported_languages_are_defined():
    assert "en" in LANGUAGES
    assert "ur" in LANGUAGES
    assert "sd" in LANGUAGES


def test_core_translation_keys_exist_in_all_languages():
    essential_keys = [
        "app_title",
        "app_tagline",
        "app_subtitle",
        "step_1_title",
        "step_2_title",
        "step_3_title",
        "safety_disclaimer_title",
        "safety_disclaimer_text",
        "upload_section_title",
        "extract_section_title",
        "screen_section_title",
        "status_alert_match_title",
        "status_verification_req_title",
        "status_no_match_title",
        "status_error_title",
        "report_title",
    ]
    for lang in ("en", "ur", "sd"):
        for key in essential_keys:
            assert key in MESSAGES[lang], f"Missing key '{key}' in language '{lang}'"
            assert len(MESSAGES[lang][key]) > 0


def test_rtl_detection():
    assert is_rtl("ur") is True
    assert is_rtl("sd") is True
    assert is_rtl("en") is False
    assert is_rtl("unknown") is False


def test_t_function_formats_kwargs_and_falls_back():
    formatted = t("upload_success", "en", name="panadol.png", size=45, width=800, height=600)
    assert "panadol.png" in formatted
    assert "45 KB" in formatted

    # Fallback to English if non-existent language
    assert t("app_title", "fr") == "Dawa-Muhafiz"

    # Fallback to key if non-existent key
    assert t("non_existent_key_xyz", "en") == "non_existent_key_xyz"
