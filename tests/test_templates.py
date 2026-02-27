"""Tests for prompt template rendering."""

from meeting_recap.classifier import ClassificationResult, MeetingType
from meeting_recap.recap import build_prompt


def test_sales_prompt_renders():
    classification = ClassificationResult(
        meeting_type=MeetingType.SALES,
        reason="External domains detected",
        internal_domains={"anyreach.com"},
        external_domains={"centene.com"},
    )
    prompt = build_prompt(
        transcript="Hello, let's discuss pricing.",
        attendees=["Alice <alice@anyreach.com>", "Bob <bob@centene.com>"],
        date="2026-02-27",
        classification=classification,
        company_name="Centene",
    )
    assert "Centene" in prompt
    assert "Hello, let's discuss pricing." in prompt
    assert "Subject line" in prompt
    assert "Action Items" in prompt


def test_internal_prompt_renders():
    classification = ClassificationResult(
        meeting_type=MeetingType.INTERNAL,
        reason="All internal",
        internal_domains={"anyreach.com"},
        external_domains=set(),
    )
    prompt = build_prompt(
        transcript="Sprint retro discussion.",
        attendees=["Alice <alice@anyreach.com>", "Bob <bob@anyreach.com>"],
        date="2026-02-27",
        classification=classification,
    )
    assert "Sprint retro discussion." in prompt
    assert "TLDR" in prompt
    assert "Parking Lot" in prompt


def test_custom_context_injected():
    classification = ClassificationResult(
        meeting_type=MeetingType.SALES,
        reason="External",
        internal_domains={"anyreach.com"},
        external_domains={"centene.com"},
    )
    prompt = build_prompt(
        transcript="Discussion about compliance.",
        attendees=["Alice <alice@anyreach.com>"],
        date="2026-02-27",
        classification=classification,
        company_name="Centene",
        custom_context="$2.3M ARR opportunity, focus on compliance requirements",
    )
    assert "$2.3M ARR" in prompt
    assert "compliance requirements" in prompt


def test_no_custom_context():
    classification = ClassificationResult(
        meeting_type=MeetingType.INTERNAL,
        reason="All internal",
        internal_domains={"anyreach.com"},
        external_domains=set(),
    )
    prompt = build_prompt(
        transcript="Standup notes.",
        attendees=["Alice <alice@anyreach.com>"],
        date="2026-02-27",
        classification=classification,
    )
    assert "Additional context" not in prompt
