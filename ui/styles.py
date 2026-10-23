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
            --dm-page-bg: #F7F9F8;
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
            background: #FFFFFF;
            border: 1px solid var(--dm-border);
            border-radius: 0.85rem;
            padding: 0.75rem 1.25rem;
            margin-bottom: 1.25rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 2px 8px rgba(16, 29, 45, 0.03);
          }}
          .dm-brand-left {{
            display: flex;
            align-items: center;
            gap: 0.85rem;
          }}
          .dm-brand-mark {{
            width: 2.75rem;
            height: 2.75rem;
            display: grid;
            place-items: center;
            flex: none;
            border-radius: 0.75rem;
            background: linear-gradient(135deg, var(--dm-dark-teal) 0%, var(--dm-emerald) 100%);
            color: #FFFFFF;
            font-weight: 800;
            font-size: 1.05rem;
            letter-spacing: -0.02em;
            box-shadow: 0 3px 10px rgba(8, 127, 112, 0.25);
          }}
          .dm-brand-title {{
            margin: 0;
            color: var(--dm-navy);
            font-size: 1.35rem;
            line-height: 1.15;
            font-weight: 800;
            letter-spacing: -0.02em;
          }}
          .dm-brand-subtitle {{
            margin: 0.15rem 0 0;
            color: var(--dm-text-muted);
            font-size: 0.82rem;
            font-weight: 500;
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
            background-color: #FFFFFF !important;
            border-right: 1px solid var(--dm-border) !important;
          }}
          .dm-sidebar-brand {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.5rem 0 1rem;
            border-bottom: 1px solid var(--dm-border);
            margin-bottom: 1rem;
          }}
          .dm-sidebar-card {{
            background: var(--dm-page-bg);
            border: 1px solid var(--dm-border);
            border-radius: 0.65rem;
            padding: 0.85rem;
            margin: 0.75rem 0;
            font-size: 0.82rem;
          }}

          /* ------------------------------------------------------------- */
          /* Footer & Trust                                                */
          /* ------------------------------------------------------------- */
          .dm-footer {{
            margin-top: 3rem;
            padding-top: 1.75rem;
            border-top: 1px solid var(--dm-border);
            color: var(--dm-text-muted);
            font-size: 0.88rem;
            line-height: 1.6;
          }}

          {rtl_css}

          @media (max-width: 640px) {{
            .dm-topbar {{ flex-direction: column; gap: 0.75rem; }}
            .dm-hero-title {{ font-size: 1.55rem; }}
            .dm-hero {{ padding: 1.25rem 1rem; }}
          }}
        </style>
        """,
        unsafe_allow_html=True,
    )
