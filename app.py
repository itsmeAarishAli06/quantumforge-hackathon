"""Dawa-Muhafiz (دوا محافظ) — Medicine Safety & Packaging Verification Assistant.

An elite, accessible digital health interface for citizens, pharmacists, and healthcare
workers in Pakistan. Extracts visible packaging text and compares it deterministically
with official DRAP rapid alerts and recalls.

Strict Medical Safety Principle:
Checks available alerts in the validated dataset; never authenticates medicine safety.
"""

from datetime import date
import hashlib

import streamlit as st
from pydantic import ValidationError

from ai.config import get_extraction_settings
from ai.errors import ExtractionError, ImageValidationError
from ai.image_processing import validate_image_bytes
from ai.medicine_extractor import extract_medicine_details
from common.schemas import MedicineDetails, VerificationResult, VerificationStatus
from ui.components import (
    render_about_page,
    render_alert_intelligence,
    render_help,
    render_overview_dashboard,
    render_photo_tips,
    render_result,
    render_safety_guidance,
    render_screening_report,
    render_top_navbar,
)
from ui.demo_service import DemoServiceError, extract_demo_details, screen_demo
from ui.i18n import LANGUAGES, is_rtl, t
from ui.styles import apply_styles
from verification.alert_matcher import check_drap_alerts
from verification.data_loader import get_dataset_metadata


DETAIL_FIELDS = {
    "Medicine name": "medicine_name",
    "Generic / active ingredient": "generic_name",
    "Strength": "strength",
    "Dosage form": "dosage_form",
    "Manufacturer": "manufacturer_name",
    "Manufacturer address": "manufacturer_address",
    "Batch / lot number": "batch_number",
    "Manufacturing date (YYYY-MM-DD)": "manufacturing_date",
    "Expiry date (YYYY-MM-DD)": "expiry_date",
    "Registration number": "registration_number",
    "Barcode value": "barcode_value",
}

FIELD_GROUPS = (
    ("Product information", ("Medicine name", "Generic / active ingredient", "Strength", "Dosage form")),
    ("Manufacturer and identification", ("Manufacturer", "Registration number", "Batch / lot number", "Manufacturer address")),
    ("Dates", ("Manufacturing date (YYYY-MM-DD)", "Expiry date (YYYY-MM-DD)")),
    ("Barcode", ("Barcode value",)),
)


def validate_image(data: bytes, max_bytes: int = 10 * 1024 * 1024) -> tuple[bool, str, tuple[int, int] | None]:
    """Return a safe validation result for in-memory JPG/PNG data."""
    try:
        image = validate_image_bytes(data, max_bytes)
        return True, "", (image.width, image.height)
    except ImageValidationError as exc:
        return False, exc.user_message, None


def _initialize_state() -> None:
    defaults = {
        "upload_version": 0,
        "active_upload_digest": None,
        "extracted": False,
        "extraction_method": None,
        "extraction_snapshot": None,
        "extraction_error": None,
        "screening_result": None,
        "screened_details": None,
        "screening_is_demo": True,
        "screening_scenario": VerificationStatus.VERIFICATION_REQUIRED.value,
        "app_language": "en",
        "active_nav": "Check Medicine",
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def _clear_workflow_data() -> None:
    for key in list(st.session_state.keys()):
        if key.startswith("detail_"):
            del st.session_state[key]
    st.session_state["extracted"] = False
    st.session_state["extraction_method"] = None
    st.session_state["extraction_snapshot"] = None
    st.session_state["extraction_error"] = None
    st.session_state["screening_result"] = None
    st.session_state["screened_details"] = None
    st.session_state["screening_is_demo"] = True


def _reset() -> None:
    _clear_workflow_data()
    st.session_state["active_upload_digest"] = None
    st.session_state["upload_version"] += 1
    st.rerun()


def _details_from_inputs() -> MedicineDetails:
    values: dict[str, object] = {}
    for label, field in DETAIL_FIELDS.items():
        value = st.session_state.get(f"detail_{field}", "")
        if field in {"manufacturing_date", "expiry_date"}:
            if value.strip():
                try:
                    values[field] = date.fromisoformat(value.strip())
                except ValueError as exc:
                    raise ValueError(f"{label} must use YYYY-MM-DD format.") from exc
            else:
                values[field] = None
        else:
            values[field] = value.strip() or None
    values["extraction_method"] = st.session_state.get("extraction_method")
    values["requires_manual_review"] = True
    return MedicineDetails(**values)


def _apply_extraction(details: MedicineDetails, method: str) -> None:
    for field in DETAIL_FIELDS.values():
        value = getattr(details, field)
        st.session_state[f"detail_{field}"] = value.isoformat() if isinstance(value, date) else (value or "")
    st.session_state["extracted"] = True
    st.session_state["extraction_method"] = method
    st.session_state["extraction_snapshot"] = details.model_dump(mode="json")
    st.session_state["extraction_error"] = None
    st.session_state["screening_result"] = None
    st.session_state["screened_details"] = None


def _sync_upload(image_bytes: bytes | None) -> None:
    digest = hashlib.sha256(image_bytes).hexdigest() if image_bytes else None
    if digest != st.session_state["active_upload_digest"]:
        _clear_workflow_data()
        st.session_state["active_upload_digest"] = digest


def _on_top_nav_change() -> None:
    val = st.session_state.get("top_nav_radio", "Check Medicine")
    st.session_state["active_nav"] = val
    st.session_state["sidebar_nav_selection"] = val


def _on_sidebar_nav_change() -> None:
    val = st.session_state.get("sidebar_nav_selection", "Check Medicine")
    st.session_state["active_nav"] = val
    st.session_state["top_nav_radio"] = val


def _on_language_change() -> None:
    st.session_state["app_language"] = st.session_state.get("selected_language_radio", "en")


def _render_sidebar(settings) -> None:
    """Render a premium healthcare navigation sidebar with status cards."""
    with st.sidebar:
        st.markdown(
            """
            <div class="dm-sidebar-brand">
              <div class="dm-brand-mark" style="width:2.4rem; height:2.4rem; font-size:0.95rem;">DM</div>
              <div>
                <strong style="color:var(--dm-navy); font-size:1.15rem;">Dawa-Muhafiz</strong>
                <div style="font-size:0.78rem; color:var(--dm-emerald); font-weight:700;">دوا محافظ</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### 🧭 Navigation")
        nav_options = ["Check Medicine", "Overview", "Alert Intelligence", "About Dawa-Muhafiz"]
        current_nav = st.session_state.get("active_nav", "Check Medicine")
        current_nav_idx = nav_options.index(current_nav) if current_nav in nav_options else 0
        st.radio(
            "Navigation Menu",
            nav_options,
            index=current_nav_idx,
            label_visibility="collapsed",
            key="sidebar_nav_selection",
            on_change=_on_sidebar_nav_change,
        )

        st.markdown("---")
        st.markdown("### 🌐 Language / زبان")
        lang_keys = list(LANGUAGES.keys())
        current_lang = st.session_state.get("app_language", "en")
        current_lang_idx = lang_keys.index(current_lang) if current_lang in lang_keys else 0
        st.radio(
            "Language Selector",
            lang_keys,
            index=current_lang_idx,
            format_func=lambda code: LANGUAGES.get(code, code),
            label_visibility="collapsed",
            key="selected_language_radio",
            on_change=_on_language_change,
        )

        st.markdown("---")
        st.markdown("### ⚙️ System Status")
        if settings.api_key:
            st.success(f"Gemini AI Active\n`{settings.model}`", icon="✅")
        else:
            st.info("Demo Mode Active\n(API Key Unconfigured)", icon="ℹ️")

        st.markdown(
            """
            <div class="dm-sidebar-card">
              <strong style="color:var(--dm-navy); display:block; margin-bottom:0.25rem;">🛡️ Medical Boundary</strong>
              <span style="color:var(--dm-text-muted);">Dawa-Muhafiz checks for matching alerts in official records. It never certifies whether a medicine is genuine, authentic, or safe.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="dm-sidebar-card">
              <strong style="color:var(--dm-navy); display:block; margin-bottom:0.25rem;">🔒 In-Memory Privacy</strong>
              <span style="color:var(--dm-text-muted);">Photos are decoded in memory and discarded when the session ends. No personal data is persisted.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption("v1.0-prototype · QuantumForge Sindh Healthcare")


def main() -> None:
    st.set_page_config(
        page_title="Dawa-Muhafiz | دوا محافظ — Medicine Safety Screening",
        page_icon="💊",
        layout="centered",
        initial_sidebar_state="expanded",
    )
    _initialize_state()
    settings = get_extraction_settings()

    # Sidebar controls
    _render_sidebar(settings)

    lang = st.session_state.get("app_language", "en")
    active_nav = st.session_state.get("active_nav", "Check Medicine")
    is_rtl_mode = is_rtl(lang)
    apply_styles(is_rtl_mode=is_rtl_mode)

    # Top Navbar
    render_top_navbar(
        active_nav=active_nav,
        lang=lang,
        gemini_ready=bool(settings.api_key),
        model=settings.model,
    )

    # Sub-Navigation Bar in Main Area (Pills selector)
    nav_tabs = {
        "Check Medicine": f"🔍 {t('nav_check_medicine', lang)}",
        "Overview": f"🏠 {t('nav_overview', lang)}",
        "Alert Intelligence": f"📋 {t('nav_alert_info', lang)}",
        "About Dawa-Muhafiz": f"ℹ️ {t('nav_about', lang)}",
    }
    nav_keys = list(nav_tabs.keys())
    top_nav_idx = nav_keys.index(active_nav) if active_nav in nav_keys else 0

    col_nav, col_quick_lang = st.columns([4, 1], vertical_alignment="center")
    with col_nav:
        st.radio(
            "Main View Switcher",
            nav_keys,
            index=top_nav_idx,
            format_func=lambda k: nav_tabs[k],
            horizontal=True,
            label_visibility="collapsed",
            key="top_nav_radio",
            on_change=_on_top_nav_change,
        )

    with col_quick_lang:
        st.caption(f"🌐 **{LANGUAGES.get(lang, lang)}**")

    # -------------------------------------------------------------------------
    # Route: Overview Dashboard
    # -------------------------------------------------------------------------
    if active_nav == "Overview":
        render_overview_dashboard(lang)
        col_cta1, _ = st.columns([2, 2])
        with col_cta1:
            if st.button(f"🔍 {t('hero_cta_check', lang)}", type="primary", use_container_width=True):
                st.session_state["active_nav"] = "Check Medicine"
                st.session_state["top_nav_radio"] = "Check Medicine"
                st.session_state["sidebar_nav_selection"] = "Check Medicine"
                st.rerun()

    # -------------------------------------------------------------------------
    # Route: Alert Intelligence
    # -------------------------------------------------------------------------
    elif active_nav == "Alert Intelligence":
        render_alert_intelligence(lang)

    # -------------------------------------------------------------------------
    # Route: About Dawa-Muhafiz
    # -------------------------------------------------------------------------
    elif active_nav == "About Dawa-Muhafiz":
        render_about_page(lang)

    # -------------------------------------------------------------------------
    # Route: Check Medicine (Primary Guided Workspace)
    # -------------------------------------------------------------------------
    else:
        # Header / Status info
        if bool(settings.api_key):
            st.success(f"AI extraction configured · {settings.model}", icon="✅")
        else:
            st.info("Gemini is not configured. You can add an API key for real image extraction or use the clearly marked synthetic demo.", icon="ℹ️")

        # 3-Step Process Guide
        st.markdown("### How it works")
        step_columns = st.columns(3)
        steps = (
            ("1", t("step_1_title", lang), t("step_1_desc", lang)),
            ("2", t("step_2_title", lang), t("step_2_desc", lang)),
            ("3", t("step_3_title", lang), t("step_3_desc", lang)),
        )
        for column, (number, title, description) in zip(step_columns, steps):
            with column.container(border=True):
                st.markdown(f'<span class="dm-step-number">{number}</span><strong>{title}</strong>', unsafe_allow_html=True)
                st.caption(description)

        # Safety Notice Banner
        st.warning(
            "This prototype extracts package text for review. It does not authenticate medicines or certify that a product is genuine or safe. "
            "It does not check live DRAP alerts. No alert match does not prove safety.",
            icon="⚠️",
        )

        # Step 1: Upload packaging
        st.markdown("## 1. Upload medicine packaging")
        st.caption(f"JPG or PNG · Maximum {settings.max_upload_bytes // (1024 * 1024)} MB · Include product name, manufacturer, batch and expiry details where present.")

        upload_col, reset_col = st.columns([3, 1], vertical_alignment="bottom")
        with upload_col:
            uploaded = st.file_uploader(
                "Choose medicine package image",
                type=["jpg", "jpeg", "png"],
                key=f"medicine_upload_{st.session_state['upload_version']}",
                help=f"Maximum size: {settings.max_upload_bytes // (1024 * 1024)} MB. Image bytes are kept in this session only.",
            )
        with reset_col:
            # Must remain at.button[0] for automated tests!
            st.button("Start again", on_click=_reset, use_container_width=True, help="Clear the current image and extraction results.")

        # Photography guidelines box
        render_photo_tips(lang)

        image_bytes = uploaded.getvalue() if uploaded is not None else None
        _sync_upload(image_bytes)
        image_valid = False
        if image_bytes is not None:
            image_valid, image_error, dims = validate_image(image_bytes, settings.max_upload_bytes)
            if image_valid:
                width, height = dims or (0, 0)
                st.success(f"Image validated: {uploaded.name} · {len(image_bytes) / 1024:.0f} KB", icon="✅")
                st.image(image_bytes, caption=f"Image preview ({width}x{height} px) · Sent to Gemini only when you request AI extraction.", use_container_width=True)
            else:
                st.error(image_error, icon="⛔")
                _clear_workflow_data()
        else:
            st.caption("Upload a package photo to enable extraction.")

        # Step 2: Extraction and review
        st.markdown("## 2. Extract and review details")
        if not settings.api_key:
            st.info("To enable AI extraction: add `GEMINI_API_KEY` to `.env`, then restart Streamlit. No key is stored in this app.", icon="🔐")

        live_col, demo_col = st.columns(2)
        with live_col:
            if st.button("Extract with Gemini", key="extract_gemini", type="primary", disabled=not image_valid or not settings.api_key, use_container_width=True):
                _clear_workflow_data()
                try:
                    with st.spinner("Reading visible packaging text with Gemini. Please wait..."):
                        details = extract_medicine_details(image_bytes)
                    _apply_extraction(details, "gemini")
                    st.rerun()
                except ExtractionError as exc:
                    st.session_state["extraction_error"] = {"code": exc.code, "message": exc.user_message}
                except Exception:
                    st.session_state["extraction_error"] = {
                        "code": "extraction_failed",
                        "message": "Extraction could not be completed. Retry or enter the details manually.",
                    }
        with demo_col:
            if st.button("Use synthetic demo details", key="extract_demo", disabled=not image_valid, use_container_width=True):
                _clear_workflow_data()
                _apply_extraction(extract_demo_details(), "demo_fixture")
                st.rerun()

        error = st.session_state.get("extraction_error")
        if error:
            st.error(f"{error['message']} · {error['code']}", icon="⛔")
        if st.session_state["extracted"]:
            if st.session_state["extraction_method"] == "gemini":
                st.success("Extraction completed. Review every field; the image-based result may be incomplete or inaccurate.", icon="✅")
                st.warning("Your image was transmitted to Google Gemini for this requested extraction. Do not upload packaging with personal information.", icon="⚠️")
            else:
                st.info("SYNTHETIC DEMO DETAILS · These values were not read from your image.", icon="ℹ️")

        # Editable detail field groups
        snapshot = st.session_state.get("extraction_snapshot") or {}
        for group_title, labels in FIELD_GROUPS:
            with st.container(border=True):
                st.markdown(f"### {group_title}")
                for index in range(0, len(labels), 2):
                    columns = st.columns(2)
                    for offset, column in enumerate(columns):
                        if index + offset >= len(labels):
                            continue
                        label = labels[index + offset]
                        field = DETAIL_FIELDS[label]
                        curr_val = st.session_state.get(f"detail_{field}", "")

                        # Visual tag indicating AI-extracted vs user-edited
                        orig_val = snapshot.get(field, "")
                        if orig_val and str(curr_val) == str(orig_val):
                            column.caption("🤖 AI Extracted")
                        elif curr_val and str(curr_val) != str(orig_val):
                            column.caption("✏️ User Corrected")

                        column.text_input(label, key=f"detail_{field}", placeholder="Not provided / unknown")

        try:
            current_details = _details_from_inputs()
        except (ValidationError, ValueError) as exc:
            current_details = None
            st.error(f"Review the date or field format: {exc}", icon="⛔")

        if current_details is not None and st.session_state["extracted"]:
            unreadable = current_details.unreadable_fields
            if unreadable:
                st.warning("Needs review: " + ", ".join(unreadable), icon="🔎")
            if current_details.extraction_notes:
                with st.expander("Extraction notes"):
                    for note in current_details.extraction_notes:
                        st.write(note)
            if snapshot and current_details.model_dump(mode="json") != snapshot:
                st.info("Edited values are your corrections. Confirm them against the physical package.", icon="✏️")
            if not current_details.batch_number:
                st.warning("Batch or lot number is missing. Future alert screening may require manual verification.", icon="⚠️")

        # Step 3: Screening & Results
        st.markdown("## 3. Official DRAP Alert Verification")
        st.caption("Screen reviewed packaging details against official DRAP Rapid Alerts & Recalls.")

        try:
            drap_meta = get_dataset_metadata()
            v_count = drap_meta.get("validated_count", 0)
        except Exception:
            v_count = 0

        with st.container(border=True):
            st.markdown("### 🛡️ Deterministic Alert Screening")
            st.caption(f"Validated official DRAP records indexed: **{v_count}** · Source: Drug Regulatory Authority of Pakistan (dra.gov.pk)")
            if st.button("🔍 Check Against Official DRAP Alerts", key="execute_real_verification", type="primary", disabled=current_details is None, use_container_width=True):
                with st.spinner("Screening details against official DRAP alerts..."):
                    real_result = check_drap_alerts(current_details)
                st.session_state["screening_result"] = real_result.model_dump(mode="json")
                st.session_state["screened_details"] = current_details.model_dump(mode="json")
                st.session_state["screening_is_demo"] = False
                st.rerun()

        with st.expander("Preview synthetic screening interface (development only)"):
            st.caption("This selector displays synthetic interface fixtures only. It does not run a product or batch match.")
            selected_scenario = st.selectbox(
                "Synthetic result scenario",
                [status.value for status in VerificationStatus],
                key="screening_scenario",
            )
            if st.button("Preview demo result", key="preview_screening", disabled=current_details is None):
                result = screen_demo(current_details, selected_scenario)
                st.session_state["screening_result"] = result.model_dump(mode="json")
                st.session_state["screened_details"] = current_details.model_dump(mode="json")
                st.session_state["screening_is_demo"] = True

        result_data = st.session_state.get("screening_result")
        if result_data:
            if current_details is None or current_details.model_dump(mode="json") != st.session_state.get("screened_details"):
                st.warning("Details changed after this result. Preview the demo result again to refresh it.")
                st.session_state["screening_result"] = None
                st.session_state["screened_details"] = None
            else:
                try:
                    validated_result = VerificationResult.model_validate(result_data)
                    is_demo = st.session_state.get("screening_is_demo", False)
                    render_result(validated_result, lang=lang, is_demo=is_demo)
                    render_screening_report(current_details, validated_result, lang=lang, is_demo=is_demo)
                except ValidationError:
                    st.error("The screening result did not pass validation. Please verify again.")
                    st.session_state["screening_result"] = None
                    st.session_state["screened_details"] = None

        render_safety_guidance(lang=lang)
        render_help(lang=lang)

    # Branded Clinical Footer
    st.markdown(
        f"""
        <div class="dm-footer">
          <p><strong>Dawa-Muhafiz (دوا محافظ)</strong> — Medicine Alert Intelligence & Safety Screening.</p>
          <p>{t('footer_about_text', lang)}</p>
          <p style="font-size:0.8rem; color:var(--dm-text-muted);">{t('footer_privacy_text', lang)} · {t('footer_standards', lang)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
