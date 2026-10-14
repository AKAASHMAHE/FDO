"""Cross-application data disclosures expected by the platform baseline."""

from app.services.comparison_service import classify_purposes
from app.services.data_type_hierarchy import canonical_data_type_code

ANCILLARY_DATA_TYPE_PREFIXES = (
    "DATA.DEVICE.ID",
    "DATA.ACCOUNT",
    "DATA.AUTH",
)

ANCILLARY_PURPOSE_CATEGORIES = frozenset(
    {"SECURITY", "SERVICE_OPERATION"}
)


def is_ancillary_declaration(
    data_type: str | None,
    purpose: str | None,
) -> bool:
    if not data_type:
        return False

    canonical_type = canonical_data_type_code(data_type)
    has_ancillary_type = any(
        canonical_type == prefix
        or canonical_type.startswith(f"{prefix}.")
        for prefix in ANCILLARY_DATA_TYPE_PREFIXES
    )
    if not has_ancillary_type:
        return False

    return bool(
        ANCILLARY_PURPOSE_CATEGORIES.intersection(
            classify_purposes(purpose)
        )
    )
