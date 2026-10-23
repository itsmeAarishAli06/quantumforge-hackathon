"""Provider- and persistence-independent contracts shared across the application."""

from datetime import date
from enum import StrEnum
from typing import Annotated

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, field_validator, model_validator


ShortText = Annotated[str, Field(min_length=1, max_length=300)]
EvidenceText = Annotated[str, Field(min_length=1, max_length=4000)]


class ContractModel(BaseModel):
    """Base class that rejects accidental, unreviewed contract fields."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class AlertType(StrEnum):
    RAPID_ALERT = "rapid_alert"
    RECALL_ALERT = "recall_alert"
    OTHER = "other"


class VerificationStatus(StrEnum):
    ALERT_MATCH = "ALERT_MATCH"
    VERIFICATION_REQUIRED = "VERIFICATION_REQUIRED"
    NO_MATCH_FOUND = "NO_MATCH_FOUND"
    ERROR = "ERROR"


class MedicineDetails(ContractModel):
    """Visible package details; absent or unreadable values remain ``None``."""

    medicine_name: ShortText | None = None
    generic_name: ShortText | None = None
    strength: ShortText | None = None
    dosage_form: ShortText | None = None
    manufacturer_name: ShortText | None = None
    manufacturer_address: Annotated[str, Field(max_length=1000)] | None = None
    batch_number: ShortText | None = None
    manufacturing_date: date | None = None
    expiry_date: date | None = None
    registration_number: ShortText | None = None
    barcode_value: Annotated[str, Field(max_length=128)] | None = None
    packaging_observations: list[Annotated[str, Field(max_length=500)]] = Field(default_factory=list)
    unreadable_fields: list[ShortText] = Field(default_factory=list)
    extraction_notes: list[Annotated[str, Field(max_length=500)]] = Field(default_factory=list)
    extraction_method: ShortText | None = None
    requires_manual_review: bool = True

    @field_validator("unreadable_fields")
    @classmethod
    def field_names_are_unique(cls, value: list[str]) -> list[str]:
        if len(value) != len(set(value)):
            raise ValueError("unreadable_fields must not contain duplicates")
        return value


class AlertRecord(ContractModel):
    """Source-supported alert facts; optional facts must not be inferred."""

    alert_id: ShortText
    alert_type: AlertType
    product_name: ShortText
    generic_name: ShortText | None = None
    active_ingredient: ShortText | None = None
    manufacturer_name: ShortText | None = None
    batch_number: ShortText | None = None
    strength: ShortText | None = None
    dosage_form: ShortText | None = None
    registration_number: ShortText | None = None
    publication_date: date | None = None
    source_title: ShortText
    source_url: AnyHttpUrl
    supporting_excerpt: EvidenceText
    validation_status: str = Field(pattern=r"^(validated|candidate|rejected)$")
    reviewed_at: date | None = None


class MatchedAlert(ContractModel):
    """Alert evidence returned with a verification result."""

    alert: AlertRecord
    match_reasons: list[ShortText] = Field(min_length=1)

    @field_validator("alert")
    @classmethod
    def only_validated_alerts_can_match(cls, alert: AlertRecord) -> AlertRecord:
        if alert.validation_status != "validated":
            raise ValueError("only validated alert records may be returned as matches")
        return alert


class VerificationResult(ContractModel):
    """Deterministic screening result; never an authenticity or safety verdict."""

    status: VerificationStatus
    medicine_details: MedicineDetails
    matching_alerts: list[MatchedAlert] = Field(default_factory=list)
    match_reasons: list[ShortText] = Field(default_factory=list)
    missing_or_uncertain_information: list[ShortText] = Field(default_factory=list)
    recommended_next_step: Annotated[str, Field(min_length=1, max_length=1000)]
    manual_review_required: bool
    dataset_record_count: int = Field(ge=0)
    error_code: ShortText | None = None

    @field_validator("matching_alerts")
    @classmethod
    def matches_must_be_validated(cls, matches: list[MatchedAlert]) -> list[MatchedAlert]:
        if any(item.alert.validation_status != "validated" for item in matches):
            raise ValueError("only validated alert records may be returned as matches")
        return matches

    @model_validator(mode="after")
    def status_matches_evidence(self):
        if self.status == VerificationStatus.ALERT_MATCH and not self.matching_alerts:
            raise ValueError("ALERT_MATCH requires at least one validated alert with evidence")
        if self.status != VerificationStatus.ALERT_MATCH and self.matching_alerts:
            raise ValueError("matching_alerts may only be present for ALERT_MATCH")
        return self
