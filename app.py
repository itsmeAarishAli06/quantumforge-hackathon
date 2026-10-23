"""Dawa-Muhafiz Streamlit workflow for medicine-label extraction and review."""

from datetime import date
import hashlib

import streamlit as st
from pydantic import ValidationError

from ai.config import get_extraction_settings
from ai.errors import ExtractionError, ImageValidationError
from ai.image_processing import validate_image_bytes
from ai.medicine_extractor import extract_medicine_details
from common.schemas import MedicineDetails, VerificationResult, VerificationStatus
from ui.components import render_help, render_result, render_safety_guidance
from ui.demo_service import DemoServiceError, extract_demo_details, screen_demo
from ui.styles import apply_styles


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
        "screening_scenario": VerificationStatus.VERIFICATION_REQUIRED.value,
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


def _render_header(gemini_ready: bool, model: str) -> None:
    st.markdown(
        '<div class="dm-brand-row"><div class="dm-brand-mark" aria-hidden="true">DM</div>'
        '<div><p class="dm-brand-name">Dawa-Muhafiz</p>'
        '<p class="dm-brand-sub">Medicine packaging information and screening prototype</p></div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="dm-hero"><h1 class="dm-hero-title">Smarter medicine information. More informed decisions.</h1>'
        '<p class="dm-hero-copy">Read visible package details, review them yourself, and prepare for a separate alert-screening step.</p>'
        '<span class="dm-demo-pill">PROTOTYPE · NOT AN OFFICIAL DRAP SERVICE</span></div>',
        unsafe_allow_html=True,
    )
    if gemini_ready:
        st.success(f"AI extraction configured · {model}", icon="✅")
    else:
        st.info("Gemini is not configured. You can add an API key for real image extraction or use the clearly marked synthetic demo.", icon="ℹ️")


def main() -> None:
    st.set_page_config(page_title="Dawa-Muhafiz | Medicine Information", page_icon="DM", layout="centered")
    _initialize_state()
    apply_styles()
    settings = get_extraction_settings()
    _render_header(bool(settings.api_key), settings.model)

    st.markdown("### How it works")
    step_columns = st.columns(3)
    steps = (
        ("1", "Upload packaging", "Choose a clear JPG or PNG photo."),
        ("2", "Review details", "Confirm visible text and correct mistakes."),
        ("3", "Screen alerts later", "Real alert checking is a separate future phase."),
    )
    for column, (number, title, description) in zip(step_columns, steps):
        with column.container(border=True):
            st.markdown(f'<span class="dm-step-number">{number}</span><strong>{title}</strong>', unsafe_allow_html=True)
            st.caption(description)

    st.warning(
        "This prototype extracts package text for review. It does not authenticate medicines or certify that a product is genuine or safe. "
        "It does not check live DRAP alerts. No alert match does not prove safety.",
        icon="⚠️",
    )

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
        st.button("Start again", on_click=_reset, use_container_width=True, help="Clear the current image and extraction results.")

    image_bytes = uploaded.getvalue() if uploaded is not None else None
    _sync_upload(image_bytes)
    image_valid = False
    if image_bytes is not None:
        image_valid, image_error, _ = validate_image(image_bytes, settings.max_upload_bytes)
        if image_valid:
            st.success(f"Image validated: {uploaded.name} · {len(image_bytes) / 1024:.0f} KB", icon="✅")
            st.image(image_bytes, caption="Image preview · The photo is sent to Gemini only when you request AI extraction.", use_container_width=True)
        else:
            st.error(image_error, icon="⛔")
            _clear_workflow_data()
    else:
        st.caption("Upload a package photo to enable extraction.")

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
        snapshot = st.session_state.get("extraction_snapshot")
        if snapshot and current_details.model_dump(mode="json") != snapshot:
            st.info("Edited values are your corrections. Confirm them against the physical package.", icon="✏️")
        if not current_details.batch_number:
            st.warning("Batch or lot number is missing. Future alert screening may require manual verification.", icon="⚠️")

    st.markdown("## 3. Alert verification is separate")
    st.info("This phase does not search DRAP alerts or decide whether a medicine is recalled, genuine, counterfeit, or safe.", icon="ℹ️")
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

    result_data = st.session_state.get("screening_result")
    if result_data:
        if current_details is None or current_details.model_dump(mode="json") != st.session_state.get("screened_details"):
            st.warning("Details changed after this result. Preview the demo result again to refresh it.")
            st.session_state["screening_result"] = None
            st.session_state["screened_details"] = None
        else:
            try:
                render_result(VerificationResult.model_validate(result_data))
            except ValidationError:
                st.error("The demo result did not pass validation. Please preview it again.")
                st.session_state["screening_result"] = None
                st.session_state["screened_details"] = None

    render_safety_guidance()
    render_help()
    st.caption("Hackathon prototype · Image extraction can be incomplete · No live DRAP verification is implemented")


if __name__ == "__main__":
    main()
