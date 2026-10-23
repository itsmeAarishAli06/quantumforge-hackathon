# Collaboration workflow

Keep `main` stable. The team may agree to use a `develop` integration branch; do not create it by default. Each change belongs on a focused feature branch, for example `feature/project-foundation`, `feature/frontend`, `feature/ai-extraction`, `feature/alert-database`, `feature/verification-engine`, `test/integration-tests`, or `docs/project-documentation`.

Before work, update from the agreed integration branch. Commit small coherent changes, run relevant tests, then open a pull request for review. Reviewers check safety language, schema compatibility, tests, and source provenance before merge. Resolve conflicts in shared files with the owners before accepting edits.

## Ownership proposal

- Developer A: future Streamlit UI and integration.
- Developer B: image handling, extraction, and provider configuration.
- Developer C (if available): reviewed DRAP data, import, SQLite, deterministic verification.
- Shared: schemas, integration tests, docs, and review. Combine roles explicitly if the team has fewer members.

Coordinate changes to `common/schemas.py`, `requirements.txt`, `.env.example`, and integration entry points. Never duplicate model definitions or change status meanings in one module alone. Do not add fabricated or unreviewed DRAP data. No remote repository, push, branch creation, or history changes are performed by this foundation setup.
