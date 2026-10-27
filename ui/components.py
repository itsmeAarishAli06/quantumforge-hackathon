"""Reusable presentation components for safety alerts, evidence, guidance, reports, and views.

Maintains strict medical boundaries:
- ALERT_MATCH: Deep red warning with official DRAP citation, excerpt, and non-consumption warning.
- VERIFICATION_REQUIRED: Calm amber alert identifying exact missing/unreadable fields.
- NO_MATCH_FOUND: Neutral slate notice explicitly stating no match found, with prominent non-authenticity disclaimer.
- ERROR: Distinct failure state, never converted to no-match.
"""

from datetime import datetime
from html import escape
import streamlit as st

from common.schemas import VerificationResult, VerificationStatus, MedicineDetails
from ui.i18n import t, is_rtl
from verification.database import fetch_validated_alerts
from verification.data_loader import get_dataset_metadata


def render_top_navbar(active_nav: str, lang: str = "en", gemini_ready: bool = False, model: str = "") -> None:
    """Render the branded application header and current system status."""
    rtl_class = "dm-localized-container" if is_rtl(lang) else ""
    status_class = "dm-status-ready" if gemini_ready else "dm-status-demo"
    status_label = "Gemini extraction ready" if gemini_ready else "Demo mode"
    status_detail = f" · {escape(model)}" if gemini_ready and model else ""
    st.markdown(
        f"""
        <div class="dm-topbar {rtl_class}">
          <div class="dm-brand-left">
            <div class="dm-brand-mark" aria-hidden="true"><span>DM</span></div>
            <div class="dm-brand-copy">
              <span class="dm-brand-eyebrow">MEDICINE SAFETY · PAKISTAN</span>
              <p class="dm-brand-title">Dawa-Muhafiz <span class="dm-brand-urdu">دوا محافظ</span></p>
              <p class="dm-brand-subtitle">{escape(t('app_descriptor', lang))}</p>
            </div>
          </div>
          <div class="dm-topbar-meta">
            <span class="dm-prototype-badge">ACADEMIC PROTOTYPE</span>
            <span class="dm-topbar-status {status_class}">
              <span class="dm-status-dot" aria-hidden="true"></span>
              {status_label}{status_detail}
            </span>
            <span class="dm-current-view">{escape(active_nav)}</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_overview_dashboard(lang: str = "en") -> None:
    """Render the premium Home / Overview dashboard."""
    rtl_class = "dm-localized-container" if is_rtl(lang) else ""
    st.markdown(
        f"""
        <div class="dm-hero {rtl_class}">
          <h1 class="dm-hero-title">{t('hero_headline', lang)}</h1>
          <p class="dm-hero-copy">{t('hero_sub', lang)}</p>
          <span class="dm-demo-pill dm-pill-demo">{t('badge_prototype', lang)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(f"### {t('hero_cta_how', lang)}")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""
            <div class="dm-wf-card {rtl_class}">
              <div class="dm-wf-num">01</div>
              <h4 class="dm-wf-title">{t('wf_card1_title', lang)}</h4>
              <p class="dm-wf-desc">{t('wf_card1_desc', lang)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="dm-wf-card {rtl_class}">
              <div class="dm-wf-num">02</div>
              <h4 class="dm-wf-title">{t('wf_card2_title', lang)}</h4>
              <p class="dm-wf-desc">{t('wf_card2_desc', lang)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""
            <div class="dm-wf-card {rtl_class}">
              <div class="dm-wf-num">03</div>
              <h4 class="dm-wf-title">{t('wf_card3_title', lang)}</h4>
              <p class="dm-wf-desc">{t('wf_card3_desc', lang)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown(f"### 🛡️ {t('trust_heading', lang)}")
    st.write(t("trust_desc", lang))

    with st.container(border=True):
        st.markdown(f"- **{t('trust_point1', lang)}**")
        st.markdown(f"- **{t('trust_point2', lang)}**")
        st.markdown(f"- **{t('trust_point3', lang)}**")

    with st.container(border=True):
        st.markdown(f"#### 📊 {t('coverage_title', lang)}")
        st.caption(t("coverage_desc", lang))


def render_alert_intelligence(lang: str = "en") -> None:
    """Render the Alert Intelligence and regulatory guidance page."""
    rtl_class = "dm-localized-container" if is_rtl(lang) else ""
    st.markdown(
        f"""
        <div class="dm-card {rtl_class}">
          <h2>📋 {t('alert_intel_title', lang)}</h2>
          <p class="dm-muted">{t('alert_intel_sub', lang)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown(f"### 🔍 {t('alert_intel_what_is', lang)}")
        st.write(t("alert_intel_what_is_desc", lang))

    with st.container(border=True):
        st.markdown(f"### 🏷️ {t('alert_intel_batch_guide', lang)}")
        st.write(t("alert_intel_batch_desc", lang))
        st.info("💡 Tip: Batch numbers often start with 'B-', 'Lot', 'B.No', or alphanumeric codes stamped on the box flap.")

    with st.container(border=True):
        st.markdown("### 🌐 Official Regulatory Authority")
        st.write("Drug Regulatory Authority of Pakistan (DRAP), Ministry of National Health Services Regulations and Coordination.")
        st.markdown(
            '<a href="https://www.dra.gov.pk/safety-information/product-recalls/rapid-alert-system/" target="_blank" rel="noopener noreferrer" style="color:#087F70; font-weight:700; text-decoration:underline;">🔗 Open Official DRAP Recall & Rapid Alert Portal &rarr;</a>',
            unsafe_allow_html=True,
        )

    try:
        alerts = fetch_validated_alerts()
        meta = get_dataset_metadata()
    except Exception:
        alerts = []
        meta = {"validated_count": 0}

    with st.container(border=True):
        st.markdown("### 📊 Validated DRAP Alerts Registry")
        st.caption(f"Currently indexing {meta.get('validated_count', len(alerts))} official DRAP alerts with full regulatory provenance.")

        if alerts:
            search_query = st.text_input("Filter DRAP alert registry by product or batch", placeholder="e.g., Brexin, Gabica, 4721026AA...", key="drap_registry_search").strip().casefold()
            filtered_alerts = [
                a for a in alerts
                if not search_query or search_query in a.product_name.casefold() or (a.batch_number and search_query in a.batch_number.casefold())
            ]
            st.caption(f"Showing {len(filtered_alerts)} of {len(alerts)} official records:")
            for a in filtered_alerts:
                with st.expander(f"{a.product_name} · Batch: {a.batch_number or 'All Batches'} [{a.alert_type.value.replace('_', ' ').title()}]"):
                    st.markdown(f"**Alert ID:** `{a.alert_id}`")
                    st.markdown(f"**Publication Date:** {a.publication_date or 'Official DRAP Record'}")
                    st.markdown(f"**Official Source:** {a.source_title}")
                    st.markdown(f"**Regulatory Excerpt:** *\"{a.supporting_excerpt}\"*")
                    st.markdown(f'<a href="{a.source_url}" target="_blank" rel="noopener noreferrer" style="color:#087F70; font-weight:700; text-decoration:underline;">🔗 Official DRAP Document Source &rarr;</a>', unsafe_allow_html=True)


def render_about_page(lang: str = "en") -> None:
    """Render the About Dawa-Muhafiz project page."""
    rtl_class = "dm-localized-container" if is_rtl(lang) else ""
    st.markdown(
        f"""
        <div class="dm-card {rtl_class}">
          <h2>ℹ️ {t('about_proj_title', lang)}</h2>
          <p class="dm-muted">{t('about_proj_sub', lang)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown(f"### 🎯 {t('about_proj_mission', lang)}")
        st.write(t("about_proj_mission_desc", lang))

    with st.container(border=True):
        st.markdown(f"### ⚖️ {t('about_proj_ethics', lang)}")
        st.markdown(t("about_proj_ethics_desc", lang))

    with st.container(border=True):
        st.markdown("### 🏗️ Technical Architecture")
        st.write("Built as a Python 3.11+ Modular Monolith adhering to Pydantic v2 domain schemas, deterministic SQLite indexing, in-memory image validation, and Google Gemini Vision extraction.")
        st.caption("QuantumForge Hackathon · Sindh Healthcare Initiative")


def render_photo_tips(lang: str = "en") -> None:
    """Render practical photography guidelines for package capture."""
    rtl_class = "dm-localized-container" if is_rtl(lang) else ""
    st.markdown(
        f"""
        <div class="dm-tips-box {rtl_class}">
          <strong>💡 {t('upload_tips_title', lang)}:</strong>
          <ul style="margin: 0.35rem 0 0.15rem; padding-left: 1.25rem;">
            <li>{t('upload_tip_light', lang)}</li>
            <li>{t('upload_tip_batch', lang)}</li>
            <li>{t('upload_tip_angle', lang)}</li>
          </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_result(result: VerificationResult, lang: str = "en", is_demo: bool = True) -> None:
    """Render a verification result with strict medical boundaries and evidence inspection."""
    st.markdown(f"## {t('result_header', lang)}")

    rtl_class = "dm-localized-container" if is_rtl(lang) else ""

    if is_demo:
        st.caption("SYNTHETIC DEMO SCENARIO | No real alert lookup was performed")
        with st.container(border=True):
            if result.status == VerificationStatus.ALERT_MATCH:
                st.error("ALERT MATCH | Synthetic demo scenario")
                st.markdown(
                    f"""
                    <div class="dm-result-card dm-res-match {rtl_class}">
                      <div class="dm-res-title dm-match-title">
                        🚨 {t('status_alert_match_title', lang)}
                      </div>
                      <p>{t('status_alert_match_desc', lang)}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.write("A sample alert-match panel is shown to demonstrate the interface.")

                for index, item in enumerate(result.matching_alerts, start=1):
                    with st.container(border=True):
                        st.markdown(
                            f"""
                            <div class="dm-evidence-badge">OFFICIAL DRAP EVIDENCE #{index}</div>
                            """,
                            unsafe_allow_html=True,
                        )
                        st.markdown(f"**Demo classification:** {item.alert.alert_type.value.replace('_', ' ').title()}")
                        st.markdown(f"**Synthetic product:** {item.alert.product_name}")
                        st.markdown(f"**Synthetic evidence:** {item.alert.supporting_excerpt}")
                        st.markdown(f"**Fixture label:** {item.alert.source_title}")
                        st.markdown(f"**Fixture address:** `{item.alert.source_url}`")
                        st.markdown("**Scenario explanation:** " + "; ".join(item.match_reasons))

                        # Working link to source
                        st.markdown(
                            f'<a href="{item.alert.source_url}" target="_blank" rel="noopener noreferrer" style="display:inline-block; margin-top:0.4rem; color:#087F70; font-weight:700; text-decoration:underline;">🔗 {t("evidence_link", lang)} &rarr;</a>',
                            unsafe_allow_html=True,
                        )

                st.warning("This sample is not a DRAP alert, source, or finding. Do not use it to make a medicine decision.")
                st.error(f"⚠️ {t('status_alert_match_warning', lang)}")

            elif result.status == VerificationStatus.VERIFICATION_REQUIRED:
                st.warning("VERIFICATION REQUIRED")
                st.markdown(
                    f"""
                    <div class="dm-result-card dm-res-req {rtl_class}">
                      <div class="dm-res-title dm-req-title">
                        ⚠️ {t('status_verification_req_title', lang)}
                      </div>
                      <p>{t('status_verification_req_desc', lang)}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.write("The available details are insufficient or ambiguous for this demo scenario.")
                if result.missing_or_uncertain_information:
                    st.markdown("**Review these details:** " + ", ".join(result.missing_or_uncertain_information))
                st.write("Check the physical package or consult a qualified pharmacist.")
                st.info(f"🔎 {t('status_verification_req_action', lang)}")

            elif result.status == VerificationStatus.NO_MATCH_FOUND:
                st.info("NO MATCH FOUND in the synthetic demo dataset.")
                st.markdown(
                    f"""
                    <div class="dm-result-card dm-res-nomatch {rtl_class}">
                      <div class="dm-res-title dm-nomatch-title">
                        ℹ️ {t('status_no_match_title', lang)}
                      </div>
                      <p>{t('status_no_match_desc', lang)}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown("**This does not establish that a medicine is genuine, approved, or safe.**")
                st.write("The current demo contains no real DRAP alert records.")
                st.warning(f"🛡️ {t('status_no_match_caveat', lang)}")

            elif result.status == VerificationStatus.ERROR:
                st.error("ERROR | The demo screening could not be completed. Please retry.")
                st.markdown(
                    f"""
                    <div class="dm-result-card dm-res-error {rtl_class}">
                      <div class="dm-res-title dm-error-title">
                        ⛔ {t('status_error_title', lang)}
                      </div>
                      <p>{t('status_error_desc', lang)}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if result.error_code:
                    st.caption(f"Demo error code: {result.error_code}")

            st.markdown(f"**Suggested next step:** {result.recommended_next_step}")
            st.caption(f"Demo-only record count: {result.dataset_record_count}")

    else:
        st.caption(f"OFFICIAL DRAP VERIFICATION ENGINE | Screened against {result.dataset_record_count} validated DRAP alert records")
        with st.container(border=True):
            if result.status == VerificationStatus.ALERT_MATCH:
                st.error(f"🚨 ALERT MATCH | Official DRAP Alert Record Detected ({len(result.matching_alerts)} match)")
                st.markdown(
                    f"""
                    <div class="dm-result-card dm-res-match {rtl_class}">
                      <div class="dm-res-title dm-match-title">
                        🚨 {t('status_alert_match_title', lang)}
                      </div>
                      <p><strong>A matching entry was found in the validated official DRAP alert database.</strong> Review the official regulatory findings below immediately.</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                for index, item in enumerate(result.matching_alerts, start=1):
                    with st.container(border=True):
                        st.markdown(
                            f"""
                            <div class="dm-evidence-badge">OFFICIAL DRAP EVIDENCE #{index} · {item.alert.alert_id}</div>
                            """,
                            unsafe_allow_html=True,
                        )
                        st.markdown(f"**Regulatory Alert Type:** {item.alert.alert_type.value.replace('_', ' ').title()}")
                        st.markdown(f"**Affected Product Name:** {item.alert.product_name}")
                        st.markdown(f"**Affected Batch Number:** `{item.alert.batch_number or 'All Batches / Product-Wide'}`")
                        if item.alert.manufacturer_name:
                            st.markdown(f"**Labelled Manufacturer:** {item.alert.manufacturer_name}")
                        if item.alert.publication_date:
                            st.markdown(f"**Publication Date:** {item.alert.publication_date}")
                        st.markdown(f"**Official Source Title:** {item.alert.source_title}")
                        st.markdown(f"**Regulatory Finding Excerpt:** *\"{item.alert.supporting_excerpt}\"*")
                        st.markdown("**Deterministic Match Reasons:** " + "; ".join(item.match_reasons))

                        # Direct link to official DRAP portal
                        st.markdown(
                            f'<a href="{item.alert.source_url}" target="_blank" rel="noopener noreferrer" style="display:inline-block; margin-top:0.4rem; color:#087F70; font-weight:700; text-decoration:underline;">🔗 Open Official DRAP Regulatory Notice ({item.alert.alert_id}) &rarr;</a>',
                            unsafe_allow_html=True,
                        )

                st.error(
                    "⚠️ **CRITICAL PRECAUTION:** Do not consume, sell, or dispense this medicine batch. "
                    "Quarantine the product and report this batch to the Drug Regulatory Authority of Pakistan (DRAP) or your provincial drug inspector."
                )

            elif result.status == VerificationStatus.VERIFICATION_REQUIRED:
                st.warning("⚠️ VERIFICATION REQUIRED | Inconclusive Match")
                st.markdown(
                    f"""
                    <div class="dm-result-card dm-res-req {rtl_class}">
                      <div class="dm-res-title dm-req-title">
                        ⚠️ {t('status_verification_req_title', lang)}
                      </div>
                      <p>The submitted medicine details partially match an official DRAP alert, but critical information (such as batch number or formulation) is missing or conflicts.</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if result.missing_or_uncertain_information:
                    st.markdown("**Notes for manual review:**")
                    for info in result.missing_or_uncertain_information:
                        st.markdown(f"- {info}")
                st.info("🔎 **Action:** Check physical packaging for the batch or lot number. If uncertain, consult a licensed pharmacist before consuming.")

            elif result.status == VerificationStatus.NO_MATCH_FOUND:
                st.info("ℹ️ NO MATCH FOUND in the validated DRAP alert database.")
                st.markdown(
                    f"""
                    <div class="dm-result-card dm-res-nomatch {rtl_class}">
                      <div class="dm-res-title dm-nomatch-title">
                        ℹ️ {t('status_no_match_title', lang)}
                      </div>
                      <p>{t('status_no_match_desc', lang)}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"**No matching alert or recall record was identified** for this product/batch among the {result.dataset_record_count} validated official DRAP alerts currently indexed."
                )
                st.warning(
                    "🛡️ **NON-AUTHENTICITY DISCLAIMER:** Dawa-Muhafiz checks only for records in its curated DRAP alert database. "
                    "An absence of an alert match DOES NOT confirm that the medicine is genuine, authentic, registered, or safe. "
                    "Always purchase medicines from licensed pharmacies and consult a healthcare professional if you suspect quality defects."
                )

            elif result.status == VerificationStatus.ERROR:
                st.error("⛔ ERROR | Alert verification could not be completed.")
                st.markdown(
                    f"""
                    <div class="dm-result-card dm-res-error {rtl_class}">
                      <div class="dm-res-title dm-error-title">
                        ⛔ {t('status_error_title', lang)}
                      </div>
                      <p>{t('status_error_desc', lang)}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if result.error_code:
                    st.caption(f"Error reference code: `{result.error_code}`")

            st.markdown(f"**Recommended next step:** {result.recommended_next_step}")
            st.caption(f"Database records verified: {result.dataset_record_count} official DRAP alerts")


def render_screening_report(details: MedicineDetails | None, result: VerificationResult, lang: str = "en", is_demo: bool = True) -> None:
    """Provide an inspectable, downloadable clinical screening summary."""
    with st.expander(f"📄 {t('report_title', lang)} (Print / Export)", expanded=False):
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        med_name = details.medicine_name if details and details.medicine_name else "Unknown / Not provided"
        batch_no = details.batch_number if details and details.batch_number else "Not provided"
        mfr_name = details.manufacturer_name if details and details.manufacturer_name else "Not provided"
        exp_date = str(details.expiry_date) if details and details.expiry_date else "Not provided"
        dataset_label = "(Demo dataset)" if is_demo else "(Official DRAP Validated Index)"
        
        report_text = f"""================================================================================
DAWA-MUHAFIZ — MEDICINE SCREENING SUMMARY REPORT
Generated at: {now_str}
Language: {lang.upper()}
Status: {result.status.value}
================================================================================

1. SUBMITTED MEDICINE PACKAGING DETAILS:
   - Product Name:        {med_name}
   - Generic Ingredient:  {(details.generic_name if details else None) or 'N/A'}
   - Strength / Form:     {(details.strength if details else None) or 'N/A'} / {(details.dosage_form if details else None) or 'N/A'}
   - Batch / Lot Number:  {batch_no}
   - Expiry Date:         {exp_date}
   - Manufacturer:        {mfr_name}
   - Registration Number: {(details.registration_number if details else None) or 'N/A'}
   - Extraction Method:   {(details.extraction_method if details else None) or 'manual'}

2. SCREENING OUTCOME:
   - Verification Status: {result.status.value}
   - Recommended Action:  {result.recommended_next_step}
   - Checked Records:     {result.dataset_record_count} {dataset_label}

3. OFFICIAL EVIDENCE CITATION:
"""
        if result.matching_alerts:
            for idx, m in enumerate(result.matching_alerts, start=1):
                report_text += f"""
   Match #{idx}:
   - Alert ID:          {m.alert.alert_id}
   - Document Title:    {m.alert.source_title}
   - Document URL:      {m.alert.source_url}
   - Official Excerpt:  {m.alert.supporting_excerpt}
   - Match Criteria:    {'; '.join(m.match_reasons)}
"""
        else:
            report_text += "   No matching official DRAP alert was found in the checked dataset.\n"

        report_text += f"""
================================================================================
CRITICAL MEDICAL SAFETY NOTICE:
Dawa-Muhafiz checks packaging details against available official alerts.
A status of NO_MATCH_FOUND does NOT certify that a medicine is genuine,
authentic, or safe. If you have medical concerns, contact a licensed
pharmacist or physician immediately.
================================================================================
"""

        st.code(report_text, language="text")
        st.download_button(
            label=f"⬇️ {t('report_btn', lang)}",
            data=report_text,
            file_name=f"dawa_muhafiz_screening_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True,
            key="download_screening_report_btn",
        )


def render_safety_guidance(lang: str = "en") -> None:
    """Place core medical-safety limitations in a prominent, readable notice."""
    st.markdown(f"## {t('safety_disclaimer_title', lang)}")
    st.warning(
        "This prototype does not authenticate medicines or certify that a product is genuine or safe. "
        "No alert match does not prove safety. Confirm details against the package and consult a qualified "
        "pharmacist or official DRAP information when in doubt."
    )
    if lang != "en":
        st.info(f"🛡️ {t('safety_disclaimer_text', lang)}")


def render_help(lang: str = "en") -> None:
    """Offer concise photo and status guidance without cluttering the main flow."""
    with st.expander(f"ℹ️ {t('upload_tips_title', lang)} & Limitations"):
        st.markdown("### Taking a useful photo")
        st.write("Use a clear, well-lit photo. Include product name and manufacturer, and batch and expiry details where present. Avoid glare and blur.")
        st.write("Batch and expiry details can help identify package information relevant to future alert checks. Confirm all displayed values on the physical package.")
        st.markdown("### What the demo statuses mean")
        st.markdown(
            "- **ALERT_MATCH:** synthetic example panel only; no real match was checked.\n"
            "- **VERIFICATION_REQUIRED:** the example indicates more information or human review is needed.\n"
            "- **NO_MATCH_FOUND:** no result in a demo fixture; this is not evidence of safety or authenticity.\n"
            "- **ERROR:** the demo operation did not complete; it is distinct from a no-match."
        )
        st.info("Gemini can extract visible text when configured. Real DRAP alert matching is not implemented.")
        st.markdown("### Privacy and accuracy")
        st.write("Images stay in the active app session unless you request Gemini extraction. When requested, image bytes are sent to Google's Gemini service. Extraction can be incomplete or inaccurate; review every field.")
