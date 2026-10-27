"""Centralized visual design system and styles for Dawa-Muhafiz.

Theme: Premium Digital Healthcare SaaS Palette:
- Deep midnight navy: #101D2D
- Dark teal: #123C43
- Primary emerald: #087F70
- Soft mint: #E7F5F0
- Warm off-white: #F7F9F8
- White surfaces: #FFFFFF
- Primary text: #182630
- Secondary text: #64747D
- Subtle borders: #E3EAE8
- Caution amber: #F0B64D
- Alert red: #C63D45
- Informational blue: #356BB3

Fully supports Right-to-Left (RTL) for Urdu and Sindhi.
"""

import streamlit as st


def apply_styles(is_rtl_mode: bool = False) -> None:
    """Inject centralized CSS styling for a clinical, trustworthy healthcare interface."""
    rtl_css = (
        """
        /* RTL support for Urdu and Sindhi */
        .dm-localized-container {
            direction: rtl;
            text-align: right;
            font-family: 'Noto Nastaliq Urdu', 'Noto Sans Arabic', 'Jameel Noori Nastaleeq', 'Segoe UI', Tahoma, sans-serif;
        }
        .dm-localized-container .stMarkdown p,
        .dm-localized-container .stMarkdown h1,
        .dm-localized-container .stMarkdown h2,
        .dm-localized-container .stMarkdown h3 {
            text-align: right;
            line-height: 1.85;
        }
        .dm-brand-row { flex-direction: row-reverse; }
        .dm-step-number { margin: 0 0 .25rem .5rem; }
        .dm-nav-pill-group { flex-direction: row-reverse; }
        """
        if is_rtl_mode
        else """
        .dm-localized-container {
            direction: ltr;
            text-align: left;
        }
        """
    )

    st.markdown(
        f"""
        <style>
          /* ------------------------------------------------------------- */
          /* Root CSS Variables                                            */
          /* ------------------------------------------------------------- */
          :root {{
            --dm-navy: #101D2D;
            --dm-dark-teal: #123C43;
            --dm-emerald: #087F70;
            --dm-soft-mint: #E7F5F0;
            --dm-page-bg: #F4F7F7;
            --dm-surface: #FFFFFF;
            --dm-text: #182630;
            --dm-text-muted: #64747D;
            --dm-border: #E3EAE8;
            --dm-amber: #F0B64D;
            --dm-red: #C63D45;
            --dm-blue: #356BB3;
          }}

          /* ------------------------------------------------------------- */
          /* Global Layout & Typography                                    */
          /* ------------------------------------------------------------- */
          .stApp {{
            background-color: var(--dm-page-bg);
            color: var(--dm-text);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
          }}

          h1, h2, h3, h4, h5, h6 {{
            color: var(--dm-text) !important;
            letter-spacing: -0.015em;
            font-weight: 750;
          }}

          /* ------------------------------------------------------------- */
          /* Top Navigation Bar Component                                  */
          /* ------------------------------------------------------------- */
          .dm-topbar {{
            position: relative;
            overflow: hidden;
            background: linear-gradient(115deg, #FFFFFF 0%, #FFFFFF 65%, #F0F8F6 100%);
            border: 1px solid #DDE8E5;
            border-radius: 1rem;
            padding: 1rem 1.35rem;
            margin: 0.15rem 0 1.1rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            box-shadow: 0 8px 26px rgba(16, 45, 50, 0.055);
          }}
          .dm-brand-left {{
            display: flex;
            align-items: center;
            gap: 0.9rem;
            min-width: 0;
          }}
          .dm-brand-mark {{
            width: 3rem;
            height: 3rem;
            display: grid;
            place-items: center;
            flex: none;
            border-radius: 0.9rem;
            background: linear-gradient(145deg, #143C43 0%, #087F70 78%, #2AA68D 100%);
            color: #FFFFFF;
            font-weight: 800;
            font-size: 1.05rem;
            letter-spacing: -0.02em;
            box-shadow: 0 5px 13px rgba(8, 127, 112, 0.2);
          }}
          .dm-brand-mark span {{
            border: 1px solid rgba(255, 255, 255, 0.35);
            border-radius: 0.58rem;
            padding: 0.15rem 0.25rem;
          }}
          .dm-brand-copy {{
            min-width: 0;
          }}
          .dm-brand-eyebrow {{
            display: block;
            margin-bottom: 0.16rem;
            color: var(--dm-emerald);
            font-size: 0.62rem;
            font-weight: 800;
            letter-spacing: 0.13em;
          }}
          .dm-brand-title {{
            margin: 0;
            color: var(--dm-navy);
            font-size: 1.24rem;
            line-height: 1.15;
            font-weight: 800;
            letter-spacing: -0.02em;
          }}
          .dm-brand-urdu {{
            margin-left: 0.3rem;
            color: var(--dm-emerald);
            font-size: 0.9rem;
            font-weight: 600;
            letter-spacing: 0;
          }}
          .dm-brand-subtitle {{
            margin: 0.2rem 0 0;
            color: var(--dm-text-muted);
            font-size: 0.77rem;
            font-weight: 500;
          }}
          .dm-topbar-meta {{
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 0.55rem;
            flex-wrap: wrap;
          }}
          .dm-prototype-badge,
          .dm-topbar-status,
          .dm-current-view {{
            display: inline-flex;
            align-items: center;
            gap: 0.42rem;
            min-height: 2rem;
            padding: 0.38rem 0.7rem;
            border: 1px solid var(--dm-border);
            border-radius: 999px;
            font-size: 0.68rem;
            font-weight: 750;
            line-height: 1.2;
          }}
          .dm-prototype-badge {{
            background: #F4F6F8;
            border-color: #E5E9ED;
            color: #54616D;
            letter-spacing: 0.07em;
          }}
          .dm-topbar-status {{
            background: #EAF7F2;
            border-color: #CCE9DD;
            color: #17684F;
          }}
          .dm-topbar-status.dm-status-demo {{
            background: #FFF7E8;
            border-color: #F3E2BB;
            color: #8A5A10;
          }}
          .dm-status-dot,
          .dm-version-dot {{
            width: 0.48rem;
            height: 0.48rem;
            flex: none;
            border-radius: 50%;
            background: #22956F;
            box-shadow: 0 0 0 3px rgba(34, 149, 111, 0.12);
          }}
          .dm-status-demo .dm-status-dot {{
            background: #D69A2D;
            box-shadow: 0 0 0 3px rgba(214, 154, 45, 0.14);
          }}
          .dm-current-view {{
            background: #FFFFFF;
            color: #4B5962;
          }}

          /* Top Nav Pills */
          .dm-nav-pill-group {{
            display: flex;
            align-items: center;
            gap: 0.4rem;
            background: var(--dm-page-bg);
            padding: 0.25rem 0.35rem;
            border-radius: 9999px;
            border: 1px solid var(--dm-border);
          }}
          .dm-nav-pill {{
            padding: 0.35rem 0.85rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--dm-text-muted);
            text-decoration: none;
            transition: all 0.15s ease-in-out;
          }}
          .dm-nav-pill:hover {{
            color: var(--dm-emerald);
            background: rgba(8, 127, 112, 0.06);
          }}
          .dm-nav-pill.active {{
            background: var(--dm-soft-mint);
            color: var(--dm-emerald);
            font-weight: 700;
          }}

          /* ------------------------------------------------------------- */
          /* Status Badges & Pills                                         */
          /* ------------------------------------------------------------- */
          .dm-demo-pill {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            margin-top: 0.4rem;
            padding: 0.25rem 0.65rem;
            border: 1px solid var(--dm-border);
            border-radius: 999px;
            background: #FFFFFF;
            color: var(--dm-text-muted);
            font-size: 0.74rem;
            font-weight: 700;
            letter-spacing: 0.03em;
            text-transform: uppercase;
          }}
          .dm-pill-configured {{
            background: var(--dm-soft-mint);
            color: var(--dm-emerald);
            border-color: #B4E2D5;
          }}
          .dm-pill-demo {{
            background: #FFFBEB;
            color: #92400E;
            border-color: #FDE68A;
          }}

          /* ------------------------------------------------------------- */
          /* Hero Section                                                  */
          /* ------------------------------------------------------------- */
          .dm-hero {{
            background: linear-gradient(180deg, #FFFFFF 0%, var(--dm-page-bg) 100%);
            border: 1px solid var(--dm-border);
            border-radius: 1rem;
            padding: 2.2rem 2rem 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 16px rgba(16, 29, 45, 0.03);
          }}
          .dm-hero-title {{
            margin: 0 0 0.65rem;
            color: var(--dm-navy);
            font-size: clamp(1.85rem, 3.4vw, 2.5rem);
            line-height: 1.2;
            font-weight: 800;
            letter-spacing: -0.025em;
          }}
          .dm-hero-copy {{
            max-width: 48rem;
            margin: 0 0 1.25rem;
            color: var(--dm-text-muted);
            font-size: 1.1rem;
            line-height: 1.6;
          }}

          /* ------------------------------------------------------------- */
          /* Workflow Cards (01, 02, 03)                                   */
          /* ------------------------------------------------------------- */
          .dm-wf-card {{
            background: var(--dm-surface);
            border: 1px solid var(--dm-border);
            border-radius: 0.85rem;
            padding: 1.4rem;
            height: 100%;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            box-shadow: 0 2px 6px rgba(16, 29, 45, 0.02);
          }}
          .dm-wf-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 18px rgba(8, 127, 112, 0.08);
            border-color: #C0DCD6;
          }}
          .dm-wf-num {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 2.2rem;
            height: 2.2rem;
            border-radius: 0.6rem;
            background: var(--dm-soft-mint);
            color: var(--dm-emerald);
            font-weight: 800;
            font-size: 0.95rem;
            margin-bottom: 0.85rem;
          }}
          .dm-wf-title {{
            margin: 0 0 0.45rem;
            font-size: 1.1rem;
            font-weight: 750;
            color: var(--dm-text);
          }}
          .dm-wf-desc {{
            margin: 0;
            color: var(--dm-text-muted);
            font-size: 0.92rem;
            line-height: 1.5;
          }}

          /* Step Numbers (Check Medicine workflow) */
          .dm-step-number {{
            display: inline-grid;
            place-items: center;
            width: 1.85rem;
            height: 1.85rem;
            margin: 0 0.5rem 0.25rem 0;
            border-radius: 50%;
            background: var(--dm-soft-mint);
            color: var(--dm-emerald);
            font-weight: 800;
            font-size: 0.88rem;
          }}
          .dm-muted {{ color: var(--dm-text-muted); }}

          /* ------------------------------------------------------------- */
          /* Clean Cards & Surfaces                                        */
          /* ------------------------------------------------------------- */
          .dm-card {{
            background: var(--dm-surface);
            border: 1px solid var(--dm-border);
            border-radius: 0.85rem;
            padding: 1.35rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 2px 6px rgba(16, 29, 45, 0.02);
          }}
          .dm-card-title {{
            margin: 0 0 0.85rem;
            color: var(--dm-navy);
            font-size: 1.18rem;
            font-weight: 750;
            display: flex;
            align-items: center;
            justify-content: space-between;
          }}

          /* Photography Tips Box */
          .dm-tips-box {{
            background: var(--dm-surface);
            border: 1px solid var(--dm-border);
            border-left: 4px solid var(--dm-emerald);
            padding: 0.95rem 1.15rem;
            border-radius: 0 0.65rem 0.65rem 0;
            margin: 0.75rem 0 1.25rem;
            font-size: 0.92rem;
            color: var(--dm-text);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
          }}

          /* ------------------------------------------------------------- */
          /* Safety Results Panels (Four Semantics)                        */
          /* ------------------------------------------------------------- */
          .dm-result-card {{
            border-radius: 0.95rem;
            padding: 1.5rem;
            margin: 1.25rem 0;
            border: 1px solid var(--dm-border);
            box-shadow: 0 4px 14px rgba(16, 29, 45, 0.04);
          }}
          .dm-res-match {{
            background: #FEF2F2;
            border-color: #FECACA;
            border-left: 6px solid var(--dm-red);
          }}
          .dm-res-req {{
            background: #FFFBEB;
            border-color: #FDE68A;
            border-left: 6px solid var(--dm-amber);
          }}
          .dm-res-nomatch {{
            background: #F8FAFC;
            border-color: var(--dm-border);
            border-left: 6px solid var(--dm-text-muted);
          }}
          .dm-res-error {{
            background: #FEF2F2;
            border-color: #FCA5A5;
            border-left: 6px solid var(--dm-red);
          }}

          .dm-res-title {{
            font-size: 1.3rem;
            font-weight: 800;
            margin: 0 0 0.6rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
          }}
          .dm-match-title {{ color: #991B1B; }}
          .dm-req-title {{ color: #92400E; }}
          .dm-nomatch-title {{ color: var(--dm-navy); }}
          .dm-error-title {{ color: #991B1B; }}

          /* Evidence Box */
          .dm-evidence-card {{
            background: #FFFFFF;
            border: 1px solid var(--dm-border);
            border-radius: 0.75rem;
            padding: 1.2rem;
            margin-top: 0.95rem;
          }}
          .dm-evidence-badge {{
            display: inline-block;
            background: var(--dm-soft-mint);
            color: var(--dm-emerald);
            font-size: 0.78rem;
            font-weight: 750;
            padding: 0.25rem 0.65rem;
            border-radius: 0.35rem;
            margin-bottom: 0.6rem;
            letter-spacing: 0.02em;
          }}
          .dm-excerpt-quote {{
            background: var(--dm-page-bg);
            border-left: 3px solid var(--dm-emerald);
            padding: 0.75rem 1rem;
            margin: 0.75rem 0;
            font-size: 0.92rem;
            color: var(--dm-text);
            font-style: italic;
            border-radius: 0 0.4rem 0.4rem 0;
          }}

          /* ------------------------------------------------------------- */
          /* Field Badges                                                  */
          /* ------------------------------------------------------------- */
          .dm-tag-extracted {{
            display: inline-block;
            background: var(--dm-soft-mint);
            color: var(--dm-emerald);
            font-size: 0.72rem;
            font-weight: 700;
            padding: 0.15rem 0.5rem;
            border-radius: 0.35rem;
            border: 1px solid #B4E2D5;
          }}
          .dm-tag-edited {{
            display: inline-block;
            background: #EFF6FF;
            color: var(--dm-blue);
            font-size: 0.72rem;
            font-weight: 700;
            padding: 0.15rem 0.5rem;
            border-radius: 0.35rem;
            border: 1px solid #BFDBFE;
          }}

          /* ------------------------------------------------------------- */
          /* Sidebar Styling                                               */
          /* ------------------------------------------------------------- */
          section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #FFFFFF 0%, #F9FBFA 100%) !important;
            border-right: 1px solid #DFE8E5 !important;
          }}
          section[data-testid="stSidebar"] > div:first-child {{
            padding-top: 1.1rem;
          }}
          .dm-sidebar-brand {{
            display: flex;
            align-items: center;
            gap: 0.7rem;
            padding: 0.2rem 0 1.05rem;
            border-bottom: 1px solid #E8EEEC;
            margin-bottom: 1.1rem;
          }}
          .dm-sidebar-mark {{
            width: 2.55rem;
            height: 2.55rem;
            border-radius: 0.78rem;
            font-size: 0.9rem;
          }}
          .dm-sidebar-mark span {{
            border-radius: 0.48rem;
            padding: 0.12rem 0.2rem;
          }}
          .dm-sidebar-brand-copy {{
            display: flex;
            flex-direction: column;
            gap: 0.08rem;
          }}
          .dm-sidebar-eyebrow {{
            color: var(--dm-emerald);
            font-size: 0.56rem;
            font-weight: 800;
            letter-spacing: 0.11em;
          }}
          .dm-sidebar-brand-copy strong {{
            color: var(--dm-navy);
            font-size: 1rem;
            line-height: 1.25;
          }}
          .dm-sidebar-urdu {{
            color: #64747D;
            font-size: 0.72rem;
            line-height: 1.25;
          }}
          .dm-sidebar-section-label {{
            margin: 0.15rem 0 0.45rem;
            color: #76858A;
            font-size: 0.63rem;
            font-weight: 800;
            letter-spacing: 0.12em;
          }}
          .dm-language-heading {{
            margin-top: 1.05rem;
          }}
          .dm-system-heading {{
            margin-top: 1.05rem;
          }}
          section[data-testid="stSidebar"] div[data-testid="stRadio"] > div[role="radiogroup"] {{
            gap: 0.25rem;
          }}
          section[data-testid="stSidebar"] div[data-testid="stRadio"] label {{
            min-height: 2.35rem;
            padding: 0.18rem 0.6rem;
            border: 1px solid transparent;
            border-radius: 0.65rem;
            color: #45545C;
            transition: background 0.16s ease, border-color 0.16s ease, color 0.16s ease;
          }}
          section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {{
            background: #F1F7F5;
            border-color: #E2EEEA;
            color: var(--dm-dark-teal);
          }}
          section[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) {{
            background: #E9F5F1;
            border-color: #D2E9E0;
            color: #126653;
            font-weight: 700;
          }}
          .dm-sidebar-status {{
            padding: 0.78rem 0.85rem;
            border: 1px solid #D7EADF;
            border-radius: 0.8rem;
            background: linear-gradient(135deg, #F0F8F4 0%, #EAF5F0 100%);
          }}
          .dm-sidebar-status-demo {{
            border-color: #EFE3C9;
            background: linear-gradient(135deg, #FFFAF0 0%, #FBF3E3 100%);
          }}
          .dm-sidebar-status-heading {{
            display: flex;
            align-items: center;
            gap: 0.55rem;
            color: #155B48;
            font-size: 0.82rem;
          }}
          .dm-sidebar-status-demo .dm-sidebar-status-heading {{
            color: #815A18;
          }}
          .dm-sidebar-status-detail {{
            display: block;
            overflow-wrap: anywhere;
            margin: 0.38rem 0 0 0.98rem;
            color: #6A7777;
            font-size: 0.7rem;
          }}
          .dm-sidebar-card {{
            display: flex;
            align-items: flex-start;
            gap: 0.65rem;
            padding: 0.78rem;
            margin: 0.65rem 0;
            border: 1px solid #E4EAE8;
            border-radius: 0.78rem;
            background: rgba(255, 255, 255, 0.82);
          }}
          .dm-sidebar-card-icon {{
            display: grid;
            place-items: center;
            width: 1.65rem;
            height: 1.65rem;
            flex: none;
            border-radius: 0.55rem;
            background: #EDF5F2;
            color: #19745F;
            font-size: 0.95rem;
            font-weight: 800;
          }}
          .dm-sidebar-card > div:last-child {{
            display: flex;
            flex-direction: column;
            gap: 0.22rem;
          }}
          .dm-sidebar-card strong {{
            color: #24333A;
            font-size: 0.76rem;
          }}
          .dm-sidebar-card span:not(.dm-sidebar-card-icon) {{
            color: var(--dm-text-muted);
            font-size: 0.69rem;
            line-height: 1.45;
          }}
          .dm-sidebar-version {{
            display: flex;
            align-items: center;
            gap: 0.38rem;
            padding-top: 0.75rem;
            border-top: 1px solid #E8EEEC;
            color: #7A888D;
            font-size: 0.58rem;
            font-weight: 750;
            letter-spacing: 0.08em;
          }}
          .dm-version-dot {{
            width: 0.38rem;
            height: 0.38rem;
            background: #8C9A9B;
            box-shadow: none;
          }}

          /* Streamlit's horizontal radio is the primary page navigation. */
          .stApp [data-testid="stMain"] div[data-testid="stRadio"] > div[role="radiogroup"][aria-orientation="horizontal"] {{
            gap: 0.3rem;
            padding: 0.35rem;
            border: 1px solid #E2E9E7;
            border-radius: 0.9rem;
            background: rgba(255, 255, 255, 0.86);
            box-shadow: 0 3px 12px rgba(16, 45, 50, 0.035);
          }}
          .stApp [data-testid="stMain"] div[data-testid="stRadio"] > div[role="radiogroup"][aria-orientation="horizontal"] label {{
            min-height: 2.3rem;
            padding: 0.25rem 0.65rem;
            border: 1px solid transparent;
            border-radius: 0.65rem;
            color: #56646B;
            font-size: 0.82rem;
            transition: background 0.16s ease, border-color 0.16s ease, color 0.16s ease;
          }}
          .stApp [data-testid="stMain"] div[data-testid="stRadio"] > div[role="radiogroup"][aria-orientation="horizontal"] label:hover {{
            background: #F4F8F7;
            color: var(--dm-dark-teal);
          }}
          .stApp [data-testid="stMain"] div[data-testid="stRadio"] > div[role="radiogroup"][aria-orientation="horizontal"] label:has(input:checked) {{
            background: #E9F5F1;
            border-color: #D2E9E0;
            color: #126653;
            font-weight: 700;
          }}

          /* ------------------------------------------------------------- */
          /* Footer & Trust                                                */
          /* ------------------------------------------------------------- */
          .dm-footer {{
            margin-top: 3rem;
            padding: 1.45rem 1.5rem 1rem;
            border: 1px solid #DFE8E5;
            border-radius: 1rem;
            background: linear-gradient(145deg, #FFFFFF 0%, #F7FAF9 100%);
            box-shadow: 0 6px 20px rgba(16, 45, 50, 0.04);
            color: var(--dm-text-muted);
            font-size: 0.82rem;
            line-height: 1.55;
          }}
          .dm-footer-top {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #E8EEEC;
          }}
          .dm-footer-brand {{
            display: flex;
            align-items: center;
            gap: 0.7rem;
          }}
          .dm-footer-mark {{
            display: grid;
            place-items: center;
            width: 2.25rem;
            height: 2.25rem;
            border-radius: 0.68rem;
            background: linear-gradient(145deg, #143C43, #087F70);
            color: #FFFFFF;
            font-size: 0.73rem;
            font-weight: 800;
          }}
          .dm-footer-brand strong,
          .dm-footer-brand small {{
            display: block;
          }}
          .dm-footer-brand strong {{
            color: var(--dm-navy);
            font-size: 0.87rem;
          }}
          .dm-footer-brand strong span {{
            margin-left: 0.2rem;
            color: var(--dm-emerald);
            font-weight: 600;
          }}
          .dm-footer-brand small {{
            margin-top: 0.1rem;
            color: #78868A;
            font-size: 0.68rem;
          }}
          .dm-footer-link {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            color: #126653 !important;
            font-size: 0.75rem;
            font-weight: 700;
            text-decoration: none !important;
          }}
          .dm-footer-link:hover {{
            color: #084C40 !important;
            text-decoration: underline !important;
          }}
          .dm-footer-boundary {{
            display: flex;
            align-items: center;
            gap: 0.6rem;
            margin: 0.9rem 0;
            padding: 0.72rem 0.8rem;
            border: 1px solid #F0E4C9;
            border-radius: 0.7rem;
            background: #FFFBF2;
            color: #6F592F;
          }}
          .dm-footer-boundary-icon {{
            display: grid;
            place-items: center;
            width: 1.4rem;
            height: 1.4rem;
            flex: none;
            border-radius: 50%;
            background: #F5E9CB;
            color: #805D17;
            font-size: 0.75rem;
            font-weight: 800;
          }}
          .dm-footer-boundary p {{
            margin: 0;
            font-size: 0.73rem;
          }}
          .dm-footer-boundary strong {{
            color: #59451F;
          }}
          .dm-footer-bottom {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.8rem 1.25rem;
            padding: 0.15rem 0 0.85rem;
            color: #68777B;
            font-size: 0.7rem;
          }}
          .dm-footer-meta {{
            display: flex;
            justify-content: space-between;
            gap: 0.8rem;
            padding-top: 0.75rem;
            border-top: 1px solid #E8EEEC;
            color: #879295;
            font-size: 0.64rem;
          }}

          {rtl_css}

          @media (max-width: 640px) {{
            .dm-topbar {{ align-items: flex-start; flex-direction: column; gap: 0.8rem; padding: 0.95rem; }}
            .dm-topbar-meta {{ justify-content: flex-start; }}
            .dm-prototype-badge, .dm-topbar-status, .dm-current-view {{ font-size: 0.62rem; }}
            .dm-footer {{ padding: 1rem; }}
            .dm-footer-top {{ align-items: flex-start; flex-direction: column; }}
            .dm-footer-bottom {{ grid-template-columns: 1fr; gap: 0.55rem; }}
            .dm-footer-meta {{ flex-direction: column; }}
            .dm-hero-title {{ font-size: 1.55rem; }}
            .dm-hero {{ padding: 1.25rem 1rem; }}
          }}
        </style>
        """,
        unsafe_allow_html=True,
    )
