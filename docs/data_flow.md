# Planned data flow

**Image validation, Gemini extraction, and review are implemented when the provider is configured.** The interface also offers an explicit synthetic extraction option. The alert lookup portion is still a future design; synthetic result panels remain test fixtures and are not a real match.

```mermaid
sequenceDiagram
  actor Person
  participant UI as Streamlit UI
  participant Image as Image validation
  participant AI as Vision/OCR extraction
  participant Contract as common/schemas.py
  participant Verify as Deterministic verifier
  participant DB as Local validated-alert index
  Person->>UI: Upload packaging image
  UI->>Image: Validate format, size, and decode
  Image-->>UI: Validated in-memory image or input error
  UI->>AI: Request visible field extraction (Gemini, if configured)
  AI->>Contract: Validate structured MedicineDetails
  Contract-->>UI: Details with missing/uncertain fields
  UI-->>Person: Review/correct extracted fields
  Person->>UI: Confirm reviewed details
  UI->>Verify: check_drap_alerts(details)
  Verify->>DB: Query validated records
  DB-->>Verify: Candidate source-backed records
  Verify-->>UI: VerificationResult and reasons/evidence
  UI-->>Person: Status, source, limitations, next step
```

The UI validates the upload before sending it to any provider. AI returns only typed extraction fields. Unreadable values stay unknown. After a person reviews details, a deterministic verifier checks the local validated dataset. A positive match includes traceable official evidence. A no-match message says the dataset search found no match and does not imply authenticity or safety. Any failure is an error, not a no-match.
