"""Small, centralized visual treatment for static UI decoration only."""

import streamlit as st


def apply_styles() -> None:
    """Style static branded blocks; interactive controls remain native Streamlit."""
    st.markdown(
        """
        <style>
          .dm-brand-row { display:flex; align-items:center; gap:.85rem; margin:.25rem 0 1rem; }
          .dm-brand-mark { width:3rem; height:3rem; display:grid; place-items:center; flex:none;
            border-radius:1rem; background:#DCEFED; color:#075C60; font-weight:800; font-size:1.05rem; }
          .dm-brand-name { margin:0; color:#142F3A; font-size:1.55rem; line-height:1.15; font-weight:750; }
          .dm-brand-sub { margin:.25rem 0 0; color:#526872; font-size:.98rem; }
          .dm-demo-pill { display:inline-block; margin-top:.7rem; padding:.28rem .65rem;
            border:1px solid #D39B37; border-radius:999px; background:#FFF7E5; color:#68480A;
            font-size:.78rem; font-weight:750; letter-spacing:.04em; }
          .dm-hero { padding:1rem 0 .25rem; }
          .dm-hero-title { margin:0 0 .55rem; color:#142F3A; font-size:clamp(1.65rem,3.4vw,2.25rem);
            line-height:1.18; font-weight:750; }
          .dm-hero-copy { max-width:48rem; margin:0; color:#526872; font-size:1.05rem; line-height:1.55; }
          .dm-step-number { display:inline-grid; place-items:center; width:1.8rem; height:1.8rem;
            margin:0 .45rem .25rem 0; border-radius:50%; background:#DCEFED; color:#075C60; font-weight:750; }
          .dm-muted { color:#526872; }
          @media (max-width: 640px) {
            .dm-brand-name { font-size:1.3rem; }
            .dm-hero { padding-top:.4rem; }
          }
        </style>
        """,
        unsafe_allow_html=True,
    )
