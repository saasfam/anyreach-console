"""Classify meetings as sales/external or internal based on attendee domains."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum


class MeetingType(Enum):
    SALES = "sales"
    INTERNAL = "internal"


# Known BPO / partner domains that should be treated as sales-type meetings
PARTNER_DOMAINS: set[str] = {
    "startek.com",
    "cp360.com",
}


@dataclass(frozen=True)
class ClassificationResult:
    meeting_type: MeetingType
    reason: str
    internal_domains: set[str]
    external_domains: set[str]


def extract_domains(attendees: list[str]) -> set[str]:
    """Extract email domains from a list of attendee names/emails."""
    email_pattern = re.compile(r"[\w.+-]+@([\w-]+\.[\w.-]+)")
    domains: set[str] = set()
    for attendee in attendees:
        match = email_pattern.search(attendee)
        if match:
            domains.add(match.group(1).lower())
    return domains


def classify_meeting(
    attendees: list[str],
    internal_domains: set[str] | None = None,
    partner_domains: set[str] | None = None,
) -> ClassificationResult:
    """Classify a meeting based on attendee email domains.

    Args:
        attendees: List of attendee strings (names, emails, or "Name <email>").
        internal_domains: Set of your company's email domains.
            Falls back to the most common domain among attendees.
        partner_domains: Additional domains to treat as external/sales.
            Merged with the built-in PARTNER_DOMAINS list.

    Returns:
        ClassificationResult with the meeting type and reasoning.
    """
    all_partner = PARTNER_DOMAINS | (partner_domains or set())
    domains = extract_domains(attendees)

    if not domains:
        return ClassificationResult(
            meeting_type=MeetingType.INTERNAL,
            reason="No email domains found; defaulting to internal",
            internal_domains=set(),
            external_domains=set(),
        )

    # Auto-detect internal domain as the most frequent one if not provided
    if internal_domains is None:
        email_pattern = re.compile(r"[\w.+-]+@([\w-]+\.[\w.-]+)")
        domain_counts: dict[str, int] = {}
        for attendee in attendees:
            match = email_pattern.search(attendee)
            if match:
                d = match.group(1).lower()
                domain_counts[d] = domain_counts.get(d, 0) + 1
        if domain_counts:
            most_common = max(domain_counts, key=domain_counts.get)  # type: ignore[arg-type]
            internal_domains = {most_common}
        else:
            internal_domains = set()

    ext_domains = domains - internal_domains
    int_domains = domains & internal_domains
    partner_overlap = ext_domains & all_partner

    if partner_overlap:
        return ClassificationResult(
            meeting_type=MeetingType.SALES,
            reason=f"Partner domains detected: {', '.join(sorted(partner_overlap))}",
            internal_domains=int_domains,
            external_domains=ext_domains,
        )

    if ext_domains:
        return ClassificationResult(
            meeting_type=MeetingType.SALES,
            reason=f"External domains detected: {', '.join(sorted(ext_domains))}",
            internal_domains=int_domains,
            external_domains=ext_domains,
        )

    return ClassificationResult(
        meeting_type=MeetingType.INTERNAL,
        reason="All attendees are from internal domains",
        internal_domains=int_domains,
        external_domains=set(),
    )
