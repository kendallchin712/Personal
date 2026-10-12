---
name: draft-comms
description: Draft emails, Slack messages, ClickUp comments and tickets, escalations and client docs in Kendall's Bedford Lane voice, following the Language & Tone Guide. Use whenever Kendall asks to draft, write, reply to, rewrite or tone-check any work comms (client email, sign-off chase, access request, UAT handover, Slack update or debrief, ClickUp comment, escalation to Alex or Alice).
---

# Draft comms

Write comms that sound like Kendall wrote them: warm, light and confident, with no corporate gloss. The full guide is in [references/tone-guide.md](references/tone-guide.md). Read it before your first draft in a session; it is the source of truth and wins over anything summarised here.

## Workflow

### 1. Pin down the brief

Work out these four things from the request and any thread or context Kendall shares. Only ask when something that gates the message is missing (a date, a name, a link); otherwise draft with a clear `[placeholder]` and keep going.

- **Audience**: client, client who is stalling or feedback-sensitive, BL team, senior dev or strategist, or Alex/Alice. This sets how much to explain (see "Tone by audience").
- **Channel**: email, Slack, ClickUp comment, ClickUp ticket, or client doc.
- **Shape**: match one of the seven house message shapes if it fits (UAT or process handover, sign-off chase, access request, post-meeting Slack debrief, workshop series, escalation, ClickUp client comment). For email, otherwise pick quick reply (1 to 3 sentences) or structured delivery email.
- **Facts**: names, dates, links, passwords, ClickUp statuses, platform names. Never invent these. Use `[Preview Link]`, `EOD [day] [date]` and so on when they're unknown.

If it's an escalation, first ask yourself whether "can we grab 15 minutes?" would do. If so, say that and offer the one-liner instead (or as well).

### 2. Draft

- Build on the shape's skeleton; the voice rules still win on wording.
- **Opener** by person: **Hey** for most (Tess, Rachel, Lauren, Dom, Issy, Rob, Harro, Geoff), **Hi** for Lillian and Isabelle, **Hey team,** for groups. A second warm beat is fine ("Happy Friday!").
- **Acknowledge the client's note personally first**, even if a teammate already replied.
- Light on the why, exact on dates that gate work: **EOD [day] [date]**.
- Plain cause and effect for anything technical. Short, sequential.
- Draft from the standing positions so nothing contradicts them: we avoid multiple product templates; feedback comes in one batch per round; sign-off is a written gate; publishing is the client's call.
- **Email**: always include a subject line (no em-dash). Never write a sign-off ("Best wishes," is the Gmail auto-signature). End on a warm line: "As always, reach out if anything's unclear" is the default; "Chat soon!", "Have a lovely weekend!", "Thanks!" also work.
- **Slack**: 3 to 5 lines, emoji-friendly, ALL-CAPS for one word and "!!" only for real excitement.
- **ClickUp**: client comments go acknowledge → what was checked → recommendation → hand the decision back with a question. Tickets for senior assignees: the commitment, the gating date, non-inferable context only. QA tickets open with "QA'd by Claude - Kendall".
- **Client docs**: follow the BL formatting guide (`Global Admin/Notion-Formatting-Guide.md`): one H1, H2 for key sections, colour-coded callouts, bold for actions and decisions. Keep Shopify admin field names exactly as shown ("Background Color").

### 3. Check

Run the mechanical check on the draft:

```bash
python3 .claude/skills/draft-comms/scripts/check_draft.py <<'EOF'
<draft text>
EOF
```

It flags em-dashes, Avoid-list phrases, written sign-offs, American spellings, vague dates and exclamation count. Treat hits as prompts, not verdicts: "Color" inside a Shopify field name is correct, and the script can't judge tone. Fix what's real, then walk the "Before you send" checklist yourself:

- [ ] Would anyone know I wrote this?
- [ ] No em-dashes, including the subject line
- [ ] No stacked hyphenated modifiers ("fresh mock-ups")
- [ ] Nothing from the Avoid list, especially the "shout" family
- [ ] About one exclamation mark (email)
- [ ] Any date that gates work reads EOD [day] [date]
- [ ] Client's note acknowledged before the practical content
- [ ] No written sign-off
- [ ] British spelling
- [ ] Cut anything that explains why the news matters
- [ ] Should this be a 15 minute chat instead?

Also cut balanced "Rather than X, we'll Y" constructions, tidy three-item lists added for rhythm, and earnest summary lines. One warm, human beat beats three polished ones.

### 4. Hand it over

- Give the draft ready to paste, in a code block or quote so formatting survives: subject line first for email.
- Below it, at most a couple of short lines: placeholders Kendall needs to fill, and anything you were unsure about (an opener for someone not on the list, a date you guessed the format of).
- Don't explain the tone choices unless asked.
- Don't send, post or create drafts in Gmail, Slack or ClickUp unless Kendall asks. If they do ask and the tool is available, create a draft rather than sending.

## Rewriting or tone-checking

When Kendall pastes their own draft to check or tighten: keep their wording wherever it already works (imperfect beats robotic), fix only what breaks the guide, and list the changes in a line or two. Don't sand it into balance.
