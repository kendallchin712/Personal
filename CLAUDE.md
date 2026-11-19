# Personal finance workspace — Kendall Chin

Read this first. It lets a fresh session pick up where earlier ones left off.

Kendall is a NZ citizen living in Melbourne and an Australian tax resident.
Until 30 Nov 2026: self-employed contractor for Bedford Lane at **$310/day**,
invoiced through Hnry (invoice on the 1st, pay ~10th for the month before).
The last Hnry invoice is 1 Dec (November, 19 days) → pay ~10 Dec.
**From 1 Dec 2026: full-time employee of Bedford Lane, $75,000 + 12% super,
paid fortnightly** (~$2,884.62 gross, ~$2,326 net a fortnight; $288.46 a
weekday). Public holidays, 4 weeks' annual leave and 10 sick days are paid.
Salary is paid fortnightly on a **Tuesday or Wednesday** (exact day to
confirm). The first pay is probably Tue 15 / Wed 16 Dec, then 29/30 Dec,
12/13 Jan, 26/27 Jan, 9/10 Feb and so on. The Morning Brief assumes Tue 15 Dec
(`SALARY_START` in `morning-brief.html`); fix it once a payslip confirms the
date. Still to confirm: whether the Christmas shutdown is paid or leave can be
taken in advance.

Kendall likes direct, blunt, concise answers with real numbers. Use the
family terms Kendall uses: the late grandmother is **"nen"**. Never invent
names for people.

## Files

| File | What it is |
|---|---|
| `money-map.html` | Main dashboard: every account, net worth, safety net, actions. Keep it current. |
| `freedom-number.html` | FIRE tracker: $1.6M target ($65k/yr × 25), scenario table. |
| `fy2526-expense-register.html` | FY25/26 deductions. That year is **filed**, so treat this as history. |
| `up-sync.py` | Pulls live Up balances via the Up API (read-only). |
| `harada-grid.*`, `README.md` | Unrelated to finance. Leave alone. |

All of this is private financial data. Deliver dashboards as files in chat.
Don't publish them anywhere public.

## Up API (`up-sync.py`)

- Reads the token from the `UP_TOKEN` environment variable (a real token is
  ~136 characters). The domain `api.up.com.au` is allowed in the environment's
  network settings.
- **Never print, log, echo or commit the token.** To check it exists, print
  only its length.
- The API is read-only. It can see balances and transactions; it cannot move
  money.

```
python3 up-sync.py --ping     # check the token works
python3 up-sync.py            # readable balances
python3 up-sync.py --json     # machine-readable, use this to update dashboards
python3 up-sync.py --json --tx 30   # plus recent transactions
```

If it reports a 401 or a missing token, the setup checklist it prints says what
to fix. Kendall changes those settings, not you.

## "Refresh my money map": the workflow

0. **Start from the published page, not the repo copy.** Pushes from routine
   sessions sometimes fail, so the published Money Map is the master copy.
   `Artifact` `read` the Money Map URL (no `path`, to count as viewed), then
   read it again with `path: "index.html"` to download it. Save the part
   between `<body>` and `</body>` over `money-map.html`, which starts with
   `<title>Money Map</title>`.
1. Run `python3 up-sync.py --json`.
2. Map the Up accounts to the `money-map.html` cards:
   - TRANSACTIONAL account → **Up — Spending**
   - Saver `Essentials` → **Up — Essentials (rent + bills)**
   - Saver `Emergency` → **Up — Emergency fund** (5.35%+ Grow rate saver)
   - Saver `Leave/Time off` → **Up — Leave / Time off** (summer unpaid days only)
   - Saver `Alice` → **Up — Alice**: friends' transfers forwarded in for a
     group collection. Show it, but leave it **out** of day-to-day and net worth.
   - **Up — Wants** is closed ($0) unless a Wants saver reappears.
   - Up's saver names carry emoji prefixes (e.g. "🚨 Emergency",
     "💰 Essentials", "🏖️ Leave/Time off"), so match by the word the name
     contains, not by exact name.
3. **Non-Up accounts are manual** (no API): BNZ (Fire Extinguisher, BLOW,
   Insurance, Advantage Visa), Wise, Sharesies, KiwiSaver, AustralianSuper.
   Keep their last values unless Kendall supplies new ones. Convert NZD → AUD
   at **~0.80**, the rate the files already use.
4. Recalculate and update:
   - the hero day-to-day figure, composition-bar %, legend and total net worth
     (day-to-day = all Up + Wise + BNZ net of the Visa; long-term = KiwiSaver +
     AustralianSuper + Sharesies)
   - the **Safety net goal**: Up Emergency + BNZ Fire Extinguisher (AUD)
     against **$12,000**
   - the Leave action text, if Leave moved
   - the "as at" date in the masthead **and** the footer, as today's date
     in Melbourne (`TZ=Australia/Melbourne date`)
5. Send Kendall the rendered file, then commit and push (see Git below).

## How the money flows

**Rent cycle (normal, don't flag it as a problem):**
- MICM rent is **$5,214** from Nov 2026 (was $5,097). It comes out around the
  18th–19th and debits **Spending**, so Kendall moves $5,214 Essentials →
  Spending the day before rent. Essentials target: **$5,393** (rent + $179
  buffer). Up's "Cover" is per-transaction (Kendall taps it, or a rule does):
  subscriptions such as Audible are covered from Essentials; everyday spending
  (Uber, shopping) should stay on Spending, not be covered from Essentials.
- Rent split (rent rises are split evenly three ways). From Nov 2026:
  Mona **$1,656.74**, Gen **$1,656.74** (each was $1,617.74), Kendall
  **$1,900.52** (was ~$1,862). Flatmates pay around the 17th–20th.
  These are meant to **auto-forward into Essentials**, but in Nov 2026 they
  landed in Spending (forward didn't fire) and Kendall moved only their own
  $1,900 from Essentials; the result is the same. That money is rent, never
  spending money. Nov: Mona paid $1,654.36 ($2.38 short).
- Kendall's share plus subscriptions tops Essentials back to target from the
  next pay.
- Low Essentials mid-month is expected. Label it as a post-rent trough.

**Dec 10 (last Hnry pay):** Essentials → $5,393; **$1,000 → Leave**; ~A$700 →
BLOW via Wise; Emergency paused; the rest stays in Spending. The 9 Nov leave
draw ($310) and the $10 left over from the October sick day ($300 drawn on
6 Nov) were taken early, on 18 Nov, so there's no Leave draw on Dec 10.

**Every fortnightly salary pay** (moved by hand; the Up auto-split isn't firing):
1. **$951 → Essentials** (rent share $1,900.52 + ~$160 bills a month)
2. **$600 → Emergency** until the safety net reaches $12k, then the same into
   a Sharesies broad index fund
3. The rest (~$775) stays in Spending

There are no Jan 10 / Feb 10 contractor pays any more. Summer salary pays are
light by the unpaid days: top each one up from Leave by **$288.46 per unpaid
day** on the payslip (public holidays are paid). Leave holds ~$3,430 after
Dec 10 and the 9 Nov draw: enough for ~11.9 unpaid days. Whatever is left
after January goes to Emergency. Kendall is in NZ from 21 Dec to end of
January with family covering food and board, so Spending builds a surplus.

**Leave rule:** for each unpaid day off, Kendall moves the day rate from Leave
into Spending: $310 for contractor days (to 30 Nov), $288.46 for employee days.
Once this summer is covered the Leave saver retires (annual leave is paid).

**Upcoming leave (15 unpaid days, $4,650 at $310):** 1 sick day in October,
Mon 9 Nov, Bedford Lane shutdown Mon 21 Dec 2026 – Fri 1 Jan 2027 (7 days;
25 Dec, 28 Dec, 1 Jan are public holidays), plus Kendall's own leave Mon 18 –
Tue 26 Jan 2027 (6 days; 26 Jan is Australia Day). Kendall works remotely from
NZ on the other days and is back at work Wed 27 Jan.

**Trips (all flights paid; check Gmail/Calendar before asking about travel):**
- Auckland Sat 7 – Sun 15 Nov 2026 (Jetstar ELV8JP). Family covers costs.
- NZ for Christmas from Mon 21 Dec (Air NZ NZ126, one-way). The return at the
  end of January isn't booked; NZ money (BLOW) pays for it and NZ extras, so
  top BLOW up ~A$700 via Wise from the Dec 10 pay. Mum and grandma cover food
  and accommodation (Auckland, a week in Wanaka with mum).
- NZ Wed 24 Feb – Tue 16 Mar 2027 (Jetstar UMPJTC; Auckland→Dunedin 7–16 Mar,
  ZS1IXD). Not yet known whether those days are unpaid.

**Public holidays:** unpaid as a contractor (e.g. Melbourne Cup, 3 Nov 2026),
paid as an employee from 1 Dec. November has 19 billable days, so the Dec 10
pay is ~$5,890 gross (~$4,450–4,520 net). December is the tightest month: it
carries Christmas in NZ.

## Goals and standing decisions

- **Safety net $12k** (~4 months of essentials) = Up Emergency (instant) + BNZ
  Fire Extinguisher (nen's money via mum, NZ$6.6k, ~2 days to move via Wise).
  The Fire Extinguisher money stays **liquid**. Kendall decided against a
  term deposit for it.
- **FIRE:** $1.6M. Once the safety net is full, new investing goes into a
  broad, low-cost global index fund in Sharesies (the money reachable before
  60). Don't add to the single stocks.
- **BNZ Advantage Visa:** only NZD bills on it (Spotify, which can't move).
  Clear it in full every month (20.95% interest).
- **Work expenses** go on the **Hnry Business Mastercard** so they're captured
  as deductions (e.g. Notion). A FY26/27 expense register doesn't exist yet;
  offer to start one.
- **Open questions for Hnry:** temporary-resident status (affects tax on NZ
  income and selling NZ shares), Hnry's pricing change.
- **Super is settled:** Bedford Lane pays 12% Super Guarantee: on each invoice
  until Nov 2026, then on salary ($9,000/yr, ~$346 a fortnight).
- **Hnry ends** after the final November invoice. Tax for FY26/27 mixes 5
  months of contractor income (Hnry over-withheld before, so expect a refund)
  with PAYG salary.

## Published pages (private claude.ai artifacts)

| Page | URL | Source |
|---|---|---|
| Morning Brief (Kendall's home-screen shortcut) | https://claude.ai/artifact/My49XxZ7KpEhg2DTFPTCfp | `morning-brief.html` |
| Money Map | https://claude.ai/artifact/VAswwoejCVfqkUyJ7ExEKv | `money-map.html` |
| Freedom Number | https://claude.ai/artifact/A7w6wcpXg4qj3zrGADrcMD | `freedom-number.html` |
| Sleep & recovery (Oura, live) | https://claude.ai/artifact/J1b43eNcogcDQj9eTn4vRZ | not in repo |

- **Morning Brief** reads Oura **live** through the connector, so it needs no
  daily update for Oura. Its Up balances come from one document in its data
  store: collection `brief`, doc `up`, with this shape:
  `{updatedAt, source, accounts:{spending, essentials, emergency, leave},
  targets:{essentials, leave, safetyNet}, manual:{fireExtinguisherAUD},
  links:{moneyMap, freedomNumber, sleepRecovery}}`.
- **Sleep & recovery** is also live. Never republish it from a routine.
- To update a page from a new session, `Artifact` `read` its URL first, then
  publish the repo file with `url` set to that URL, so the link stays the same.

## Daily 8am routine

A scheduled routine runs this every morning at 8am Melbourne time:

1. Clone `kendallchin712/Personal` if it isn't already there, check out
   `claude/personal-finances-q02plj`, and `git pull`.
2. Check `UP_TOKEN` is set (print only its length) and run
   `python3 up-sync.py --json`. If it fails, stop here. Don't write
   guessed numbers anywhere; say what failed.
3. **Morning Brief data:** `ArtifactData` `get` collection `brief`, doc `up`
   on the Morning Brief URL. Then `set` it with `if_version` set to the
   version you just read. Write fresh `accounts` (Spending = the TRANSACTIONAL
   account; Essentials, Emergency and `Leave/Time off` savers by name),
   `updatedAt` = the output of `date -u +%Y-%m-%dT%H:%M:%SZ` run at that
   moment (never a remembered or guessed time) and `source` = "Up API". Keep `targets`,
   `manual` and `links` as they were.
4. **Money Map:** run the refresh workflow above (Up cards, hero, net worth,
   safety net, dates). Then `Artifact` `read` the Money Map URL and publish
   `money-map.html` with `url` set to it.
5. Commit with a short message, then push. If the push is refused for lack
   of access, call `add_repo` (owner `kendallchin712`, repo `Personal`,
   access `push`) once and retry. If it still fails, skip the push and say
   so in the summary. The published pages are what Kendall reads, so a
   missed push loses nothing important.
6. Finish with a 2–3 line summary: the balances, anything unusual (e.g.
   Spending under $100, or rent hit but flatmate money hasn't arrived), and
   anything that failed.

Don't touch Freedom Number or Sleep & recovery in the routine.

## Git

- Work on branch `claude/personal-finances-q02plj`. Before committing, run
  `git fetch` and check the branch matches the remote. Container restarts
  have checked out an unrelated history before.
- Never force-push. If histories diverge, stack new work on top of the remote
  branch without rewriting it.
