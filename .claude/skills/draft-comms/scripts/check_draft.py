#!/usr/bin/env python3
"""Flag mechanical breaks of the Bedford Lane Language & Tone Guide.

Reads a draft from stdin (or a file path argument) and prints one line per
hit. Hits are prompts to look, not verdicts: tone still needs a human read.
"""
import re
import sys

AVOID = {
    r"\bjust shout\b|\bgive me a shout\b|\bgive us a shout\b": 'the "shout" family; use "As always, reach out if anything\'s unclear"',
    r"\bhappy to\b": '"happy to" is stock filler; say what you\'ll do',
    r"\bfeel free to\b": '"feel free to" is stock filler; ask directly',
    r"\bI wanted to reach out\b": "agency-formal; get straight to the point",
    r"\bplease don'?t hesitate\b": "agency-formal; get straight to the point",
    r"\brest assured\b": "agency-formal; confidence comes through tone",
    r"\bdive in\b|\bdiving in\b": "AI tell; get straight to the point",
    r"\ball good on our end\b": "reads as AI; say plainly what's happening",
    r"\brather than hold(ing)? things up\b": "reads as AI; say plainly what's happening",
    r"\brather than\b[^.?!]*,\s*we'?ll\b": '"Rather than X, we\'ll Y"; just say Y',
    r"\bjust following up\b|\bjust checking in\b": "undermines the ask; lead with what's new or the date",
    r"\bsorry to bother\b": "undermines the ask; lead with what's new or the date",
    r"\b(the )?project is on track\b": "declared confidence; show it through tone",
    r"\ball (of )?the feedback\b": 'over-claim; try "the latest round of feedback"',
}

SIGN_OFF = r"^\s*(best wishes|best|kind regards|regards|warm regards|cheers|thanks|many thanks),?\s*\n\s*(kendall|k)\s*$"

HYPHEN_OK = {"pre-order", "pre-orders", "e-commerce", "check-in", "follow-up", "sign-off", "sign-offs", "re-run"}

VAGUE_DATES = r"\b(later this week|early next week|sometime next week|soon|shortly|in the coming days|ASAP)\b"

US_SPELLINGS = {
    r"\b(organiz|prioritiz|finaliz|realiz|recogniz|customiz|optimiz|utiliz|summariz|categoriz|apologiz|authoriz)(e|es|ed|ing|ation|ations)\b": "-ize; use -ise",
    r"\b(colou?r)\b": None,  # handled below so "Color" can be flagged with a Shopify caveat
    r"\b(favor|honor|behavior|labor|flavor|neighbor)(s|ed|ing|ite|ites)?\b": "-or; use -our",
    r"\b(center|theater)(s|ed)?\b": "-er; use -re",
    r"\bcatalog(s)?\b": "use catalogue",
    r"\banalyz(e|es|ed|ing)\b": "use analyse",
    r"\benroll(ment)?\b": "use enrol/enrolment",
}


def main() -> int:
    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    hits = []

    def add(kind, match_text, note):
        hits.append(f"[{kind}] {match_text!r}: {note}")

    for m in re.finditer("—", text):
        line = text[: m.start()].count("\n") + 1
        add("em-dash", text.splitlines()[line - 1].strip()[:60], f"line {line}; use a full stop, comma, or restructure")

    for pattern, note in AVOID.items():
        for m in re.finditer(pattern, text, re.IGNORECASE):
            add("avoid", m.group(0), note)

    m = re.search(SIGN_OFF, text, re.IGNORECASE | re.MULTILINE)
    if m:
        add("sign-off", m.group(0).strip().replace("\n", " / "), "Gmail adds the signature; end on a warm line instead")

    for m in re.finditer(VAGUE_DATES, text, re.IGNORECASE):
        add("vague date", m.group(0), "if this gates work, use EOD [day] [date]")

    for pattern, note in US_SPELLINGS.items():
        for m in re.finditer(pattern, text, re.IGNORECASE):
            if note is None:
                if m.group(0).lower() == "color":
                    add("spelling", m.group(0), 'use "colour", unless it\'s an exact Shopify field name like "Background Color"')
                continue
            add("spelling", m.group(0), note)

    for m in re.finditer(r"(?<![\w/@.-])[A-Za-z]+(?:-[A-Za-z]+)+(?![\w/@-])", text):
        if m.group(0).lower() not in HYPHEN_OK:
            add("hyphen?", m.group(0), "stacked hyphenated modifier? fine for real product terms (pre-order)")

    bangs = text.count("!")
    if bangs > 2:
        add("exclamations", f"{bangs} found", "aim for about one in email (Slack can run warmer)")

    for m in re.finditer(r"\b[A-Z]{3,}(?:\s+[A-Z]{3,}){2,}\b", text):
        add("caps", m.group(0), "ALL-CAPS for one word, not a sentence")

    if hits:
        print("\n".join(hits))
        print(f"\n{len(hits)} thing(s) to look at.")
    else:
        print("No mechanical issues found. Still read it against the checklist.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
