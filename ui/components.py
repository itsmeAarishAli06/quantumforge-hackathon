"""Reusable result and safety presentation components."""

import streamlit as st

from common.schemas import VerificationResult, VerificationStatus


def render_result(result: VerificationResult) -> None:
    """Render a validated result fixture with explicit demo boundaries."""
    st.markdown("## Screening result")
    st.caption("SYNTHETIC DEMO SCENARIO | No real alert lookup was performed")
    with st.container(border=True):
        if result.status == VerificationStatus.ALERT_MATCH:
            st.error("ALERT MATCH | Synthetic demo scenario")
            st.write("A sample alert-match panel is shown to demonstrate the interface.")
            for item in result.matching_alerts:
                with st.container(border=True):
                    st.markdown(f"**Demo classification:** {item.alert.alert_type.value.replace('_', ' ').title()}")
                    st.markdown(f"**Synthetic product:** {item.alert.product_name}")
                    st.markdown(f"**Synthetic evidence:** {item.alert.supporting_excerpt}")
                    st.markdown(f"**Fixture label:** {item.alert.source_title}")
                    st.markdown(f"**Fixture address:** `{item.alert.source_url}`")
                    st.markdown("**Scenario explanation:** " + "; ".join(item.match_reasons))
            st.warning("This sample is not a DRAP alert, source, or finding. Do not use it to make a medicine decision.")
        elif result.status == VerificationStatus.VERIFICATION_REQUIRED:
            st.warning("VERIFICATION REQUIRED")
            st.write("The available details are insufficient or ambiguous for this demo scenario.")
            if result.missing_or_uncertain_information:
                st.markdown("**Review these details:** " + ", ".join(result.missing_or_uncertain_information))
            st.write("Check the physical package or consult a qualified pharmacist.")
        elif result.status == VerificationStatus.NO_MATCH_FOUND:
            st.info("NO MATCH FOUND in the synthetic demo dataset.")
            st.markdown("**This does not establish that a medicine is genuine, approved, or safe.**")
            st.write("The current demo contains no real DRAP alert records.")
        elif result.status == VerificationStatus.ERROR:
            st.error("ERROR | The demo screening could not be completed. Please retry.")
            if result.error_code:
                st.caption(f"Demo error code: {result.error_code}")
        st.markdown(f"**Suggested next step:** {result.recommended_next_step}")
        st.caption(f"Demo-only record count: {result.dataset_record_count}")


def render_safety_guidance() -> None:
    """Place core medical-safety limitations in a prominent, readable notice."""
    st.markdown("## Safety notice")
    st.warning(
        "This prototype does not authenticate medicines or certify that a product is genuine or safe. "
        "No alert match does not prove safety. Confirm details against the package and consult a qualified "
        "pharmacist or official DRAP information when in doubt."
    )


def render_help() -> None:
    """Offer concise photo and status guidance without cluttering the main flow."""
    with st.expander("Help and limitations"):
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
