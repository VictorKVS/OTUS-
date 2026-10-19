"""PART/ASSEMBLY: input guards for the OSINT reference contract."""

import datetime as dt


WEIGHTS = {
    "suspected_restream": 65,
    "suspected_iptv": 50,
    "trademark": 40,
    "suspected_counterfeit": 55,
    "phishing": 90,
    "other": 20,
}


def validate_category(category):
    if category not in WEIGHTS:
        raise ValueError("Unsupported category")
    return category


def validate_title(title):
    value = str(title).strip()[:500]
    if not value:
        raise ValueError("Missing title")
    return value


def parse_observed_at(value):
    observed = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if observed.utcoffset() is None:
        raise ValueError("Timezone required")
    return observed
