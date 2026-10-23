# Implementation roadmap

The foundation is complete and Phase 2 provides the synthetic UI demo. Continue in small phases, keeping synthetic data visibly separate from official records.

| Phase | Owner(s) | Main files | Acceptance |
|---|---|---|---|
| 1. Review contracts | All | `common/schemas.py`, `docs/api_contracts.md` | Team agrees on field optionality, statuses, and matching evidence rules. |
| 2. UI shell (complete) | A + integration | `app.py`, `ui/*`, frontend tests | In-memory upload/review/result flow; synthetic fixtures labelled; no verification claim. |
| 3. Image and extraction (implemented) | B | `ai/*`, extraction tests, `.env.example` | Gemini structured extraction is implemented; validated images yield typed fields; unreadable fields remain unknown; provider failures are explicit. Configure a key and complete a manual live-image check. |
| 4. Reviewed data and DB | C | `data/*`, `verification/database.py`, `data_loader.py` | Source review metadata is complete; import is idempotent; candidates cannot match. |
| 5. Deterministic matcher | C + all | `verification/alert_matcher.py`, unit tests | Exact, missing, conflicting, ambiguous, and no-match cases have deterministic explanations. |
| 6. Integration | All | `app.py`, integration tests | User-reviewed details reach matcher; all statuses and failures display safely with evidence. |
| 7. Demo and handoff | All | README/docs/tests | Clean setup, repeatable demo, documented limitations; no-match caveat is clear. |

Foundation commands from the repository root:

```powershell
python -m pip install -r requirements.txt
python -m pytest
```

Later phase commands should be added with each implementation. Do not run a live provider or use a real medicine image in automated tests without an explicit privacy and cost decision.
