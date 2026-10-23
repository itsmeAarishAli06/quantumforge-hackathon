"""Planned SQLite access boundary; full persistence is deferred.

Future implementation should expose parameterized, read-only alert queries and
initialize/rebuild the local index from reviewed JSON source records.
"""

from pathlib import Path


def database_path() -> Path:
    """Resolve configured local database path. Configuration comes later."""
    raise NotImplementedError("SQLite access is planned, not implemented yet.")
