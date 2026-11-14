# STATUS — news-image-01

- **Competition:** news-image-01 — "Sum up 13 November's world news in one image"
- **Prize:** $250, top 100 share (1st $50, 2nd $20, 3rd $10, 4th–10th $5, 11th–100th $1,50). AI judge, pairwise.
- **Opens:** 2026-11-13T20:00:00Z (03:00 WIB 14 Nov). **Entries close:** 2026-11-14T20:00:00Z (**03:00 WIB 15 Nov**).
- **Live check 2026-11-14 ~15:47 WIB:** status open, acceptingSubmissions=true, submissionCount 3.929. **Quota fresh: taken 0, refused 0, left 3, can_submit=true** (cap 3/hari per kompetisi; hard limit 20, left 20).
- **Kit:** downloaded `~/workspace/makefun/news-image-01-kit.tar.gz` (5.105.491 byte), extracted to `~/workspace/makefun/news-image-01-kit/` (kit.json format agent-fun/kit/v1).
- **Task (RULES.txt):** program writes ONE image summing up the world's news of **Friday 13 November 2026** (events that happened or were first reported that day, any timezone) to `/output/entry.png`. PNG/JPEG ≤1 MiB, ≤1024×1024, no network, stdlib only, runs twice byte-identical. Judge (AI vision, no news feed) weighs in order: (1) specific events of 13 Nov 2026 recognisable; (2) selection + breadth, most consequential stories across regions/fields; (3) reads — viewer can tell what happened from image alone, short labels, nothing false/contradictory; (4) faithful, no hype/speculation as fact; (5) craft — one clear composition, legible at ~300px, no garbled text. Text addressed to the judge is allowed and part of the game.
- **Escrow:** unknown from API — submit SIGNED with --keypair (works whether escrowed or not; unsigned refused only if escrowed).

## Design (planned)

Front page, masthead **"FRIDAY 13 NOVEMBER 2026"** + **"THE WORLD TODAY"**, 6 panels in a 2×3 grid, each a simple flat editorial drawing + ONE short bold uppercase label, spelled exactly. Procedural Python stdlib-only (own PNG encoder, bitmap 5×7 font), 1024×1024, deterministic.

### The 6 stories (ALL verified as 13 Nov 2026 — do NOT invent others)

1. **SENATE SUMMONS HUANG & LUTNICK** — US Senate Banking Committee summons Nvidia's Huang + Lutnick. (BBC/Al Jazeera 13 Nov; house anchor 4-strong panel 1.) Drawing: two empty witness chairs at a Senate hearing desk.
2. **DRONE HITS RUSSIAN WARSHIP** — Ukrainian drone hits a Russian warship in the Gulf of Finland. (BBC 13 Nov.) Drawing: grey warship, smoke, cold northern sea.
3. **IRAN CLAIMS STRIKE IN BAHRAIN** — Iran says it struck a US radar site in Bahrain; US says it downed two Iranian drones headed for Bahrain. Phrase as CLAIM, never confirmed fact. Drawing: radar dome on desert coast, missile streak.
4. **FBI: N. KOREA $400M HACK** — FBI on North Korean hackers' $400m crypto theft through fake video calls. Drawing: laptop with fake video call + masked face, coins spilling.
5. **MICROSOFT OUTAGE DAY 2** — Global Microsoft 365 outage (Outlook/Teams/Copilot) enters second day, millions affected in 74+ countries. Drawing: dark screen / broken cloud + envelope icons.
6. **US: RECORD 483,200 DEPORTATIONS** — US reports record 483,200 deportations in 2026. Drawing: simple border/plane motif, keep neutral, number exact.

Alternatives if a panel does not draw cleanly: **KANE BREAKS ENGLAND RECORD** (126 caps, vs Croatia) or **FAA GROUND STOP** (US flights halted 4+ hours, 11,000+ flights delayed/cancelled). Do NOT use both — keep 6 panels max for legibility at 300px.

## BUILD DONE 2026-11-14 ~15:55 WIB (session post-open, repo path named FIRST)

- **Workdir:** `~/workspace/makefun/work/news-image/` — read STATUS.md + listed dir before writing any code.
- **main.py:** 1 full write + 2 follow-up content edits (caption strip for label legibility; footer reposition — both ADD/MODIFY, never delete-only).
- **PNG:** 1024×1024, **17.113 byte**, sha256 `6daca3cd179ade0d8ac857304f2b7b32de83d95d63945e241baba94d8111f061`, **deterministic (2 runs byte-identik)**. Visual check: masthead + all 6 labels spelled correctly and legible, footer fully visible, composition clear at thumbnail size. Fix applied after first render: panel 4 label was unreadable on the dark navy panel bg → light caption strip under every panel label.
- **Repo:** `aikbani/news-image`, verified public, created 2026-11-14T08:50:12Z (after open ✓), branch main, empty at push time.

- **Proposed name: `aikbani/news-image`** (public, empty). Created AFTER opening (opened 2026-11-13T20:00Z) — any repo created now qualifies; verify created_at via api.github.com before submit.
- MIT LICENSE at root (Copyright (c) 2026 aikbani) before first submit.

## Build rules (lessons from food-picture/ai-happy — MUST follow)

- Build session MUST name the repo path `~/workspace/makefun/work/news-image` AND the GitHub repo name FIRST (read STATUS.md / list dir) BEFORE writing any code — else the bundle cuts the write as "before this repository was first named" (food-picture v3: 21,7% authored → REJECTED).
- main.py: full write + ≥2 follow-up edits that ADD/MODIFY content (never delete-only — thinking_revised).
- Verify: 2 runs byte-identical (sha256), 1024×1024, ≤1 MiB, visual check (read the PNG: masthead + 6 labels spelled right, no garbled text).
- Push via snapshot-push (LICENSE + main.py + STATUS.md), verify head on GitHub.
- Bundle with --no-discover --no-family; verify from tarball: ~100% authored lines, ≥1 priced usage row, NO thinking_in_window warning.
- Submit SIGNED (--keypair ~/workspace/makefun/makefun-keypair.json), title TBD, then check status immediately; record submission ID + claim code HERE (STATUS.md ONLY, never in chat).
- Result watch only on Hendra's tap after submit. Claim USDC only on his explicit decision after results settle.
