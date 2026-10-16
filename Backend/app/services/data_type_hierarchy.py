"""Canonical parent relationships for normalized data-type codes."""

DATA_TYPE_ALIASES: dict[str, str] = {
    "PRECISE_LOCATION": "DATA.LOCATION.PRECISE",
    "LOCATION.PRECISE": "DATA.LOCATION.PRECISE",
    "APPROXIMATE_LOCATION": "DATA.LOCATION.APPROXIMATE",
    "LOCATION.APPROXIMATE": "DATA.LOCATION.APPROXIMATE",
    "LOCATION": "DATA.LOCATION",
    "CONTACTS": "DATA.CONTACTS",
    "DEVICE": "DATA.DEVICE",
    "ACCOUNT": "DATA.ACCOUNT",
    "FINANCIAL": "DATA.FINANCIAL",
    "HEALTH": "DATA.HEALTH",
    "MEDIA": "DATA.MEDIA",
    "USAGE": "DATA.USAGE",
    "OTHER": "DATA.OTHER",
}

DATA_TYPE_PREFIX_ALIASES: dict[str, str] = {
    "DATA.COM.": "DATA.COMM.",
}

DATA_TYPE_PARENTS: dict[str, str] = {
    "DATA.LOCATION": "DATA",
    "DATA.LOCATION.PRECISE": "DATA.LOCATION",
    "DATA.LOCATION.APPROXIMATE": "DATA.LOCATION",
    "DATA.CONTACT": "DATA",
    "DATA.CONTACT.EMAIL": "DATA.CONTACT",
    "DATA.CONTACT.ADDRESS": "DATA.CONTACT",
    "DATA.CONTACT.PHONE_EMAIL": "DATA.CONTACT",
    "DATA.CONTACT.EMAIL_PHONE_USERNAME": "DATA.CONTACT",
    "DATA.CONTACT.PHONE": "DATA.CONTACT",
    "DATA.CONTACTS": "DATA",
    "DATA.CONTACTS.LIST": "DATA.CONTACTS",
    "DATA.DEVICE": "DATA",
    "DATA.DEVICE.ID": "DATA.DEVICE",
    "DATA.DEVICE.SMART_HOME": "DATA.DEVICE",
    "DATA.DEVICE.STORAGE": "DATA.DEVICE",
    "DATA.DEVICE.SENSOR": "DATA.DEVICE",
    "DATA.ACCOUNT": "DATA",
    "DATA.ACCOUNT.GOOGLE": "DATA.ACCOUNT",
    "DATA.ACCOUNT.USER_ID": "DATA.ACCOUNT",
    "DATA.ACCOUNT.PERSONAL_INFO": "DATA.ACCOUNT",
    "DATA.AUTH": "DATA",
    "DATA.AUTH.SECRET_KEY": "DATA.AUTH",
    "DATA.COMM": "DATA",
    "DATA.COMM.MESSAGE_CONTENT": "DATA.COMM",
    "DATA.FINANCIAL": "DATA",
    "DATA.FINANCIAL.PAYMENT": "DATA.FINANCIAL",
    "DATA.FINANCIAL.TRANSACTION": "DATA.FINANCIAL",
    "DATA.GAMING": "DATA",
    "DATA.GAMING.GAMEPLAY": "DATA.GAMING",
    "DATA.HEALTH": "DATA",
    "DATA.HEALTH.ACTIVITY": "DATA.HEALTH",
    "DATA.HEALTH.APPOINTMENT": "DATA.HEALTH",
    "DATA.HEALTH.HEART_RATE": "DATA.HEALTH",
    "DATA.HEALTH.PROVIDER_PREFERENCES": "DATA.HEALTH",
    "DATA.HEALTH.RECORD": "DATA.HEALTH",
    "DATA.HEALTH.PERSONAL_HEALTH": "DATA.HEALTH",
    "DATA.HEALTH.VITALS": "DATA.HEALTH",
    "DATA.MEDIA": "DATA",
    "DATA.MEDIA.CAMERA": "DATA.MEDIA",
    "DATA.MEDIA.MICROPHONE": "DATA.MEDIA",
    "DATA.MEDIA.PHOTO": "DATA.MEDIA",
    "DATA.MEDIA.VIDEO": "DATA.MEDIA",
    "DATA.MEDIA.PHOTOS_VIDEOS": "DATA.MEDIA",
    "DATA.MEDIA.AUDIO_VIDEO": "DATA.MEDIA",
    "DATA.FILE": "DATA",
    "DATA.FILE.USER_FILES": "DATA.FILE",
    "DATA.USAGE": "DATA",
    "DATA.USAGE.ACTIVITY_HISTORY": "DATA.USAGE",
    "DATA.USAGE.ASSIGNMENT_CONTENT": "DATA.USAGE",
    "DATA.USAGE.CART_ACTIVITY": "DATA.USAGE",
    "DATA.USAGE.COMMENT_CONTENT": "DATA.USAGE",
    "DATA.USAGE.LESSON_ACTIVITY": "DATA.USAGE",
    "DATA.USAGE.PLAYBACK_ACTIVITY": "DATA.USAGE",
    "DATA.USAGE.POST_CONTENT": "DATA.USAGE",
    "DATA.USAGE.PROGRESS_RECORDS": "DATA.USAGE",
    "DATA.USAGE.SEARCH_HISTORY": "DATA.USAGE",
    "DATA.USAGE.WATCH_HISTORY": "DATA.USAGE",
    "DATA.USAGE.ACTIVITY_LOGS": "DATA.USAGE",
    "DATA.USAGE.TRIP_DETAILS": "DATA.USAGE",
    "DATA.OTHER": "DATA",
}


def _is_ancestor(ancestor: str, child: str) -> bool:
    current = DATA_TYPE_PARENTS.get(child)
    while current is not None:
        if current == ancestor:
            return True
        current = DATA_TYPE_PARENTS.get(current)
    return False


def data_type_relation(
    expected_data_type: str,
    evidence_data_type: str | None,
) -> str | None:
    """Return the evidence-to-expectation hierarchy relationship."""
    if not evidence_data_type:
        return None

    expected = canonical_data_type_code(expected_data_type)
    evidence = canonical_data_type_code(evidence_data_type)

    if expected == evidence:
        return "EXACT"
    if _is_ancestor(evidence, expected):
        return "BROADER_EVIDENCE"
    if _is_ancestor(expected, evidence):
        return "NARROWER_EVIDENCE"
    return None


def canonical_data_type_code(data_type: str) -> str:
    code = data_type.strip().upper()
    if code in DATA_TYPE_ALIASES:
        return DATA_TYPE_ALIASES[code]
    for alias_prefix, canonical_prefix in DATA_TYPE_PREFIX_ALIASES.items():
        if code.startswith(alias_prefix):
            return canonical_prefix + code[len(alias_prefix):]
    return code


def is_known_data_type(data_type: str) -> bool:
    code = canonical_data_type_code(data_type)
    known_codes = set(DATA_TYPE_PARENTS) | set(DATA_TYPE_PARENTS.values())
    return code == "DATA" or code in known_codes


def hierarchy_edges() -> tuple[tuple[str, str], ...]:
    """Return (child, parent) edges including taxonomy roots."""
    edges = list(DATA_TYPE_PARENTS.items())
    edges.extend(
        [
            ("DATA", "DataType"),
            ("PersonalData", "DataType"),
        ]
    )
    return tuple(edges)
