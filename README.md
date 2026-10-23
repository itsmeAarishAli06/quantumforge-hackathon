# Dawa-Muhafiz

Dawa-Muhafiz is an academic medicine alert screening prototype for Pakistan. It is intended to help review visible packaging details against an available set of official DRAP alerts. It does not authenticate medicines or certify safety.

## Current phase

Phase 4 provides a Streamlit frontend with in-memory image preview, editable medicine fields, Gemini vision extraction when configured, and a separate synthetic demo path. **The app does not contact DRAP, access an alert database, or perform real alert matching.** Synthetic demo values and result panels are clearly labelled.

The interface uses a navy/teal theme, grouped editable details, a clear upload/review flow, text labels for each state, and a visible safety notice. Native Streamlit controls remain in use; small CSS styles decorate static branding and step labels.

## Setup and run (PowerShell)

Requires Python 3.11 or newer.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env and set GEMINI_API_KEY to your own key before live extraction.
streamlit run app.py
```

Run tests in another terminal with the environment activated:

```powershell
python -m pytest -q
```

The uploader accepts JPG/JPEG and PNG, limits files to 10 MB by default, validates the actual decoded format, and does not save uploads to disk. To use live extraction, configure `GEMINI_API_KEY`; optionally set `GEMINI_MODEL` and `GEMINI_TIMEOUT_MS`. Uploaded bytes are transmitted to Google Gemini only after the user presses **Extract with Gemini**. Do not upload images containing personal information. The model may misread text; review every field against the package.

If the key is unavailable, the app explains setup and keeps **Use synthetic demo details** available. This fixture is unrelated to the uploaded image. The result scenario selector previews four synthetic interface states and is not a medicine lookup control. The sample alert evidence uses an `example.org` fixture and is explicitly marked synthetic.

## Project map

- `app.py`: page layout, upload validation, session state, editable details, and demo workflow.
- `ui/components.py`: reusable result and safety panels.
- `ui/demo_service.py`: fixed synthetic extraction fixture and scenario results; no matching or API calls.
- `common/schemas.py`: shared Pydantic contracts.
- `ai/`: image validation, Gemini adapter, and schema-validated extraction.
- `verification/`: future reviewed-data import and deterministic matching; real alert verification is not implemented.
- `docs/`: architecture, contracts, data flow, database design, collaboration workflow, and roadmap.

Never interpret `NO_MATCH_FOUND` as proof of authenticity, approval, or safety. For concerns, check the package and consult a qualified pharmacist or official DRAP information. Do not commit API keys, images, local databases, or personal data.

## Gemini setup and limitations

The project uses Google's maintained `google-genai` Python SDK with a configurable Gemini model (default `gemini-3.8-flash`) and JSON-structured output validated into `MedicineDetails`. Get a Gemini API key through Google's AI Studio, place it only in the ignored local `.env`, and restart Streamlit. No automated test uses a key or makes a network call. Without a key, live extraction is disabled and the app does not silently invent a response.

Image recognition can omit or misread small, blurred, curved, or obscured package text. Unknown values remain empty; ambiguous dates stay unset and require review. The image is sent to Google only when a live extraction is explicitly requested. No alert data is queried by this phase, and this prototype does not provide medical advice or authenticate medicine.

Official SDK references: [Google Gen AI Python SDK](https://github.com/googleapis/python-genai), [Gemini image input](https://ai.google.dev/gemini-api/docs/image-understanding), and [structured output](https://ai.google.dev/gemini-api/docs/structured-output).
