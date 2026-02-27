"""Example usage of the meeting recap generator."""

from meeting_recap import classify_meeting, generate_recap

# ──────────────────────────────────────────────
# Example 1: Sales call with Centene
# ──────────────────────────────────────────────
sales_attendees = [
    "Sarah Chen <sarah@anyreach.com>",
    "Mike Rodriguez <mike@anyreach.com>",
    "Jennifer Walsh <jwalsh@centene.com>",
    "Tom Baker <tbaker@centene.com>",
]

# Classify first to see what template will be used
classification = classify_meeting(
    sales_attendees,
    internal_domains={"anyreach.com"},
)
print(f"Meeting type: {classification.meeting_type.value}")
print(f"Reason: {classification.reason}")
# -> Meeting type: sales
# -> Reason: External domains detected: centene.com

# Generate the recap (requires ANTHROPIC_API_KEY env var)
# result = generate_recap(
#     transcript=open("centene_call_transcript.txt").read(),
#     attendees=sales_attendees,
#     date="2026-02-27",
#     company_name="Centene",
#     custom_context="$2.3M ARR opportunity, focus on compliance requirements",
#     internal_domains={"anyreach.com"},
# )
# print(result["recap"])


# ──────────────────────────────────────────────
# Example 2: BPO partner call (auto-detected as sales)
# ──────────────────────────────────────────────
partner_attendees = [
    "Sarah Chen <sarah@anyreach.com>",
    "Raj Patel <raj@startek.com>",
]

classification = classify_meeting(
    partner_attendees,
    internal_domains={"anyreach.com"},
)
print(f"\nMeeting type: {classification.meeting_type.value}")
print(f"Reason: {classification.reason}")
# -> Meeting type: sales
# -> Reason: Partner domains detected: startek.com


# ──────────────────────────────────────────────
# Example 3: Internal team meeting
# ──────────────────────────────────────────────
internal_attendees = [
    "Sarah Chen <sarah@anyreach.com>",
    "Mike Rodriguez <mike@anyreach.com>",
    "Lisa Park <lisa@anyreach.com>",
]

classification = classify_meeting(
    internal_attendees,
    internal_domains={"anyreach.com"},
)
print(f"\nMeeting type: {classification.meeting_type.value}")
print(f"Reason: {classification.reason}")
# -> Meeting type: internal
# -> Reason: All attendees are from internal domains
