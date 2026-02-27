"""CLI entry point for meeting recap generation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from meeting_recap.recap import generate_recap


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Generate a meeting recap from a transcript using Claude."
    )
    parser.add_argument(
        "transcript",
        type=Path,
        help="Path to the transcript file (plain text).",
    )
    parser.add_argument(
        "--attendees",
        nargs="+",
        required=True,
        help='Attendee names/emails, e.g. "Alice <alice@acme.com>" "Bob <bob@partner.com>"',
    )
    parser.add_argument(
        "--date",
        required=True,
        help="Meeting date (e.g. 2026-02-27).",
    )
    parser.add_argument(
        "--company",
        default=None,
        help="Company name for sales recaps.",
    )
    parser.add_argument(
        "--context",
        default=None,
        help="Custom context to inject (e.g. deal notes).",
    )
    parser.add_argument(
        "--internal-domains",
        nargs="*",
        default=None,
        help="Your company email domains for classification.",
    )
    parser.add_argument(
        "--partner-domains",
        nargs="*",
        default=None,
        help="Additional partner domains to treat as external.",
    )
    parser.add_argument(
        "--model",
        default="claude-sonnet-4-20250514",
        help="Claude model ID to use.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output as JSON instead of plain text.",
    )

    args = parser.parse_args(argv)

    transcript_path: Path = args.transcript
    if not transcript_path.is_file():
        print(f"Error: transcript file not found: {transcript_path}", file=sys.stderr)
        sys.exit(1)

    transcript = transcript_path.read_text()

    internal = set(args.internal_domains) if args.internal_domains else None
    partner = set(args.partner_domains) if args.partner_domains else None

    result = generate_recap(
        transcript=transcript,
        attendees=args.attendees,
        date=args.date,
        company_name=args.company,
        custom_context=args.context,
        internal_domains=internal,
        partner_domains=partner,
        model=args.model,
    )

    if args.json_output:
        print(json.dumps(result, indent=2))
    else:
        print(f"[{result['meeting_type'].upper()} MEETING] {result['classification_reason']}\n")
        print(result["recap"])


if __name__ == "__main__":
    main()
