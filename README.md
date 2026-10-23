# Dawa-Muhafiz

Dawa-Muhafiz is an academic medicine alert screening prototype for Pakistan. It is intended to help review visible packaging details against an available set of official DRAP alerts. It does not authenticate medicines or certify safety.

## Current phase

Phase 2 provides a Streamlit frontend with in-memory image preview, editable medicine fields, synthetic demo extraction, and selectable synthetic screening states. **It does not analyze the uploaded image, call Gemini/OCR, contact DRAP, access a database, or perform real alert matching.** Every demo value and result is marked synthetic.

## Setup and run (PowerShell)

Requires Python 3.11 or newer.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
streamlit run app.py
```

Run tests in another terminal with the environment activated:

```powershell
python -m pytest -q
```

The uploader accepts JPG/JPEG and PNG, limits files to 10 MB by default, validates the actual decoded format, and does not save uploads to disk. The limit can be changed with `MAX_UPLOAD_BYTES`; Streamlit's upload cap is configured in `.streamlit/config.toml` and must be adjusted to match if the limit changes.

## Project map

- `app.py`: page layout, upload validation, session state, editable details, and demo workflow.
- `ui/components.py`: reusable result and safety panels.
- `ui/demo_service.py`: fixed synthetic extraction fixture and scenario results; no matching or API calls.
- `common/schemas.py`: shared Pydantic contracts.
- `ai/` and `verification/`: future integration boundaries; real extraction and verification are not implemented.
- `docs/`: architecture, contracts, data flow, database design, collaboration workflow, and roadmap.

Never interpret `NO_MATCH_FOUND` as proof of authenticity, approval, or safety. For concerns, check the package and consult a qualified pharmacist or official DRAP information. Do not commit API keys, images, local databases, or personal data.
