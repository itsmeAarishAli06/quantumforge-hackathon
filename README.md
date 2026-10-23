<<<<<<< HEAD
# Dawa-Muhafiz

Dawa-Muhafiz is a planned medicine safety screening prototype for Pakistan. Its intended purpose is to extract visible packaging details and compare them with a locally maintained, reviewed dataset of official DRAP alerts.

## Current state

This repository is at the **foundation stage**. Shared Pydantic v2 contracts and future module boundaries are present. The Streamlit UI, image extraction, SQLite operations, and alert matching are not implemented. No real alert records or verification results are included.

The system must never say that a medicine is genuine, authentic, safe, or counterfeit based on a photo or on the absence of a match. `NO_MATCH_FOUND` means only that no match was found in the available validated dataset. A technical failure is an error, not a no-match.

## Setup

Requires Python 3.11 or newer.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m pytest
```

The test suite currently checks shared contracts and package imports. There is no runnable application yet; `app.py` intentionally reports that the UI is deferred.

## Project map

- `common/schemas.py`: single shared source for medicine, source-alert, match-evidence, and verification contracts.
- `ai/`: future image processing and provider adapter; extraction only, no safety decision.
- `verification/`: future reviewed-data import, SQLite access, and deterministic matching.
- `data/`: provenance guidance; no fabricated or unreviewed alerts.
- `docs/`: architecture, data flow, database, contracts, collaboration workflow, and roadmap.

See [docs/architecture.md](docs/architecture.md) and [CONTRIBUTING.md](CONTRIBUTING.md) before starting module work. Never commit API keys, uploaded images, local databases, or private user data. A real alert must be checked against an official source and include traceable evidence.
=======
# quantumforge-hackathon
Building innovative AI-powered solutions to solve real-world problems through intelligent technology. 
>>>>>>> 5700318f26c4e097b7c2fcbca722a8aa536f9d10
