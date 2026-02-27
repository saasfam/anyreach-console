"""Core recap generation logic using Claude."""

from __future__ import annotations

import anthropic

from meeting_recap.classifier import ClassificationResult, MeetingType, classify_meeting
from meeting_recap.templates import INTERNAL_RECAP_PROMPT, SALES_RECAP_PROMPT


def _build_custom_context_block(custom_context: str | None) -> str:
    if not custom_context:
        return ""
    return f"\nAdditional context:\n{custom_context}\n"


def build_prompt(
    transcript: str,
    attendees: list[str],
    date: str,
    classification: ClassificationResult,
    company_name: str | None = None,
    custom_context: str | None = None,
) -> str:
    """Build the full prompt from a template and meeting metadata."""
    context_block = _build_custom_context_block(custom_context)
    attendees_str = ", ".join(attendees)

    if classification.meeting_type == MeetingType.SALES:
        return SALES_RECAP_PROMPT.format(
            company_name=company_name or "Unknown",
            attendees=attendees_str,
            date=date,
            transcript=transcript,
            custom_context_block=context_block,
        )

    return INTERNAL_RECAP_PROMPT.format(
        attendees=attendees_str,
        date=date,
        transcript=transcript,
        custom_context_block=context_block,
    )


def generate_recap(
    transcript: str,
    attendees: list[str],
    date: str,
    company_name: str | None = None,
    custom_context: str | None = None,
    internal_domains: set[str] | None = None,
    partner_domains: set[str] | None = None,
    model: str = "claude-sonnet-4-20250514",
) -> dict[str, str]:
    """Generate a meeting recap from a transcript.

    Args:
        transcript: The full meeting transcript text.
        attendees: List of attendee strings (names, emails, or "Name <email>").
        date: Meeting date string.
        company_name: Company name for sales recaps (auto-derived if omitted).
        custom_context: Optional deal/meeting-specific notes to inject
            (e.g., "This is a $2.3M ARR opportunity with Centene").
        internal_domains: Your company's email domains for classification.
        partner_domains: Additional partner domains to treat as external.
        model: Claude model to use.

    Returns:
        Dict with keys: "meeting_type", "classification_reason", "recap".
    """
    classification = classify_meeting(
        attendees,
        internal_domains=internal_domains,
        partner_domains=partner_domains,
    )

    prompt = build_prompt(
        transcript=transcript,
        attendees=attendees,
        date=date,
        classification=classification,
        company_name=company_name,
        custom_context=custom_context,
    )

    client = anthropic.Anthropic()
    message = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    recap_text = message.content[0].text

    return {
        "meeting_type": classification.meeting_type.value,
        "classification_reason": classification.reason,
        "recap": recap_text,
    }
