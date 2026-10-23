"""Unit tests for the DRAP alert data loader and provenance validator."""

import json
from pathlib import Path
import pytest

from verification.data_loader import (
    AlertImportError,
    get_dataset_metadata,
    load_reviewed_alerts,
)


DEFAULT_JSON = Path(__file__).resolve().parents[1] / "data" / "drap_alerts.json"


def test_load_default_alerts_into_sqlite(tmp_path):
    test_db = tmp_path / "test_drap.db"
    count = load_reviewed_alerts(DEFAULT_JSON, db_path=test_db)
    assert count == 20

    meta = get_dataset_metadata(db_path=test_db)
    assert meta["validated_count"] == 20
    assert meta["is_synthetic"] is False
    assert meta["latest_publication_date"] is not None


def test_reject_missing_source_file(tmp_path):
    with pytest.raises(AlertImportError, match="not found"):
        load_reviewed_alerts(tmp_path / "nonexistent.json", db_path=tmp_path / "test.db")


def test_reject_duplicate_alert_id(tmp_path):
    bad_data = [
        {
            "alert_id": "DRAP-DUP-01",
            "alert_type": "rapid_alert",
            "product_name": "Product 1",
            "source_title": "DRAP Alert",
            "source_url": "https://dra.gov.pk/a",
            "supporting_excerpt": "Official excerpt 1",
            "validation_status": "validated",
            "reviewed_at": "2026-01-01",
        },
        {
            "alert_id": "DRAP-DUP-01",
            "alert_type": "rapid_alert",
            "product_name": "Product 2",
            "source_title": "DRAP Alert",
            "source_url": "https://dra.gov.pk/b",
            "supporting_excerpt": "Official excerpt 2",
            "validation_status": "validated",
            "reviewed_at": "2026-01-01",
        },
    ]
    bad_file = tmp_path / "dup.json"
    bad_file.write_text(json.dumps(bad_data), encoding="utf-8")

    with pytest.raises(AlertImportError, match="duplicate alert_id"):
        load_reviewed_alerts(bad_file, db_path=tmp_path / "test.db")


def test_reject_missing_excerpt_on_validated_alert(tmp_path):
    bad_data = [
        {
            "alert_id": "DRAP-FAIL-01",
            "alert_type": "recall_alert",
            "product_name": "Product Without Excerpt",
            "source_title": "DRAP Recall",
            "source_url": "https://dra.gov.pk/alert",
            "supporting_excerpt": "abcd",  # Too short (< 5 chars)
            "validation_status": "validated",
            "reviewed_at": "2026-01-01",
        }
    ]
    bad_file = tmp_path / "no_excerpt.json"
    bad_file.write_text(json.dumps(bad_data), encoding="utf-8")

    with pytest.raises(AlertImportError, match="supporting excerpt"):
        load_reviewed_alerts(bad_file, db_path=tmp_path / "test.db")


def test_reject_missing_reviewed_at_on_validated_alert(tmp_path):
    bad_data = [
        {
            "alert_id": "DRAP-FAIL-02",
            "alert_type": "recall_alert",
            "product_name": "Product Without Review Date",
            "source_title": "DRAP Recall",
            "source_url": "https://dra.gov.pk/alert",
            "supporting_excerpt": "Valid excerpt text",
            "validation_status": "validated",
            "reviewed_at": None,  # Missing!
        }
    ]
    bad_file = tmp_path / "no_review.json"
    bad_file.write_text(json.dumps(bad_data), encoding="utf-8")

    with pytest.raises(AlertImportError, match="reviewed_at"):
        load_reviewed_alerts(bad_file, db_path=tmp_path / "test.db")
