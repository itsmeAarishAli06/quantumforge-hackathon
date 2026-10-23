# Dawa-Muhafiz (دوا محافظ) — Medicine Safety & Alert Screening

Dawa-Muhafiz is an academic medicine alert screening prototype for Pakistan. It helps review visible packaging details and deterministically compares them against a curated dataset of official DRAP (Drug Regulatory Authority of Pakistan) Rapid Alerts and Recall notices.

**Strict Medical Safety Boundary:**
Dawa-Muhafiz checks for matching records in its available alert database. It does not certify that a medicine is genuine, authentic, or safe. `NO_MATCH_FOUND` does not prove safety.

---

## Current phase: Phase 5

Phase 5 introduces a reliable, deterministic medicine alert verification engine that compares reviewed medicine details against a locally stored, traceable SQLite index populated from official DRAP Rapid Alerts and Class I/II Recalls.

### Key Capabilities

1. **AI Vision Packaging Extraction**: Extracts medicine name, generic name, batch number, dates, manufacturer, and strength via Google Gemini structured output with in-memory validation.
2. **Review & Correction Workflow**: Users can inspect and correct any extracted values before running alert verification.
3. **Deterministic Verification Engine**: Multi-field matching across product name, active ingredient, batch number, strength, and dosage form. AI is never used to make verification decisions.
4. **Conservative Batch Matching**:
   - Exact batch match on affected batch yields `ALERT_MATCH` with complete regulatory evidence.
   - Known batch that differs from the alert's affected batch yields `NO_MATCH_FOUND`.
   - Missing batch on packaging when product matches a batch-specific alert yields `VERIFICATION_REQUIRED`.
   - Product-level alerts (e.g. unregistered or spurious products) match all batches.
5. **Traceable DRAP Evidence**: 20 official DRAP alerts indexed with source URLs (`dra.gov.pk`), publication dates, official titles, and exact regulatory excerpts.
6. **Regulatory Registry Explorer**: An interactive alert registry in the Alert Intelligence view allows users to browse and search all indexed DRAP alerts.
7. **Clinical Screening Summary Export**: Downloadable and printable text report citing submitted details, outcome, official evidence, and precautionary guidance.

---

## Setup and run (PowerShell)

Requires Python 3.11 or newer.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env and set GEMINI_API_KEY to your own key for live AI extraction.
streamlit run app.py
```

Run the complete test suite in another terminal with the environment activated:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

---

## How It Works

1. **Upload packaging photo**: Accepts JPG/JPEG and PNG (up to 10 MB). Images are kept in session memory only and are never saved to disk.
2. **Extract details**:
   - With an API key: extracts visible text via Google Gemini Vision (`gemini-2.5-flash`).
   - Without an API key: users can enter details manually or use the clearly marked synthetic demo fixture.
3. **Review & correct**: Edit any field to correct OCR mistakes.
4. **Check against DRAP alerts**: Click **Check Against Official DRAP Alerts** to deterministically query the local SQLite database.
5. **Evidence-backed results**: Review official DRAP evidence, precautionary warnings, and recommended actions.

---

## Project Map

- `app.py`: Streamlit application layout, navigation, packaging review workflow, and verification interface.
- `verification/alert_matcher.py`: Conservative, deterministic multi-field matching engine.
- `verification/database.py`: Local SQLite database connection, schema, and parameterized queries.
- `verification/data_loader.py`: JSON alert importer with strict provenance validation and metadata tracking.
- `data/drap_alerts.json`: 20 official DRAP alerts with full regulatory provenance.
- `ui/components.py`: Evidence cards, clinical report export, alert registry, and multilingual navigation.
- `ui/demo_service.py`: Fixed synthetic demo fixtures for offline development and testing.
- `common/schemas.py`: Shared Pydantic contracts and domain models.
- `ai/`: Image processing, Gemini vision adapter, and schema extraction.
- `docs/`: Architecture, contracts, database design, and collaboration workflows.

---

## Medical Safety Principles

- AI only extracts text from photos; it never authenticates medicine or decides alerts.
- An alert match requires traceable, validated official DRAP evidence.
- `NO_MATCH_FOUND` means only that no record was found in the checked database; it never implies that a medicine is authentic, approved, or safe.
- Technical failures in database access or parsing return `ERROR`, never `NO_MATCH_FOUND`.
