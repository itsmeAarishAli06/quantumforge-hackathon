"""Deterministic DRAP alert verification engine.

Compares user-reviewed medicine packaging details against the local validated
DRAP alert database using conservative, multi-field deterministic rules.

Cardinal Medical Safety Invariants:
1. Deterministic matching only: AI is never used to decide if an alert matches.
2. An alert match requires traceable, validated official DRAP evidence.
3. NO_MATCH_FOUND means only that no record was found in the checked dataset;
   it never implies that a medicine is authentic, approved, or safe.
4. Failures in database access or parsing return ERROR, never NO_MATCH_FOUND.
"""

from pathlib import Path
import re

from common.schemas import (
    AlertRecord,
    MatchedAlert,
    MedicineDetails,
    VerificationResult,
    VerificationStatus,
)
from verification.database import database_path, fetch_validated_alerts, fetch_validated_count
from verification.data_loader import load_reviewed_alerts


DEFAULT_DATASET_JSON = Path(__file__).resolve().parents[1] / "data" / "drap_alerts.json"


def normalize_text(text: str | None) -> str:
    """Normalize text conservatively: case-fold, strip noise punctuation, collapse whitespace."""
    if not text:
        return ""
    # Case fold
    cleaned = text.casefold()
    # Strip trademark and registration symbols
    cleaned = re.sub(r"[®™©]", "", cleaned)
    # Replace dashes, slashes, and underscores with spaces for word tokenization
    cleaned = re.sub(r"[-_/\\,;:]", " ", cleaned)
    # Collapse multiple spaces
    return " ".join(cleaned.split())


def normalize_batch(batch: str | None) -> str:
    """Normalize batch strings: strip whitespace and noise, preserve alphanumerics and leading zeros."""
    if not batch:
        return ""
    cleaned = batch.strip().casefold()
    # Strip common prefixes like 'batch:', 'lot:', 'b.no:'
    cleaned = re.sub(r"^(batch|lot|b\.no|bno)[\s.:#-]*", "", cleaned)
    # Remove whitespace
    return re.sub(r"\s+", "", cleaned)


def normalize_strength(strength: str | None) -> str:
    """Normalize common strength expressions without altering unit values."""
    if not strength:
        return ""
    cleaned = strength.strip().casefold()
    cleaned = re.sub(r"\s*(mg|mcg|g|ml|iu|%)\b", r"\1", cleaned)
    return re.sub(r"\s+", "", cleaned)


def _token_match(submitted_name: str, alert_name: str) -> bool:
    """Check if primary brand or product name matches with conservative boundary."""
    norm_sub = normalize_text(submitted_name)
    norm_alert = normalize_text(alert_name)

    if not norm_sub or not norm_alert:
        return False

    # Exact normalized match
    if norm_sub == norm_alert:
        return True

    sub_tokens = set(norm_sub.split())
    alert_tokens = set(norm_alert.split())

    # Stopwords that are too generic to establish product identity on their own
    stopwords = {"tablets", "tablet", "capsules", "capsule", "injection", "infusion",
                 "syrup", "suspension", "drops", "cream", "liquid", "mg", "ml", "ds",
                 "forte", "oral", "ophthalmic", "solution", "each", "pack", "sterile"}

    sub_core = sub_tokens - stopwords
    alert_core = alert_tokens - stopwords

    if not sub_core or not alert_core:
        return False

    # Primary brand token match (e.g., 'brexin', 'gabica', 'venofer', 'danzen', 'zetol', 'caricef')
    # If the core brand name is present in both:
    if sub_core.issubset(alert_core) or alert_core.issubset(sub_core):
        return True

    # At least one meaningful specific brand token matches
    common = sub_core.intersection(alert_core)
    for token in common:
        if len(token) >= 4:  # Specific name token
            return True

    return False


def _check_conflicts(details: MedicineDetails, alert: AlertRecord) -> list[str]:
    """Identify conflicting attributes (e.g. differing strengths or dosage forms)."""
    conflicts: list[str] = []

    # Check strength conflict
    if details.strength and alert.strength:
        norm_sub_str = normalize_strength(details.strength)
        norm_alert_str = normalize_strength(alert.strength)
        if norm_sub_str and norm_alert_str and norm_sub_str != norm_alert_str:
            # If neither is a substring of the other
            if norm_sub_str not in norm_alert_str and norm_alert_str not in norm_sub_str:
                conflicts.append(f"Strength mismatch (Packaging: {details.strength} vs Alert: {alert.strength})")

    # Check dosage form conflict
    if details.dosage_form and alert.dosage_form:
        norm_sub_form = normalize_text(details.dosage_form)
        norm_alert_form = normalize_text(alert.dosage_form)
        if norm_sub_form and norm_alert_form and norm_sub_form != norm_alert_form:
            conflicts.append(f"Dosage form mismatch (Packaging: {details.dosage_form} vs Alert: {alert.dosage_form})")

    return conflicts


def check_drap_alerts(
    medicine_details: MedicineDetails,
    db_path: Path | None = None,
) -> VerificationResult:
    """Deterministically compare reviewed packaging details against validated DRAP alerts.

    Returns a typed VerificationResult matching the shared domain contract.
    """
    target_db = db_path or database_path()

    # Step 1: Ensure dataset is loaded and accessible
    try:
        count = fetch_validated_count(target_db)
        if count == 0 and DEFAULT_DATASET_JSON.is_file():
            load_reviewed_alerts(DEFAULT_DATASET_JSON, target_db)
            count = fetch_validated_count(target_db)
    except Exception as exc:
        return VerificationResult(
            status=VerificationStatus.ERROR,
            medicine_details=medicine_details,
            matching_alerts=[],
            match_reasons=[],
            missing_or_uncertain_information=["Database is inaccessible or query failed"],
            recommended_next_step="A technical error occurred while querying the local alert database. Please retry later.",
            manual_review_required=True,
            dataset_record_count=0,
            error_code="DB_UNAVAILABLE",
        )

    if count == 0:
        return VerificationResult(
            status=VerificationStatus.NO_MATCH_FOUND,
            medicine_details=medicine_details,
            matching_alerts=[],
            match_reasons=[],
            missing_or_uncertain_information=["No validated alert records are loaded in the database."],
            recommended_next_step="No validated alerts are available in the local database. This does not confirm medicine safety or authenticity.",
            manual_review_required=True,
            dataset_record_count=0,
            error_code=None,
        )

    # Step 2: Validate input sufficiency
    sub_name = medicine_details.medicine_name or ""
    sub_generic = medicine_details.generic_name or ""
    sub_batch = medicine_details.batch_number or ""

    if not sub_name.strip() and not sub_batch.strip():
        return VerificationResult(
            status=VerificationStatus.VERIFICATION_REQUIRED,
            medicine_details=medicine_details,
            matching_alerts=[],
            match_reasons=[],
            missing_or_uncertain_information=["medicine_name", "batch_number"],
            recommended_next_step="Please provide at least a medicine brand name or batch number to screen against DRAP alerts.",
            manual_review_required=True,
            dataset_record_count=count,
            error_code=None,
        )

    # Step 3: Fetch validated alerts and evaluate deterministic rules
    alerts = fetch_validated_alerts(target_db)

    positive_matches: list[tuple[AlertRecord, list[str]]] = []
    inconclusive_notes: list[str] = []

    norm_sub_batch = normalize_batch(sub_batch)

    for alert in alerts:
        reasons: list[str] = []

        # Evaluate product name / generic name match
        name_matched = False
        if sub_name and _token_match(sub_name, alert.product_name):
            name_matched = True
            reasons.append(f"Product name matches official alert: '{alert.product_name}'")
        elif sub_generic and alert.generic_name and _token_match(sub_generic, alert.generic_name):
            name_matched = True
            reasons.append(f"Active ingredient matches official alert: '{alert.generic_name}'")

        # Evaluate batch matching
        alert_has_batch = bool(alert.batch_number and alert.batch_number.strip())
        norm_alert_batch = normalize_batch(alert.batch_number) if alert_has_batch else ""

        # Batch-specific alert case
        if alert_has_batch:
            if norm_sub_batch:
                # Check for exact batch match
                if norm_sub_batch == norm_alert_batch:
                    # If product identity also matches:
                    if name_matched:
                        conflicts = _check_conflicts(medicine_details, alert)
                        if conflicts:
                            inconclusive_notes.append(
                                f"Batch '{alert.batch_number}' matches alert for '{alert.product_name}', but details conflict: {'; '.join(conflicts)}."
                            )
                        else:
                            reasons.append(f"Exact affected batch number match: '{alert.batch_number}'")
                            positive_matches.append((alert, reasons))
                    else:
                        # Batch matches, but product name is known and unrelated
                        if sub_name.strip():
                            # Different product with coincidentally same batch string
                            pass
                        else:
                            # Product name was omitted by user, batch matched alert
                            reasons.append(f"Batch number '{alert.batch_number}' matches alert for '{alert.product_name}'.")
                            positive_matches.append((alert, reasons))
                else:
                    # Batch is known, but differs from this alert's batch
                    # Does the product name match?
                    if name_matched:
                        # This batch is different from the alert's affected batch.
                        pass
            else:
                # Submitted batch is MISSING/unreadable, but product name matches a batch-specific alert!
                if name_matched:
                    inconclusive_notes.append(
                        f"Product '{alert.product_name}' matches a DRAP alert for batch '{alert.batch_number}', "
                        "but the packaging is missing a batch number. Check package for batch number."
                    )
        else:
            # Product-wide alert (alert applies to all batches, e.g. unregistered product like Zetol)
            if name_matched:
                conflicts = _check_conflicts(medicine_details, alert)
                if conflicts:
                    inconclusive_notes.append(
                        f"Product '{alert.product_name}' matches a product-wide alert, but attributes conflict: {'; '.join(conflicts)}."
                    )
                else:
                    reasons.append(f"Product-level alert match (applies to all batches): '{alert.product_name}'")
                    positive_matches.append((alert, reasons))

    # Step 4: Synthesize VerificationResult
    if positive_matches:
        matched_alerts = [
            MatchedAlert(alert=alert_rec, match_reasons=r_list)
            for alert_rec, r_list in positive_matches
        ]
        all_reasons = [r for _, r_list in positive_matches for r in r_list]
        return VerificationResult(
            status=VerificationStatus.ALERT_MATCH,
            medicine_details=medicine_details,
            matching_alerts=matched_alerts,
            match_reasons=all_reasons,
            missing_or_uncertain_information=[],
            recommended_next_step=(
                "Do not consume or dispense this medicine batch. Review the official DRAP alert evidence, "
                "quarantine the product, and consult a licensed pharmacist or DRAP field force."
            ),
            manual_review_required=True,
            dataset_record_count=count,
            error_code=None,
        )

    if inconclusive_notes:
        return VerificationResult(
            status=VerificationStatus.VERIFICATION_REQUIRED,
            medicine_details=medicine_details,
            matching_alerts=[],
            match_reasons=[],
            missing_or_uncertain_information=inconclusive_notes,
            recommended_next_step=(
                "Verification is inconclusive. Product matches an official alert entry, but batch or formulation "
                "details require manual confirmation. Inspect physical packaging or consult a pharmacist."
            ),
            manual_review_required=True,
            dataset_record_count=count,
            error_code=None,
        )

    # Clean no-match result
    return VerificationResult(
        status=VerificationStatus.NO_MATCH_FOUND,
        medicine_details=medicine_details,
        matching_alerts=[],
        match_reasons=[],
        missing_or_uncertain_information=[],
        recommended_next_step=(
            "No matching alert was found in the available validated DRAP database. "
            "This does NOT confirm that the medicine is genuine, authentic, approved, or safe."
        ),
        manual_review_required=True,
        dataset_record_count=count,
        error_code=None,
    )
