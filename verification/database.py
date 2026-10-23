"""SQLite database access boundary for Dawa-Muhafiz.

Manages connection pooling, schema initialization, and parameterized read-only
queries against the local validated DRAP alert index.
"""

from datetime import date
import os
from pathlib import Path
import sqlite3

from common.schemas import AlertRecord, AlertType


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DB_REL_PATH = Path("data") / "dawa_muhafiz.db"


def database_path() -> Path:
    """Resolve configured local database path from environment or default."""
    env_path = os.getenv("DATABASE_PATH", "").strip()
    if env_path:
        p = Path(env_path)
        return p if p.is_absolute() else (ROOT_DIR / p)
    return ROOT_DIR / DEFAULT_DB_REL_PATH


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    """Open a connection to the SQLite database with row factory enabled."""
    target_path = db_path or database_path()
    target_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(target_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_database(db_path: Path | None = None) -> None:
    """Initialize SQLite schema and indexes idempotently."""
    conn = get_connection(db_path)
    try:
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS alerts (
                    alert_id TEXT PRIMARY KEY,
                    alert_type TEXT NOT NULL,
                    product_name TEXT NOT NULL,
                    generic_name TEXT,
                    active_ingredient TEXT,
                    manufacturer_name TEXT,
                    batch_number TEXT,
                    strength TEXT,
                    dosage_form TEXT,
                    registration_number TEXT,
                    publication_date TEXT,
                    source_title TEXT NOT NULL,
                    source_url TEXT NOT NULL,
                    supporting_excerpt TEXT NOT NULL,
                    validation_status TEXT NOT NULL,
                    reviewed_at TEXT,
                    source_sha256 TEXT,
                    created_at TEXT NOT NULL
                );
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_alerts_product_name ON alerts(product_name);"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_alerts_batch_number ON alerts(batch_number);"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_alerts_validation_status ON alerts(validation_status);"
            )
    finally:
        conn.close()


def row_to_alert_record(row: sqlite3.Row) -> AlertRecord:
    """Map a database row safely into the Pydantic AlertRecord contract."""
    pub_date = None
    if row["publication_date"]:
        try:
            pub_date = date.fromisoformat(row["publication_date"])
        except ValueError:
            pub_date = None

    rev_date = None
    if row["reviewed_at"]:
        try:
            rev_date = date.fromisoformat(row["reviewed_at"])
        except ValueError:
            rev_date = None

    return AlertRecord(
        alert_id=row["alert_id"],
        alert_type=AlertType(row["alert_type"]),
        product_name=row["product_name"],
        generic_name=row["generic_name"],
        active_ingredient=row["active_ingredient"],
        manufacturer_name=row["manufacturer_name"],
        batch_number=row["batch_number"],
        strength=row["strength"],
        dosage_form=row["dosage_form"],
        registration_number=row["registration_number"],
        publication_date=pub_date,
        source_title=row["source_title"],
        source_url=row["source_url"],
        supporting_excerpt=row["supporting_excerpt"],
        validation_status=row["validation_status"],
        reviewed_at=rev_date,
    )


def fetch_validated_alerts(db_path: Path | None = None) -> list[AlertRecord]:
    """Retrieve all validated DRAP alert records from the index."""
    init_database(db_path)
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM alerts 
            WHERE validation_status = 'validated'
            ORDER BY publication_date DESC, alert_id ASC;
            """
        )
        rows = cursor.fetchall()
        return [row_to_alert_record(r) for r in rows]
    finally:
        conn.close()


def fetch_validated_count(db_path: Path | None = None) -> int:
    """Return the total number of validated alert records available in SQLite."""
    init_database(db_path)
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM alerts WHERE validation_status = 'validated';")
        count = cursor.fetchone()[0]
        return int(count)
    finally:
        conn.close()
