"""Deterministic DRAP alert verification engine and SQLite data access layer."""

from verification.alert_matcher import check_drap_alerts
from verification.data_loader import AlertImportError, get_dataset_metadata, load_reviewed_alerts
from verification.database import (
    database_path,
    fetch_validated_alerts,
    fetch_validated_count,
    get_connection,
    init_database,
)

__all__ = [
    "AlertImportError",
    "check_drap_alerts",
    "database_path",
    "fetch_validated_alerts",
    "fetch_validated_count",
    "get_connection",
    "get_dataset_metadata",
    "init_database",
    "load_reviewed_alerts",
]
