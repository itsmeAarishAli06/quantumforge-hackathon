"""Planned importer for reviewed JSON alert records.

Only source-supported facts with documented provenance may be imported.
Candidate/unreviewed rows must never be eligible for positive matches.
"""

from pathlib import Path


def load_reviewed_alerts(source_path: str | Path) -> int:
    """Validate and import reviewed records; importer is deferred."""
    raise NotImplementedError("Alert importing is planned, not implemented yet.")
