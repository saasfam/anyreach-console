"""Prompt templates for meeting recap generation."""

SALES_RECAP_PROMPT = """\
You are summarizing a sales call transcript for all meeting attendees. \
Be concise, professional, and action-oriented.

Meeting context:
- Company: {company_name}
- Attendees: {attendees}
- Date: {date}
{custom_context_block}
Transcript:
{transcript}

Generate a recap email with these sections:

**Subject line**: Brief, specific to what was discussed

**Meeting Summary** (2-3 sentences max — what was this meeting about and what stage are we at)

**Key Discussion Points**
- What the prospect cares about (pain points, priorities, requirements)
- Any objections or concerns raised
- Pricing/commercial topics discussed

**Decisions Made**
- List any commitments or agreements from either side

**Action Items**
- Format: [Owner] — Action — Due date (if mentioned)
- Separate into "Our team" and "Their team" actions

**Next Steps**
- What happens next, including any scheduled follow-ups

Tone: Professional but warm. Do NOT include filler or pleasantries. \
Do NOT editorialize or add information not in the transcript. \
If something is unclear, flag it as "To confirm: ..."
"""

INTERNAL_RECAP_PROMPT = """\
You are summarizing an internal team meeting transcript. Be direct and concise.

Meeting context:
- Attendees: {attendees}
- Date: {date}
{custom_context_block}
Transcript:
{transcript}

Generate a recap with these sections:

**Subject line**: Brief summary of meeting focus

**TLDR** (1-2 sentences)

**Decisions Made**
- Bullet each decision clearly

**Action Items**
- Format: [Owner] — Action — Due date
- If no due date was mentioned, note "TBD"

**Open Questions / Parking Lot**
- Anything unresolved that needs follow-up

**Key Updates Shared**
- Brief bullets on any status updates or new info shared

Skip any section that has nothing to report. No fluff.
"""
