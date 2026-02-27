"""Tests for the meeting classifier."""

from meeting_recap.classifier import MeetingType, classify_meeting


def test_internal_only():
    attendees = [
        "Alice <alice@anyreach.com>",
        "Bob <bob@anyreach.com>",
    ]
    result = classify_meeting(attendees, internal_domains={"anyreach.com"})
    assert result.meeting_type == MeetingType.INTERNAL
    assert result.external_domains == set()


def test_external_attendee_triggers_sales():
    attendees = [
        "Alice <alice@anyreach.com>",
        "Bob <bob@centene.com>",
    ]
    result = classify_meeting(attendees, internal_domains={"anyreach.com"})
    assert result.meeting_type == MeetingType.SALES
    assert "centene.com" in result.external_domains


def test_partner_domain_triggers_sales():
    attendees = [
        "Alice <alice@anyreach.com>",
        "Bob <bob@startek.com>",
    ]
    result = classify_meeting(attendees, internal_domains={"anyreach.com"})
    assert result.meeting_type == MeetingType.SALES
    assert "startek.com" in result.external_domains
    assert "Partner" in result.reason


def test_custom_partner_domain():
    attendees = [
        "Alice <alice@anyreach.com>",
        "Bob <bob@newpartner.io>",
    ]
    result = classify_meeting(
        attendees,
        internal_domains={"anyreach.com"},
        partner_domains={"newpartner.io"},
    )
    assert result.meeting_type == MeetingType.SALES
    assert "Partner" in result.reason


def test_auto_detect_internal_domain():
    """When no internal_domains provided, most common domain is assumed internal."""
    attendees = [
        "Alice <alice@anyreach.com>",
        "Bob <bob@anyreach.com>",
        "Charlie <charlie@anyreach.com>",
        "Dave <dave@external.com>",
    ]
    result = classify_meeting(attendees)
    assert result.meeting_type == MeetingType.SALES
    assert "anyreach.com" in result.internal_domains
    assert "external.com" in result.external_domains


def test_no_emails_defaults_to_internal():
    attendees = ["Alice", "Bob"]
    result = classify_meeting(attendees)
    assert result.meeting_type == MeetingType.INTERNAL
    assert "defaulting" in result.reason.lower()


def test_cp360_partner():
    attendees = [
        "Alice <alice@anyreach.com>",
        "Bob <bob@cp360.com>",
    ]
    result = classify_meeting(attendees, internal_domains={"anyreach.com"})
    assert result.meeting_type == MeetingType.SALES
    assert "Partner" in result.reason
