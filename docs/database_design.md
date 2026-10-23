# Planned database design

**Status:** Design only; SQLite access and import are deferred.

SQLite will index reviewed JSON records for local queries. JSON remains the reviewable portable source. One alert row represents one product/batch assertion supported by a source; a document covering several batches may create several rows with shared source metadata. Unknown facts remain null.

| Column | Type | Requirement / meaning |
|---|---|---|
| `alert_id` | TEXT primary key | Stable internal record identifier |
| `alert_type` | TEXT | `rapid_alert`, `recall_alert`, or documented other type |
| `product_name` | TEXT | Product name as shown in source |
| `generic_name`, `active_ingredient` | TEXT nullable | Only where documented |
| `manufacturer_name` | TEXT nullable | Only where documented |
| `batch_number` | TEXT nullable | Exact lot/batch as documented |
| `strength`, `dosage_form` | TEXT nullable | Only where documented |
| `registration_number` | TEXT nullable | Only where documented |
| `publication_date` | TEXT nullable | ISO date, if available in source |
| `source_title`, `source_url` | TEXT | Original official document title and URL |
| `supporting_excerpt` | TEXT | Short source passage supporting fields/classification |
| `validation_status` | TEXT | `validated`, `candidate`, or `rejected`; only validated is matchable |
| `reviewed_at` | TEXT nullable | Reviewer date; required for validated records |
| `source_sha256` | TEXT | Hash of captured source document for provenance/change review |
| `created_at` | TEXT | Import timestamp |

Planned indexes: `product_name`, `batch_number`, and `validation_status`; add manufacturer index only if query volume warrants it. No foreign key is needed in the MVP: source metadata travels with each record, which keeps each match self-contained. A later normalized source-document table is only justified if many rows share documents and need coordinated updates.

## Import process

1. A reviewer reads the original official DRAP document and records only supported facts, source metadata, excerpt, review date, and validation status in JSON.
2. The loader validates each row against the shared schema plus import-specific provenance rules.
3. It rejects malformed dates/URLs, missing source evidence, duplicate IDs, and attempts to mark an unreviewed record validated.
4. It imports transactionally with parameterized statements and can rebuild the local database idempotently.
5. Candidate/rejected records may be retained for team review but are excluded from all matching queries.

If the SQLite file is missing, future startup may build it from the reviewed JSON. If both source JSON and database are missing, verification returns `ERROR`. If data loads successfully but contains zero validated records, the result must say that no reviewed alerts are available; no-match is not a safety claim. If no row matches, return `NO_MATCH_FOUND` with the dataset limitation.
