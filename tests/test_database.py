"""Unit tests for the SQLite verification database layer."""

from pathlib import Path
import sqlite3
import pytest

from verification.database import (
    fetch_validated_alerts,
    fetch_validated_count,
    get_connection,
    init_database,
)
from verification.data_loader import load_reviewed_alerts

DEFAULT_JSON = Path(__file__).resolve().parents[1] / "data" / "drap_alerts.json"


def test_init_database_creates_tables(tmp_path):
    test_db = tmp_path / "init_test.db"
    init_database(test_db)
    assert test_db.is_file()

    conn = get_connection(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='alerts';")
    row = cursor.fetchone()
    conn.close()
    assert row is not None
    assert row[0] == "alerts"


def test_fetch_validated_count_empty(tmp_path):
    test_db = tmp_path / "empty.db"
    init_database(test_db)
    assert fetch_validated_count(test_db) == 0


def test_fetch_validated_alerts_returns_typed_schemas(tmp_path):
    test_db = tmp_path / "populated.db"
    load_reviewed_alerts(DEFAULT_JSON, db_path=test_db)

    count = fetch_validated_count(test_db)
    assert count == 20

    alerts = fetch_validated_alerts(test_db)
    assert len(alerts) == 20
    for a in alerts:
        assert a.validation_status == "validated"
        assert a.product_name
        assert "dra.gov.pk" in str(a.source_url)
        assert a.supporting_excerpt
