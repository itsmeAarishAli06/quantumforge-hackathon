# Planned Python contracts

All shared models live in `common/schemas.py`; no module should define a second copy. Contracts are independent of Streamlit, Gemini, and SQLite. Extra fields are rejected to catch interface drift. Unreadable medicine fields are `None`, optionally named in `unreadable_fields`.

```python
def extract_medicine_details(image_path: str | Path) -> MedicineDetails: ...
def check_drap_alerts(medicine_details: MedicineDetails) -> VerificationResult: ...
```

`MedicineDetails` carries medicine/generic name, strength, dosage form, manufacturer and address, batch, manufacturing/expiry dates, registration number, barcode, observations, unreadable fields, notes, extraction method, and manual-review flag. Every extracted field that cannot be read remains absent. The extraction method returns validated data or raises a typed extraction/input error in its future implementation; it does not make alert or safety decisions.

`AlertRecord` carries alert ID/type, documented product details, source title/URL, source excerpt, validation status, and review date. Optional source facts remain null. `MatchedAlert` pairs an alert record with one or more explicit match reasons. The result statuses are `ALERT_MATCH`, `VERIFICATION_REQUIRED`, `NO_MATCH_FOUND`, and `ERROR`.

`VerificationResult` includes status, submitted `MedicineDetails`, traceable matching records, match reasons, missing/uncertain information, recommended next step, manual-review requirement, dataset count, and an optional stable error code. Schema validation requires evidence for `ALERT_MATCH` and disallows unvalidated alert records as matches. The future verifier must use `ERROR` for unavailable/corrupt data or failed queries; it must not report a no-match when lookup did not complete.

## Error expectations

- Invalid/unsupported image: input error before provider call.
- Provider unavailable or malformed response: extraction error; never fabricate missing values.
- Invalid contract: validation error surfaced safely for correction/review.
- Missing/corrupt database or failed query: verification `ERROR`.
- Empty valid dataset or completed lookup with no match: `NO_MATCH_FOUND`, explicitly qualified as limited to available validated records.
- Ambiguous or insufficient details: `VERIFICATION_REQUIRED`.
- Positive match: `ALERT_MATCH` only with validated source evidence and deterministic reasons.
