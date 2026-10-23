"""Data loader and provenance validator for reviewed DRAP alert records.

Validates official source metadata before importing records into SQLite.
Candidate or unreviewed rows are never eligible for positive matching.
"""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from pydantic import ValidationError

from common.schemas import AlertRecord
from verification.database import database_path, get_connection, init_database


class AlertImportError(ValueError):
    """Raised when an alert file contains invalid schema or unverified provenance."""


def load_reviewed_alerts(source_path: str | Path, db_path: Path | None = None) -> int:
    """Validate and import reviewed alert records into the local SQLite index.

    Returns the count of validated records imported.
    """
    path = Path(source_path)
    if not path.is_file():
        raise AlertImportError(f"Alert source file not found: {path}")

    try:
        raw_data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise AlertImportError(f"Failed to read JSON alert source: {exc}") from exc

    if not isinstance(raw_data, list):
        raise AlertImportError("Alert source root must be a JSON array of alert records.")

    validated_records: list[AlertRecord] = []
    seen_ids: set[str] = set()

    for idx, item in enumerate(raw_data):
        if not isinstance(item, dict):
            raise AlertImportError(f"Record at index {idx} must be a JSON object.")

        alert_id = item.get("alert_id")
        if not alert_id or alert_id in seen_ids:
            raise AlertImportError(f"Record at index {idx} has missing or duplicate alert_id: {alert_id}")
        seen_ids.add(alert_id)

        try:
            record = AlertRecord.model_validate(item)
        except ValidationError as exc:
            raise AlertImportError(f"Validation failed for alert {alert_id}: {exc}") from exc

        # Strict Provenance Enforcement for Validated Records:
        if record.validation_status == "validated":
            if not record.supporting_excerpt or len(record.supporting_excerpt.strip()) < 5:
                raise AlertImportError(f"Validated alert {alert_id} requires a supporting excerpt from DRAP.")
            if not record.source_title:
                raise AlertImportError(f"Validated alert {alert_id} requires an official DRAP source title.")
            if not str(record.source_url).startswith("http"):
                raise AlertImportError(f"Validated alert {alert_id} requires a valid official source URL.")
            if record.reviewed_at is None:
                raise AlertImportError(f"Validated alert {alert_id} must have a recorded reviewed_at date.")

        validated_records.append(record)

    # Ingest transactionally into SQLite
    target_db = db_path or database_path()
    init_database(target_db)
    conn = get_connection(target_db)
    created_at_iso = datetime.now(timezone.utc).isoformat()

    imported_validated_count = 0
    try:
        with conn:
            for rec in validated_records:
                rec_bytes = json.dumps(rec.model_dump(mode="json"), sort_keys=True).encode("utf-8")
                sha256_hash = hashlib.sha256(rec_bytes).hexdigest()

                conn.execute(
                    """
                    INSERT OR REPLACE INTO alerts (
                        alert_id, alert_type, product_name, generic_name, active_ingredient,
                        manufacturer_name, batch_number, strength, dosage_form, registration_number,
                        publication_date, source_title, source_url, supporting_excerpt,
                        validation_status, reviewed_at, source_sha256, created_at
                    ) VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    );
                    """,
                    (
                        rec.alert_id,
                        rec.alert_type.value,
                        rec.product_name,
                        rec.generic_name,
                        rec.active_ingredient,
                        rec.manufacturer_name,
                        rec.batch_number,
                        rec.strength,
                        rec.dosage_form,
                        rec.registration_number,
                        rec.publication_date.isoformat() if rec.publication_date else None,
                        rec.source_title,
                        str(rec.source_url),
                        rec.supporting_excerpt,
                        rec.validation_status,
                        rec.reviewed_at.isoformat() if rec.reviewed_at else None,
                        sha256_hash,
                        created_at_iso,
                    ),
                )
                if rec.validation_status == "validated":
                    imported_validated_count += 1
    finally:
        conn.close()

    return imported_validated_count


def get_dataset_metadata(db_path: Path | None = None) -> dict[str, object]:
    """Return verified statistics and freshness information for the alert dataset."""
    target_db = db_path or database_path()
    init_database(target_db)
    conn = get_connection(target_db)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM alerts WHERE validation_status = 'validated';")
        validated_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM alerts;")
        total_count = cursor.fetchone()[0]

        cursor.execute("SELECT MAX(publication_date) FROM alerts WHERE validation_status = 'validated';")
        latest_pub = cursor.fetchone()[0]

        cursor.execute("SELECT MAX(reviewed_at) FROM alerts WHERE validation_status = 'validated';")
        latest_rev = cursor.fetchone()[0]

        return {
            "validated_count": int(validated_count),
            "total_count": int(total_count),
            "latest_publication_date": latest_pub,
            "latest_reviewed_date": latest_rev,
            "database_path": str(target_db),
            "is_synthetic": False if validated_count > 0 else True,
        }
    finally:
        conn.close()
