# Dawa-Muhafiz architecture

**Phase:** Frontend demo. A Streamlit user flow and synthetic demo service are implemented; there is no real image extraction, database, or alert matcher.

## Purpose and scope

Dawa-Muhafiz is planned as a local Python modular monolith for screening packaging details against a reviewed local dataset of official DRAP alerts. The future application extracts what is visibly printed, lets a person review uncertain fields, then compares details with validated alert records. A photograph and missing alert match can never establish that a medicine is genuine, authentic, safe, counterfeit, or approved.

## Component architecture

```mermaid
flowchart LR
  User --> UI[Future Streamlit UI\napp.py]
  UI --> Image[Image validation\nai/image_processing.py]
  Image --> Extract[Extraction orchestration\nai/medicine_extractor.py]
  Extract --> Provider[Configurable vision provider\nai/vision_provider.py]
  Provider --> Extract
  Extract --> Contracts[Shared Pydantic contracts\ncommon/schemas.py]
  UI --> Matcher[Deterministic matcher\nverification/alert_matcher.py]
  Matcher --> DB[(Future SQLite index)]
  JSON[Reviewed JSON records\ndata/] --> Loader[Future importer\nverification/data_loader.py]
  Loader --> DB
  Matcher --> Contracts
  Contracts --> UI
  DRAP[Official DRAP documents] -. manual review and evidence .-> JSON
```

All modules will run in one process. `common/schemas.py` owns shared Pydantic models and enums; AI and verification modules depend on these contracts, never on each other's implementation. The verifier will be deterministic and independent of the vision provider. JSON source records are portable reviewed inputs; SQLite is a future local query index.

## Module responsibilities

| Module | Responsibility | Current phase |
|---|---|---|
| `app.py` | Streamlit layout, upload validation/preview, session state, and demo workflow | Implemented for synthetic demo |
| `ui/components.py` | Reusable result and safety presentation | Implemented |
| `ui/demo_service.py` | Fixed synthetic extraction and selectable result scenarios | Implemented; no API or matching logic |
| `common/schemas.py` | Single source for medicine, alert, evidence, and result models | Implemented and tested |
| `ai/image_processing.py` | Validate/decode image; impose size and pixel limits; temporary preprocessing | Documented interface only |
| `ai/vision_provider.py` | Provider-neutral extraction contract; later Gemini adapter | Protocol only; no API calls |
| `ai/medicine_extractor.py` | Orchestrate image preparation and structured extraction | Documented interface only |
| `verification/data_loader.py` | Import reviewed JSON records and provenance into local index | Documented interface only |
| `verification/database.py` | Future SQLite schema/index access | Documented interface only |
| `verification/alert_matcher.py` | Deterministic comparison and evidence-backed result | Documented interface only |
| `data/` | Reviewed source records and provenance guidance | No alert records included |

## Data ownership and safety boundary

AI owns only the extraction of visible text and uncertainty. It must not generate a safety/authenticity verdict or fill unknown values by guessing. The data reviewer owns whether a source record is supported by an original official document. The deterministic matcher owns whether provided fields satisfy explicit comparison rules. The UI owns clear wording and evidence display, not the decision itself.

Only records checked against official source documents may be eligible for positive matches. Every positive match must carry source title, URL, excerpt, and match reasons. Candidate or synthetic records are never presented as official. `NO_MATCH_FOUND` means no match in the available validated records; it does not establish authenticity, approval, or safety. Technical failures yield `ERROR`.

## Error handling

Invalid or corrupt images stop before provider calls. Provider unavailability, malformed provider output, contract validation errors, missing/corrupt database, and query failures remain distinguishable failures and must never be converted into a no-match. User-facing errors should be concise and avoid exposing secrets or raw provider exceptions. Missing/uncertain information is represented explicitly and requests manual review.

## Privacy and security

Future upload handling must constrain extensions, decoded formats, bytes, and pixel count; avoid persistent image storage by default and remove temporary files. API keys belong in ignored `.env` files, never source or logs. Treat OCR/provider strings as untrusted and escape them in the UI. Use parameterized SQL. Do not log uploaded images, personal data, or full provider responses unnecessarily. Keep local databases and runtime artifacts out of version control.

## Future integration points

The agreed functions are `extract_medicine_details(image_path) -> MedicineDetails` and `check_drap_alerts(medicine_details) -> VerificationResult`. Provider configuration will come from environment variables. A future importer will validate JSON before indexing it. The UI will allow review/editing of extracted fields before calling verification. See [API contracts](api_contracts.md), [data flow](data_flow.md), and [database design](database_design.md).

## Included and deferred

Included: Python package layout, shared Pydantic contracts, Streamlit demo UI, in-memory image validation and preview, editable fields, synthetic demo extraction/scenarios, documentation, and tests. Deferred: Gemini calls, OCR, real extraction, SQLite operations, JSON importer, matching logic, scraping, authentication, deployment, and production medical verification. No actual alert records or verification results are supplied.
