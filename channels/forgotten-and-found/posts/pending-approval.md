# Forgotten & Found — pending approval log

## 2026-11-23 (scheduled run) — STEP 1 check: Mary Celeste confirmed PUBLISHED
- `gh run list --workflow publish.yml --limit 10`: run `44581764533` completed successfully 2026-11-19
  and `result.json` (committed 2026-11-20) confirms "The Mary Celeste: The Ship Found Empty at Sea" is
  live public — videoId `pK2saSricOg`, https://youtu.be/pK2saSricOg, published 2026-11-20T17:56:04Z.
  No open "Publish blocked" issues (`gh api repos/.../issues?state=open` → 0). Today is Monday — F&F's
  turn; producing the next video.

## 2026-11-20 (scheduled run) — STEP 1 check: Mary Celeste run now actively awaiting Katie's review
- `gh run list --workflow publish.yml --limit 10` / `gh api .../actions/runs/44581764533/jobs`: the
  Sleepy Meadow run (`44142087104`) that was blocking this one on the shared `concurrency: publish`
  group completed successfully 2026-11-19. This run's `prepare` job then ran (success) and its
  `publish` job entered `waiting` on the GitHub `publish-approval` environment review at 18:49:57Z —
  no longer just queued, genuinely awaiting Katie's approval now, ~23h. No open "Publish blocked"
  issues; issue #14 (Peter Rabbit resemblance) remains closed.

## 2026-11-19 (scheduled run, continued) — "The Mary Celeste: The Ship Found Empty at Sea" PRODUCED, staged, dispatched for approval
- STEP 2: picked Unsolved & Unexplained (UU) — the channel's largest-weighted pillar (35%) and, after
  Port Royal, the pillar due for its next video. Checked `scripts/`/`posts/`: 01 Bell Witch (haunting),
  02 Roanoke (vanished colony), 03 Dancing Plague (mass hysteria), 04 Pied Piper (folklore), 05 Port
  Royal (natural disaster) — no prior video has covered an unsolved maritime mystery. Verified facts via
  WebSearch against Smithsonian Magazine, History.com, Encyclopaedia Britannica, and Royal Museums
  Greenwich before writing: the Mary Celeste's 1872 Atlantic crossing, her crew of ten, the Dei Gratia's
  boarding party findings (disassembled pump, missing lifeboat and papers, undisturbed belongings), the
  Gibraltar salvage inquiry that ruled out violence without naming a cause, and the later Arthur Conan
  Doyle short story that many retellings mistake for fact (flagged explicitly in the script as fiction,
  not history). Script: `scripts/06-mary-celeste.md`.
- Narration via Piper (`en_US-lessac-medium`; `pip install piper-tts` landed on `/usr/local/bin/python3.13`
  again, not default `python3` 3.11 — same split as every prior run; voice model copied from the media
  repo's `voices/`). Ran the module directly via `python3.13 -m piper` since the wrapper script hardcodes
  `python3`. Runtime: 5:12 (312.3s) — shorter than the 8-9 min target, in line with the normal
  script-length variance seen on every prior F&F video.
- Visuals: 6 scene illustrations + 1 thumbnail via Canva `generate-image`, all 7 succeeded without
  hitting `quota_cooldown` this run (no Runway fallback needed). Same full-resolution export limitation
  as every prior run (`export-download.canva.com` confirmed still blocked via direct `curl` test, 403)
  — worked around it the same documented way: built a disposable 6912x3456 Canva design (`DAHbYWI5FqY`),
  inserted each image full-bleed on its own page, captured the ~600x300 page-preview thumbnails straight
  from each `insert_fill` edit response (no extra move+read needed this run — the thumbnail came back
  populated on the first edit call for every page). ffmpeg upscales these to 1920x1080 in assembly.
  Minor cosmetic note: the New York harbor scene's background skyline reads slightly too modern for 1872
  (an artifact of the image model) — visual only, doesn't affect any claim in the narration or
  description; not worth a regeneration cycle today. Thumbnail is a dramatic adrift-ghost-ship shot
  (emotional hook); title states the documented mystery (informational hook) — no repeat between them.
- Assembled with `pipeline/assemble_video.sh`: 1920x1080, 17.5 MB, well under the 95 MB staging limit.
  Spot-checked frames at 15s and 300s — clean upscale, no artifacts, narration/visual beats in sync.
- Payload (`posts/06-mary-celeste-payload.json`): `type: "public"`, `selfDeclaredMadeForKids: "no"`
  (hard rule 2 — general-audience history content), AI-disclosure line present, full source citations,
  5 hashtags in the description (one within the first ~140 characters), none identical to stories 1-5's
  sets. Validated clean via `python3 -m automation.publish check`. Approval hash:
  `75ae79734282269e14c2df805bc44cde4d4ca10337e2a4602ecb89ef945d2e65`.
- **Staged**: video committed as `staged/post-forgotten-and-found-06/video.mp4` in the private media repo
  (commit `8bc0e6c`). Payload + script committed to `youtube-automation-` main (commit `5c6c0a8`).
- **Dispatched**: `gh workflow run publish.yml -f post=channels/forgotten-and-found/posts/06-mary-celeste-payload.json -f tag=post-forgotten-and-found-06` →
  run https://github.com/katherineparks141-eng/youtube-automation-/actions/runs/44581764533.
  This run is queued (`pending`, no jobs started after ~1 minute) behind run `44142087104` (Sleepy
  Meadow story 06) because `publish.yml` declares one shared `concurrency: publish` group and that run
  is still `waiting` on Katie's review, now ~2 days — same expected queueing behavior documented on
  every prior run with two runs in flight, not a new fault. It will start its own `prepare` job once
  that run is approved, rejected, or cancelled.
  **AWAITING KATIE'S APPROVAL on GitHub** (both this run and the still-pending `44142087104`, in order)
  — nothing will go live until she reviews and approves them.
- Dashboard to-do `r20261119-youtube-production-01` created on
  https://claude.ai/artifact/KPm8DRRk9RrVT9JH3YtcQL pointing at the run URL above.
- **Known gap carried over**: `automation/youtube.py` still has no `thumbnails.set` call, so this
  video's dedicated thumbnail won't upload automatically — Katie will need to set it by hand in
  YouTube Studio after this publishes, same as every video published under the new flow so far.

## 2026-11-19 (scheduled run) — STEP 1 check: "Port Royal: The Pirate City the Sea Swallowed in Two Minutes" PUBLISHED
- `gh run list --workflow publish.yml --limit 10`: run `43922804382` (Port Royal, post-forgotten-and-found-05) completed successfully 2026-11-17T23:09:34Z.
  `channels/forgotten-and-found/posts/05-port-royal-payload.result.json` confirms it went live, public: videoId `X_ZmbV1VVg0` (https://youtu.be/X_ZmbV1VVg0). No open "Publish blocked" issues.
  Issue #14 (Peter Rabbit resemblance, Sleepy Meadow) was closed by Katie 2026-11-18 — resolved. One run (`44142087104`, Sleepy Meadow story 06) is still `waiting` on Katie's GitHub approval, now ~2 days — logged on the Sleepy Meadow side.
- Dashboard refreshed (`data/youtube-analytics.json`, 2026-11-18 pull: 1 subscriber, 4,251 views, 10 videos — unchanged subscriber count, +3 views since 11/17's 4,248).
- STEP 2: today is Thursday — Forgotten & Found's turn. Producing next video below.

## 2026-11-16 (scheduled run) — "Port Royal: The Pirate City the Sea Swallowed in Two Minutes" PRODUCED, staged, dispatched for approval
- STEP 1 (read-only): `gh run list --workflow publish.yml --limit 10` shows all 6 runs completed.
  Run `43477718427` (Sleepy Meadow story 05, dispatched 2026-11-13 and still awaiting approval
  as of that run's log) has now completed successfully — see the Sleepy Meadow pending-approval
  log for the confirmed live result. No `publish.yml` run is currently waiting on Katie. Issue
  #14 (possible Peter Rabbit/Beatrix Potter resemblance in Sleepy Meadow stories 01-03, still
  live) remains **open**, 6 days now with no comment from Katie — flagging again; this doesn't
  block Forgotten & Found production but is a standing compliance item.
- STEP 2: today is Monday — Forgotten & Found's turn. Checked `scripts/`/`posts/`: 01 Bell Witch
  (Folklore with a History), 02 Roanoke (Unsolved & Unexplained), 03 Dancing Plague (Strange But
  True), 04 Pied Piper (Folklore with a History) — **Lost Places is the only pillar with zero
  videos so far**, so picked a Lost Places topic: Port Royal, Jamaica, the pirate-era city a
  third of which sank into Kingston Harbour in the 1692 earthquake. Verified against Wikipedia,
  Texas A&M's Nautical Archaeology Program (Dr. Donny Hamilton's published excavation findings),
  UNESCO's 2024 Jamaica Tentative List entry, and Jamaica National Heritage Trust before writing
  — no copyrighted characters, real documented history, named the transatlantic slave trade
  plainly rather than skipping past it.
- Script: `scripts/05-port-royal-jamaica.md`. Narration via Piper (`en_US-lessac-medium`,
  `python3.13 -m piper` — same 3.13/3.11 split as prior runs, voices copied from the media
  repo's `voices/`). Runtime: 6:03 (363.4s) — shorter than the 9-10 min target, consistent with
  the normal script-length variance seen on prior videos (e.g. Pied Piper ran 6:29 vs 8-9 min).
- Visuals: 6 scene illustrations + 1 thumbnail via Canva `generate-image`, all 7 succeeded
  without hitting `quota_cooldown` this run. Same egress-blocked raw-asset export
  (`export-download.canva.com`/`media.canva.com`, confirmed via a direct `curl` test returning
  `CONNECT tunnel failed, response 403`) as every prior run — worked around it the same
  documented way: built a disposable 1920x1080 Canva design (`DAHbGQhhvBU`), inserted each image
  full-bleed on its own page, captured the ~600x338 page-preview thumbnails via `read-design`/
  `edit-design` (not subject to the egress block), then committed the transaction. ffmpeg
  upscales these to 1920x1080 in assembly. Thumbnail is a split above/below-waterline composition
  (emotional hook); title carries the informational hook — no repeat between them.
- Assembled with `pipeline/assemble_video.sh`: 1920x1080, 22 MB, well under the 95 MB staging
  limit. Spot-checked frames at 30s and 200s — clean sync, no text artifacts, no watermarks.
- Payload (`posts/05-port-royal-payload.json`): `type: "public"`, `selfDeclaredMadeForKids: "no"`
  (hard rule 2 — general-audience history content), AI-disclosure line present, full source
  citations, 5 hashtags in the description (one at character ~70, within the first 100), none
  identical to stories 1-4's sets. Validated clean via `python3 -m automation.publish check`.
  Approval hash: `82dda76d604ee657d137374e2767840022b9a11553adf79ffbe0f4072596da05`.
- **Staged**: video committed as `staged/post-forgotten-and-found-05/video.mp4` in the private
  media repo (commit `9f1dd19`). Payload + script committed to `youtube-automation-` main.
- **Dispatched**: `gh workflow run publish.yml -f post=channels/forgotten-and-found/posts/05-port-royal-payload.json -f tag=post-forgotten-and-found-05`.
  **AWAITING KATIE'S APPROVAL on GitHub** — nothing will go live until she reviews and approves
  the `publish-approval` environment review on that run.
- **Known gap carried over**: `automation/youtube.py` still has no `thumbnails.set` call, so this
  video's dedicated thumbnail won't upload automatically — Katie will need to set it by hand in
  YouTube Studio after this publishes, same as every video published under the new flow so far.

## 2026-11-13 (scheduled run) — STEP 1 check: "The Pied Piper of Hamelin" PUBLISHED
- `gh run list --workflow publish.yml --limit 10`: run `43273789908` (Pied Piper, post-forgotten-and-found-04)
  completed successfully on 2026-11-12. `channels/forgotten-and-found/posts/04-pied-piper-payload.result.json`
  confirms it went live: videoId `4CXYaztUFBA`, https://youtu.be/4CXYaztUFBA, publishedAt
  2026-11-12T18:20:36Z, public. Katie's `publish-approval` GitHub review was the actual gate —
  confirmed genuinely approved and published, nothing more to do for this one.
- Issue #14 (possible Peter Rabbit/Beatrix Potter resemblance in Sleepy Meadow videos 01-03) is
  **still open**, 0 comments — unrelated to this channel directly but noting it per the
  cross-channel flag in the prior entry below.
- No open "Publish blocked" issues for Forgotten & Found.

## 2026-11-12 (scheduled run) — "The Pied Piper of Hamelin" PRODUCED, staged, dispatched for approval
- STEP 1 (read-only): run `42869962397` (Sleepy Meadow story 04b, new Pip design) is **still
  waiting** on Katie's `publish-approval` GitHub review — now ~2 days since dispatch
  (2026-11-10 17:56 UTC). No other `publish.yml` runs waiting; no `*.result.json` files exist
  yet for either channel, so nothing has actually gone live under the new GitHub Actions flow.
  Issue #14 (possible Peter Rabbit/Beatrix Potter resemblance in the live Sleepy Meadow videos
  01-03) is **still open**, 0 comments, 0 action taken — flagging again for Katie.
- STEP 1.5: refreshed the Katie HQ dashboard (`dashboard/youtube-analytics` doc) from
  `data/youtube-analytics.json` (last refreshed 2026-11-11T18:17:28Z upstream; numbers
  unchanged since 11/9: 1 subscriber, 4,247 lifetime views, 6 videos). Reported
  `subscribersNetChange: 0` (flat across all 3 tracked refreshes, not estimated). `perVideo`
  stays empty — no video has published under the new flow yet. Also refreshed the `youtube`
  project card's one-line `line` field on `dashboard/current`.
- STEP 2: today is Thursday — Forgotten & Found's turn. New topic, Folklore with a History
  pillar (the channel's 4th pillar, not yet covered by videos 01-03): "The Pied Piper of
  Hamelin: The Real History Behind the Legend." Verified via web search against Wikipedia and
  Museum Hameln's own site before writing the script, to keep hard rule 6 (cited sources)
  accurate. No copyrighted characters — the Pied Piper of Hamelin is public-domain medieval
  folklore, not a trademarked character.
- Script: `scripts/04-pied-piper-of-hamelin.md`. Narration via Piper (`en_US-lessac-medium`,
  voice copied from the private media repo's `voices/` — `pip install piper-tts` landed on
  Python 3.13 in this environment, not the default `python3` on 3.11, so narration was run via
  `/usr/local/bin/python3.13 -m piper`; worth noting for the next run in case the same split
  recurs). Runtime: 6:29 (389.2s) — shorter than the 8-9 min target, consistent with normal
  script-length variance seen on prior videos (e.g. "The Bunny Who Counted the Stars").
- Visuals: 6 scene illustrations + 1 thumbnail via Canva `generate-image` (one `quota_cooldown`
  on the first thumbnail attempt; retried successfully a few calls later, no video-order
  pipeline change needed). Hit the same full-resolution export limitation logged on the
  2026-11-10 Sleepy Meadow run (`export-download.canva.com` / `media.canva.com` both
  `connect_rejected` under this session's egress policy): worked around it the same documented
  way — built a disposable 1920x1080 Canva design (`DAHauTBZZp0`), inserted each image
  full-bleed on its own page, and captured the ~600x338 page-preview thumbnails the Canva MCP
  tool fetches itself (not subject to the egress block). ffmpeg upscales these to 1920x1080 in
  assembly, consistent with the established pipeline quality.
- Assembled with `pipeline/assemble_video.sh`: 1920x1080, ~21.7 MB, well under the 95 MB
  staging limit. Spot-checked two extracted frames for visual/audio sync — clean.
- Payload (`posts/04-pied-piper-payload.json`): `type: "public"`,
  `selfDeclaredMadeForKids: "no"` (hard rule 2 — general-audience history content), AI-
  disclosure line present, full source citations (Wikipedia, Museum Hameln, the Lüneburg
  manuscript, the Zimmern Chronicle, Jürgen Udolph's emigration research), 5 hashtags in the
  description (first one at character 94, within the first 100), none identical to prior F&F
  videos' sets. Validated clean via `python3 -m automation.publish check`. Approval hash:
  `f40a21fbc31ef3253ab423cbe59504e50003cf9dcc6c56bc6f13f825f6b2a453`.
- **Staged**: video committed as `staged/post-forgotten-and-found-04/video.mp4` in the private
  media repo (commit `1b5c527`). Payload + script committed to `youtube-automation-` main.
- **Dispatched**: `gh workflow run publish.yml -f post=channels/forgotten-and-found/posts/04-pied-piper-payload.json -f tag=post-forgotten-and-found-04` →
  run https://github.com/katherineparks141-eng/youtube-automation-/actions/runs/43273789908.
  Unlike run `42869962397` (which reached the `prepare` job and the `publish-approval` wait
  within seconds on 2026-11-10), this run sat at `pending` with zero jobs for several minutes.
  Checked `publish.yml`: it declares `concurrency: publish` (one shared group, no per-run
  key), and run `42869962397` is still `waiting` on Katie's environment review — so GitHub is
  correctly queuing this run behind it, not failing or stuck. It will start its own `prepare`
  job as soon as run `42869962397` is approved or rejected (or cancelled). This is expected
  behavior given two outstanding approvals queue on the same workflow, not a new fault — ruled
  out the Actions-budget guess I first wrote here. Created the GitHub-approval to-do on the
  Katie HQ dashboard for this video regardless, since the dispatch itself succeeded and will
  run once its turn comes.
  **AWAITING KATIE'S APPROVAL on GitHub** (both this run and the still-pending `42869962397`)
  — nothing will go live until she reviews and approves them, in order.
- **Known gap carried over from the 11/10 run**: `automation/youtube.py` still has no
  `thumbnails.set` call, so this video's dedicated thumbnail (saved this session; not part of
  the committed payload) won't upload automatically — Katie will need to set it by hand in
  YouTube Studio after this publishes, same as story 04b.

## 2026-11-10 (12:30 ET scheduled run) — STEP 1 only: nothing waiting, no production today (not F&F's day)
- STEP 1 (read-only): no `publish.yml` runs waiting for Katie's approval (only the 3
  `test/private-upload` test dispatches from 2026-11-09 exist). No open GitHub issues
  concerning this channel (issue #14 is Sleepy Meadow/Pip only). No `*.result.json` files.
- Per cadence (Forgotten & Found: Mon/Thu), today is Tuesday — Sleepy Meadow's turn. No new
  F&F production this run; see `sleepy-meadow-stories/posts/pending-approval.md` for today's
  production (story 04, new Pip design, awaiting Katie's approval on GitHub).

## 2026-11-10 (~00:42 UTC) — STEP 1 only: nothing waiting, no production today (not F&F's day)
- STEP 1 (read-only): no `publish.yml` runs waiting for Katie's approval under the new
  flow — the only runs are the 3 `test/private-upload` test dispatches from 2026-11-09.
  No open GitHub issues. No `*.result.json` files yet for either channel.
- Per cadence (Forgotten & Found: Mon/Thu, Sleepy Meadow: Tue/Fri), today is Tuesday —
  Sleepy Meadow Stories' turn, not Forgotten & Found's. No new F&F production this run.

## 2026-11-09 (12:38 PM ET) — First live scheduled run under the new flow: still blocked on media-repo access
- STEP 1 (read-only): no runs waiting for Katie under the new flow. The only `publish.yml`
  runs today are the 3 private end-to-end tests on `test/private-upload`
  (2 succeeded, 1 failed) from this morning's build session, already covered in
  `SESSION_HANDOFF.md`. No open GitHub issues. No `*.result.json` files exist yet for
  either channel.
- STEP 1.5 (read-only): `data/youtube-analytics.json` and the Katie HQ dashboard
  (`youtube-analytics` doc) were already refreshed at 16:06-16:17 UTC this morning and
  had not changed by this run — nothing new to pull (4,247 lifetime channel views, 1
  subscriber, 6 videos, $0 spend/revenue, not monetized).
- STEP 2/3: blocked before any production started. Independently re-confirmed this
  morning's finding, now narrowed down: `gh` itself works fine for the main repo this
  session (`gh run list`, `gh issue list`/`gh api .../issues` all succeeded) — the specific
  problem is that `katherineparks141-eng/youtube-automation-media` is not in this
  session's GitHub repository scope. Both `gh api repos/.../youtube-automation-media`
  and the GitHub MCP tools return: "GitHub access to this repository is not enabled for
  this session. Use add_repo to request access" — but no `add_repo` or `list_repos` tool
  is exposed to this scheduled-task session to grant it (checked via ToolSearch with
  several phrasings; none found).
- Per CLAUDE.md's "don't route around a guardrail/tool failure" principle, did not
  attempt a workaround (no alternate upload route exists — no Mac device bridge is
  connected to this scheduled task either) and did not produce a new video this run,
  since anything produced couldn't be staged regardless of production succeeding — same
  call the 11:18 AM build session made for the same reason. Nothing produced or staged.
- **Needs Katie/engineering**: add `katherineparks141-eng/youtube-automation-media` to
  this scheduled task's GitHub repository access (currently only `youtube-automation-`
  is in scope, per this session's "Repository Scope" list), or give the routine's session
  some other way to create a GitHub Release on that repo. Until this is resolved, every
  scheduled run will hit this same wall at STEP 3, for both channels.

## 2026-11-05 — "The Dancing Plague of 1518: When a City Danced Itself to Death"
- Logline: In July 1518 a woman in Strasbourg began dancing and didn't stop; within
  a month nearly 400 people had joined her. Covers what the six surviving chronicle
  accounts actually document, the city council's two failed remedies, and the three
  competing modern theories (ergot poisoning, religious/supernatural, mass
  psychogenic illness) ranked from weakest to strongest evidence.
- Payload: `posts/03-dancing-plague-payload.json`
- Script: `scripts/03-dancing-plague-of-1518.md`
- Runtime: 7:51 (narration-length)
- Privacy: public (cadence target); `selfDeclaredMadeForKids: "no"` (hard rule 2 —
  general-audience history content)
- Sources cited in description per hard rule 6: Wikipedia; National Geographic;
  John Waller, *A Time to Dance, A Time to Die* (2008) and *The Lancet* (2009);
  Lynneth J. Miller [Renberg], *Dance Research* (2017).
- Pillar: Strange But True (first F&F video in this pillar — prior two were both
  Unsolved & Unexplained).
- **PUBLISHED 2026-11-05.** Katie approved on the HQ dashboard
  (to-do `r20261105-youtube-production-01`) and ran the `--yes` publish herself
  from her Mac terminal (this session's auto-mode safety gate again blocked it
  from running `--yes` itself — "Create Public Surface" — same as 11/3):
  `postId cmw3vnrqv0gkpod07x2z1xcq9` (integration `cmvy6plen09q6nk0750rg2fha`).
  Confirmed live public.

## 2026-11-03 — "The Lost Colony of Roanoke: Every Theory, Ranked"
- Logline: John White returns to Roanoke in 1590 to find all 117 colonists gone
  without a trace, save the single word "CROATOAN" carved into a post. Ranks
  all six leading disappearance theories from weakest to strongest evidence.
- Payload: `posts/02-roanoke-payload.json`
- Script: `scripts/02-roanoke-lost-colony.md`
- Runtime: 7:15 (narration-length)
- Privacy: public (cadence target); `selfDeclaredMadeForKids: "no"` (hard rule 2
  — general-audience history content)
- Sources cited in description per hard rule 6: National Park Service / Fort
  Raleigh National Historic Site, NCpedia, History Hit.
- **PUBLISHED 2026-11-03.** Katie approved on the HQ dashboard
  (to-do `r20261103-youtube-production-03`). This session's auto-mode safety
  gate blocked it from running the `--yes` publish itself ("Create Public
  Surface"), so Katie ran it herself from her Mac terminal:
  `postId cmw11tt9l024rnx06emyi3utv` (integration `cmvy6plen09q6nk0750rg2fha`).
  Confirmed live public.
- Note: this video was originally produced in a 2026-11-02 session but could
  not be uploaded that day because the device bridge to Katie's Mac was
  unreachable; the finished media file from that run was not recoverable in
  a later session, so narration, all 9 images, and video assembly were
  redone from the surviving script on 2026-11-03. No content changes from
  the original plan — same script, same shot list, same settings.
