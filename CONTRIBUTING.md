# Contributing

This is a student-team project with a modular-monolith design. Keep `main` stable. The team may use `develop` as an integration branch if agreed; otherwise, open reviewed feature branches against `main`.

## Workflow

1. Pull the latest agreed integration branch before starting.
2. Create a focused branch, for example `feature/ai-extraction`, `feature/alert-database`, `feature/frontend`, `test/integration-tests`, or `docs/project-documentation`.
3. Keep changes small and commit with a clear message.
4. Run relevant tests and open a pull request for review.
5. Coordinate changes to shared contracts, dependency files, and app integration before merging.

Do not rewrite shared model definitions independently in module packages. `common/schemas.py` is the single contract source. Resolve schema changes with all module owners and update contract tests and docs in the same change. Do not add real alert data without official source evidence and review metadata. Do not commit secrets, uploads, or generated databases.

Suggested ownership: Developer A owns future UI and integration; Developer B owns image extraction and provider configuration; Developer C owns reviewed alert records and deterministic verification. For a smaller team, combine roles explicitly. Schemas, integration, tests, and documentation are shared responsibilities.
