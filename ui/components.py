"""Reusable presentation components; no screening or fixture logic lives here."""

import streamlit as st

from common.schemas import VerificationResult, VerificationStatus


def render_result(result: VerificationResult) -> None:
    """Render a validated result and its demo-only status/evidence."""
    st.markdown("### Screening result")
    st.caption("SYNTHETIC DEMONSTRATION RESULT · Not a DRAP lookup")
    with st.container(border=True):
        if result.status == VerificationStatus.ALERT_MATCH:
            st.error("ALERT MATCH · Synthetic demo scenario")
            for item in result.matching_alerts:
                st.markdown(f"**Classification:** {item.alert.alert_type.value}")
                st.markdown(f"**Evidence:** {item.alert.supporting_excerpt}")
                st.markdown(f"**Source label:** {item.alert.source_title}")
                st.markdown(f"**Demo URL:** {item.alert.source_url}")
                st.markdown("**Why shown:** " + "; ".join(item.match_reasons))
                st.warning("This is synthetic test evidence, not an official DRAP alert or source.")
        elif result.status == VerificationStatus.VERIFICATION_REQUIRED:
            st.warning("VERIFICATION REQUIRED")
            st.write("The available demo details are insufficient or marked for review.")
            if result.missing_or_uncertain_information:
                st.write("Review: " + ", ".join(result.missing_or_uncertain_information))
            st.write("Check the physical packaging or consult a qualified pharmacist.")
        elif result.status == VerificationStatus.NO_MATCH_FOUND:
            st.info("NO MATCH FOUND in the synthetic demo dataset.")
            st.write("This does not prove the medicine is genuine, approved, or safe.")
        elif result.status == VerificationStatus.ERROR:
            st.error("The demo screening could not be completed. Please retry.")
            if result.error_code:
                st.caption(f"Demo error code: {result.error_code}")
        st.write(result.recommended_next_step)
        st.caption(f"Demo dataset records: {result.dataset_record_count}")


def render_safety_guidance() -> None:
    """Show concise safe-use and image guidance."""
    st.markdown("### Safety and photo guidance")
    st.markdown(
        "- Use a clear photograph showing product name, manufacturer, batch number, and expiry date where present.\n"
        "- Confirm displayed details against the physical packaging.\n"
        "- A missing alert match does not establish authenticity or safety.\n"
        "- Consult a qualified pharmacist or official DRAP information if you are unsure."
    )
