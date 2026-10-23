"""Streamlit demo UI for Dawa-Muhafiz (synthetic scenarios only)."""

from datetime import date
from io import BytesIO
import os

import streamlit as st
from PIL import Image, UnidentifiedImageError
from pydantic import ValidationError

from common.schemas import MedicineDetails, VerificationResult, VerificationStatus
from ui.components import render_result, render_safety_guidance
from ui.demo_service import DemoServiceError, extract_demo_details, screen_demo


MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_BYTES", str(10 * 1024 * 1024)))
MAX_IMAGE_PIXELS = 20_000_000
DETAIL_FIELDS = {
    "Medicine name": "medicine_name",
    "Generic name": "generic_name",
    "Strength": "strength",
    "Dosage form": "dosage_form",
    "Manufacturer": "manufacturer_name",
    "Manufacturer address": "manufacturer_address",
    "Batch number": "batch_number",
    "Manufacturing date (YYYY-MM-DD)": "manufacturing_date",
    "Expiry date (YYYY-MM-DD)": "expiry_date",
    "Registration number": "registration_number",
    "Barcode value": "barcode_value",
}


def validate_image(data: bytes) -> tuple[bool, str, tuple[int, int] | None]:
    """Validate image bytes in memory; never writes the upload to disk."""
    if not data:
        return False, "The uploaded file is empty.", None
    if len(data) > MAX_UPLOAD_BYTES:
        return False, f"Image is too large. Maximum allowed size is {MAX_UPLOAD_BYTES // (1024 * 1024)} MB.", None
    try:
        with Image.open(BytesIO(data)) as image:
            if image.format not in {"JPEG", "PNG"}:
                return False, "Unsupported image format. Please upload a JPG or PNG image.", None
            size = image.size
            if size[0] * size[1] > MAX_IMAGE_PIXELS:
                return False, "Image dimensions are too large to process safely.", None
            image.verify()
        return True, "", size
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError, ValueError):
        return False, "This image could not be read. Try a clear JPG or PNG file.", None


def _initialize_state() -> None:
    st.session_state.setdefault("upload_version", 0)
    st.session_state.setdefault("extracted", False)
    st.session_state.setdefault("screening_result", None)
    st.session_state.setdefault("screened_details", None)
    st.session_state.setdefault("screening_scenario", "VERIFICATION_REQUIRED")


def _reset() -> None:
    for key in list(st.session_state.keys()):
        if key.startswith("detail_"):
            del st.session_state[key]
    st.session_state["upload_version"] += 1
    st.session_state["extracted"] = False
    st.session_state["screening_result"] = None
    st.session_state["screened_details"] = None
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
    values["extraction_method"] = "demo" if st.session_state["extracted"] else None
    values["requires_manual_review"] = True
    return MedicineDetails(**values)


def main() -> None:
    st.set_page_config(page_title="Dawa-Muhafiz | Medicine Alert Screening", page_icon="💊", layout="centered")
    _initialize_state()

    st.title("Dawa-Muhafiz")
    st.subheader("Medicine Alert Screening")
    st.write("Review visible medicine-package details against an available alert dataset.")
    st.warning(
        "This tool screens medicine details against an available alert dataset. "
        "It does not authenticate medicines or certify their safety."
    )

    st.markdown("### How it works")
    step_a, step_b, step_c = st.columns(3)
    step_a.markdown("**1 · Upload**\n\nChoose a package photo.")
    step_b.markdown("**2 · Review**\n\nCheck the displayed details.")
    step_c.markdown("**3 · Screen**\n\nPreview a demo result.")
    st.info("DEMO MODE: extraction values and alert scenarios are synthetic. No AI provider or DRAP database is contacted.")

    st.markdown("### 1. Medicine package image")
    left, right = st.columns([3, 1])
    with left:
        uploaded = st.file_uploader(
            "Upload JPG or PNG image",
            type=["jpg", "jpeg", "png"],
            key=f"medicine_upload_{st.session_state['upload_version']}",
            help=f"Maximum size: {MAX_UPLOAD_BYTES // (1024 * 1024)} MB. The image stays in memory for this session.",
        )
    with right:
        st.button("Clear workflow", on_click=_reset, use_container_width=True)

    image_bytes: bytes | None = None
    image_valid = False
    if uploaded is not None:
        image_bytes = uploaded.getvalue()
        image_valid, image_error, _dimensions = validate_image(image_bytes)
        if image_valid:
            st.image(image_bytes, caption="Uploaded image preview", use_container_width=True)
        else:
            st.error(image_error)
            st.session_state["extracted"] = False
            st.session_state["screening_result"] = None
            st.session_state["screened_details"] = None

    st.markdown("### 2. Medicine details")
    st.caption("These editable fields are user-reviewed inputs. Empty fields mean unknown.")
    if st.button("Extract Medicine Details (DEMO)", disabled=not image_valid, type="primary"):
        try:
            demo_details = extract_demo_details()
            for field in DETAIL_FIELDS.values():
                value = getattr(demo_details, field)
                st.session_state[f"detail_{field}"] = value.isoformat() if value else ""
            st.session_state["extracted"] = True
            st.session_state["screening_result"] = None
            st.session_state["screened_details"] = None
            st.rerun()
        except DemoServiceError as exc:
            st.error(f"Demo extraction could not run: {exc}")

    if st.session_state["extracted"]:
        st.info("Synthetic demo details shown. They were not read from the uploaded image.")

    with st.container(border=True):
        for index in range(0, len(DETAIL_FIELDS), 2):
            labels = list(DETAIL_FIELDS.keys())
            fields = list(DETAIL_FIELDS.values())
            columns = st.columns(2)
            for offset, column in enumerate(columns):
                i = index + offset
                if i >= len(labels):
                    continue
                label, field = labels[i], fields[i]
                column.text_input(label, key=f"detail_{field}", placeholder="Unknown / not provided")

    try:
        current_details = _details_from_inputs()
    except (ValidationError, ValueError) as exc:
        current_details = None
        st.error(f"Please correct the medicine details: {exc}")

    if current_details is not None:
        if not current_details.batch_number:
            st.warning("Batch number is missing. A real screening may require manual verification.")
        if not current_details.medicine_name:
            st.caption("Medicine name is unknown. Add it from the package before previewing a screening scenario.")

    st.markdown("### 3. Check available alerts")
    scenario_options = [status.value for status in VerificationStatus]
    selected_scenario = st.selectbox(
        "Demo screening scenario",
        scenario_options,
        key="screening_scenario",
        help="This selector previews synthetic interface states. It does not run a real alert lookup.",
    )
    if st.button("Check Available Alerts (DEMO)", disabled=current_details is None):
        try:
            result = screen_demo(current_details, selected_scenario)
            st.session_state["screening_result"] = result.model_dump(mode="json")
            st.session_state["screened_details"] = current_details.model_dump(mode="json")
        except (DemoServiceError, ValidationError) as exc:
            st.error(f"Demo screening could not be completed: {exc}")
            st.session_state["screening_result"] = None
            st.session_state["screened_details"] = None

    result_data = st.session_state.get("screening_result")
    screened = st.session_state.get("screened_details")
    if result_data:
        if current_details is None or current_details.model_dump(mode="json") != screened:
            st.warning("Medicine details changed after screening. Run the demo screen again to refresh the result.")
            st.session_state["screening_result"] = None
            st.session_state["screened_details"] = None
        else:
            try:
                render_result(VerificationResult.model_validate(result_data))
            except ValidationError:
                st.error("The result could not be validated. Please run the demo screen again.")
                st.session_state["screening_result"] = None
                st.session_state["screened_details"] = None

    render_safety_guidance()


if __name__ == "__main__":
    main()
