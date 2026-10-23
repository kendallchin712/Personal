# Personal finance workspace — Kendall Chin

Read this first. It lets a fresh session pick up where earlier ones left off.

Kendall is a NZ citizen living in Melbourne, an Australian tax resident, and a
self-employed contractor for Bedford Lane, invoiced through Hnry. Day rate is
**$310/day from 1 Oct 2026** (was $290). Invoice goes out on the 1st, pay lands
around the 10th.

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

1. Run `python3 up-sync.py --json`.
2. Map the Up accounts to the `money-map.html` cards:
   - TRANSACTIONAL account → **Up — Spending**
   - Saver `Essentials` → **Up — Essentials (rent + bills)**
   - Saver `Emergency` → **Up — Emergency fund** (5.35%+ Grow rate saver)
   - Saver `Leave/Time off` → **Up — Leave / Time off** (target $3,100)
   - **Up — Wants** is closed ($0) unless a Wants saver reappears.
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
   - the "as at" date in the masthead **and** the footer
5. Send Kendall the rendered file, then commit and push (see Git below).

## How the money flows

**Rent cycle (normal, don't flag it as a problem):**
- MICM rent of **$5,097** debits from Essentials around the 16th–19th, which
  drains Essentials to near zero.
- Flatmates Mona and Gen each pay ~$1,617.7 (~$3,235 total) around the 17th–20th.
  These **auto-forward into Essentials**. That money is rent, never spending money.
- Kendall's share (~$1,880) tops Essentials back to target from the next pay.
- Low Essentials mid-month is expected. Label it as a post-rent trough.

**Payday (~10th):** the Up auto-split is **not** firing, so Kendall moves money
by hand, in this order:
1. Essentials → back to its target
2. Leave → $1,000 (must hit $3,100 by the Dec 10 pay)
3. Emergency → $325 ("bank the raise": the $290→$310 increase)
4. The rest stays in Spending

From **February**, once the Christmas leave is used, the $1,000 Leave transfer
switches to Emergency.

**Leave rule:** for each unpaid day off, Kendall pays themself the day rate
($310) from the Leave saver into Spending.

**Upcoming leave:** Bedford Lane shutdown 21 Dec 2026 – 3 Jan 2027, plus
18–22 Jan 2027.

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
  income and selling NZ shares), super at 12%, Hnry's pricing change.

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
   `updatedAt` = now (ISO, UTC) and `source` = "Up API". Keep `targets`,
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
