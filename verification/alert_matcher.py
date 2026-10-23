"""Future deterministic matcher; matching logic is intentionally deferred."""

from common.schemas import MedicineDetails, VerificationResult


def check_drap_alerts(medicine_details: MedicineDetails) -> VerificationResult:
    """Compare details with validated local alerts; no matcher exists yet."""
    raise NotImplementedError("Alert matching is planned, not implemented yet.")
