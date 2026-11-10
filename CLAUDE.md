# YouTube Automation — operating rules

This file is the standing playbook for Katie's fully-automated YouTube work. Any Claude
session working in this repo (or picking this project back up from `claude.ai`) should
read this first and follow it. It covers two channel concepts currently running
side-by-side as a test: **Forgotten & Found** (history/folklore, zero filming) and
**Sleepy Meadow Stories** (original kids' bedtime stories, zero filming). Full strategy
detail for both lives in the "Business Ideas Playbook" Claude Doc
(https://claude.ai/artifact/fb773ed3-b385-41b6-8489-a1b4d5704920, Ideas 8 and 9) — this
file is the *execution* rules, that doc is the *strategy*. Keep both in sync.

## Hard rules (never break these)

1. **Never publish without Katie's explicit yes on that exact post.** The posting script
   (`~/katie-hq/shared/postiz.py` on her Mac) previews by default and only sends with
   `--yes`. That flag is only ever used after Katie has approved that specific video,
   title, description, and privacy setting — never on a standing "go ahead." Per Katie's
   existing HQ pattern (`~/katie-hq/shared/RUN_CLOSEOUT.md`), that approval is captured as
   a to-do on the Katie HQ dashboard (https://claude.ai/artifact/KPm8DRRk9RrVT9JH3YtcQL,
   `ArtifactData` collection `todos`, project id `youtube`) with `ask: "approve"` — her
   Approve tap there (collection `approvals`, doc id = the to-do id, `byOwner: true`,
   `text` unchanged) is the "yes," not a chat reply. See "Approval flow" below.
2. **Made-for-kids declaration must be accurate per channel, not defaulted.**
   - Forgotten & Found → `selfDeclaredMadeForKids: "no"` (general-audience content).
   - Sleepy Meadow Stories → `selfDeclaredMadeForKids: "yes"` (genuinely children's
     content — misdeclaring this is a real FTC/COPPA compliance risk, not a style choice).
3. **Every video description includes an AI-disclosure line.** Something like "This
   video uses AI narration and AI-generated illustrations." Non-negotiable per both
   channels' identity (set in Idea 8/9) and YouTube's synthetic-media disclosure
   expectations.
4. **No copyrighted or trademarked characters/IP, ever.** Original characters and
   original research only. (This is *why* the channel pivoted away from stitched TV-show
   compilations — see the Playbook doc for the full reasoning.)
5. **No credentialed-advice framing.** Nothing presented as medical, legal, or financial
   advice — this is what makes AI-narrated content eligible for monetization under
   YouTube's policy in the first place.
6. **Every factual/history video cites its sources** in the description (see Bell Witch
   example under `channels/forgotten-and-found/scripts/`).
7. **Never commit secrets to this repo.** The real `POSTIZ_API_KEY` lives only in
   `~/katie-hq/shared/.env` on Katie's Mac and is never duplicated here. This repo's
   `postiz_channels.json` reference only contains channel/project IDs, which are not
   secret.
8. **Posting is channel-scoped.** This project posts only to the channels listed for
   `forgotten-and-found` in `~/katie-hq/shared/postiz_channels.json` (currently the
   "Katie Tuell" YouTube channel, integration id `cmvy6plen09q6nk0750rg2fha`). Don't add
   channels to that file without Katie naming them.

## Automation (2026-11-09)

Publishing moved to GitHub Actions + direct YouTube API. Routine: produce, commit payload,
commit `video.mp4` as `staged/post-<channel>-<NN>/video.mp4` in the PRIVATE repo `youtube-automation-media` (never a public repo), run `gh workflow run publish.yml -f
post=<payload> -f tag=<tag>`. Katie's approval is the `publish-approval` environment
review on GitHub, not a dashboard tap. Never run `--yes` or publish any other way. See
`docs/AUTOMATION.md`. The Postiz/dashboard sections below are legacy until setup is done.

## Cadence target

**2 new videos a week per channel, public — 4 total across Forgotten & Found and
Sleepy Meadow combined.** Confirmed by Katie on Nov 1, 2026 (originally stated as "3 a
week" and clarified to 2 each). This roughly doubles the per-channel production load
compared to the earlier "3 combined" draft — worth watching that Piper/Canva/ffmpeg
generation time still comfortably supports 2/week per channel before pushing further.

- **Floor:** never drop below 1/week per active channel — research (vidIQ, 10M+ channel
  study) shows under-1/month channels barely grow at all, while ~weekly is the first
  tier with real traction. 2/week is comfortably above this floor for both channels.
- **Timing:** publish weekday afternoons, 2–4 PM Eastern, Wednesday performs best for
  long-form. Publish 1–2 hours before the actual audience peak so YouTube can index
  first. (Matters more once a channel is past ~10K subs — below that, consistency beats
  precision.)
- **Suggested slot pattern at 2/week per channel:** each channel posts afternoons on
  two of Mon / Wed / Fri, staggered so Forgotten & Found and Sleepy Meadow don't both
  land the same day — e.g. Forgotten & Found on Mon/Thu, Sleepy Meadow on Tue/Fri —
  which also spreads production load across the week instead of batching 4 videos into
  2 days.

## Production pipeline (per video)

1. **Research + script** — Claude writes a timestamped script with visual notes per
   beat. History videos (Forgotten & Found) cite every source at the bottom. Kids videos
   (Sleepy Meadow) keep a consistent original-character model described explicitly.
2. **Narration — free, offline, no API cost.** Piper TTS, installed via
   `pip install piper-tts`. Voice models already set up:
   - Forgotten & Found → `en_US-lessac-medium` (calm, measured male narrator)
   - Sleepy Meadow → `en_US-amy-medium` (warm female narrator)
   Voice models download once from Hugging Face (`rhasspy/piper-voices`) — see
   `pipeline/setup_tts_voices.sh`. Generate with `pipeline/generate_narration.py`.
   (Narration stays on Piper always — neither Runway nor Higgsfield can generate speech
   on a free plan, and Katie decided Nov 1, 2026 not to pay to unlock either for this.)
3. **Visuals — Canva's `generate-image` tool is the primary source**, not plan-gated.
   For any recurring character (e.g. Pip the bunny), generate one reference image first,
   then pass its Canva media id as `imageReferences` on every subsequent image of that
   character for visual consistency.
   **Runway's free-tier image models (nano-banana-pro, seedream-5-pro, gen-4, etc.) are a
   secondary source** — Katie has ~530 leftover credits there and image generation
   (unlike speech/video) isn't plan-gated on Runway's free tier, so it's worth spending
   those down before they expire/she cancels, rather than leaving them unused. Higgsfield
   is NOT used for visuals or narration going forward (see "Open items" — image gen is
   blocked outright on its free plan and its audio credit allowance is too small to be
   useful); drop it from the pipeline.
4. **Assembly — ffmpeg, local, no cost.** Ken Burns pan/zoom per still, duration sliced
   evenly across the image set to match total narration length, then muxed with the
   narration track. Template in `pipeline/assemble_video.sh`.
5. **Upload + preview — Postiz, via the shared script.**
   ```
   python3 ~/katie-hq/shared/postiz.py upload --project forgotten-and-found FILE.mp4
   python3 ~/katie-hq/shared/postiz.py post --project forgotten-and-found payload.json
   ```
   without `--yes` first — this only previews, nothing is sent.
6. **Publish** — only after Katie's Approve tap on the dashboard to-do for that exact
   video (see "Approval flow" below) — never from a chat "go ahead" and never from a
   standing instruction.

## Approval flow (Katie HQ dashboard)

Katie's existing cross-project pattern (`~/katie-hq/shared/RUN_CLOSEOUT.md`) is how every
automated run gets her yes, and this project uses it instead of a chat-only approval:

1. After producing a preview (step 5 above), add ONE to-do via `ArtifactData` `batch`
   (op `set`) to collection `todos` on the dashboard
   (`https://claude.ai/artifact/KPm8DRRk9RrVT9JH3YtcQL`), doc_id
   `r<YYYYMMDD>-youtube-production-01` (increment the suffix if more than one that day):
   ```json
   {
     "project": "youtube",
     "projectName": "YouTube Automation",
     "text": "Approve posting \"<title>\" (<channel>, public) to the Katie Tuell YouTube channel",
     "ask": "approve",
     "done": false,
     "createdAt": "<ISO now>",
     "source": "youtube-production",
     "sourceName": "YouTube automation routine",
     "prompt": "Work in the youtube-automation- repo (katherineparks141-eng/youtube-automation-). Read channels/<channel>/posts/<NN>-payload.json and the matching script. The preview is already uploaded to Postiz. Run `python3 ~/katie-hq/shared/postiz.py post --project forgotten-and-found payload.json --yes` to publish it, then confirm it posted and update the to-do. End with /wrap."
   }
   ```
   `text` must name the exact title, channel, and "public" — that exact wording is what
   her Approve tap counts as a yes for.
2. **Every new routine firing starts by checking for a pending approval from last time**,
   per `RUN_CLOSEOUT.md` step 3b: `list`/`query` the `todos` collection for open
   (`done: false`) docs with `source: "youtube-production"`, then read the matching
   `approvals/<same doc id>` doc. If `byOwner: true` and `text` matches exactly with no
   `handledAt` yet: that is Katie's yes — run the `--yes` publish now, then `update` the
   approval with `handledAt` + one-line `result`, and tick the to-do `done: true`. If the
   approval doc doesn't exist yet or has no tap, leave it — don't publish, don't nag, just
   move on to producing the next video.
3. Never publish a video whose to-do Katie hasn't tapped Approve on. Never mark a to-do
   done without having actually published (or, if the attempt failed, without saying so
   in `result`).

## Analytics report (views, followers, spend, profit)

Katie asked for this to live on the Katie HQ dashboard (Nov 1, 2026), not in a separate
report. It's read-only reporting — no approval needed to refresh it.

- **Numbers:** `ArtifactData` `get`, collection `dashboard`, doc_id `youtube-analytics`,
  on https://claude.ai/artifact/KPm8DRRk9RrVT9JH3YtcQL. Fields: `views` (sum of per-post
  views), `subscribersNetChange` (gained − lost; Postiz has no absolute subscriber-count
  endpoint — check YouTube Studio for the real total), `spendUsd`, `revenueUsd`,
  `profitUsd`, `monetized`, `perVideo[]` (title/channel/postId/views/likes/comments).
- **Source of the numbers:**
  - Per-video views/likes/comments: `python3 ~/katie-hq/shared/postiz.py analytics --post <postId> --days 30` (one call per published video; postIds are in each channel's `posts/*.json` after publish).
  - Channel-level (minutes watched, subscribers gained/lost, average view %):
    `python3 ~/katie-hq/shared/postiz.py analytics --integration cmvy6plen09q6nk0750rg2fha --days 30`.
  - Spend: $0 as long as the pipeline stays on free Piper + Canva + ffmpeg + Runway's
    free-tier image credits (see "Open items"). If that ever changes (a paid plan, a
    credit purchase), log the real dollar amount here — never guess.
  - Revenue/profit: $0 until the channel is monetized (YouTube Partner Program: 1,000
    subscribers + 4,000 public watch hours, or the Shorts equivalent, in the trailing 12
    months). Once monetized, pull AdSense revenue the same way other revenue numbers get
    confirmed elsewhere in Katie HQ — never estimate it.
- **Refresh:** every scheduled production run (`STEP 1.5` in the routine) re-pulls these
  numbers and `update`s the `youtube-analytics` doc, then updates the one-line `line`
  field on the `youtube` project card in `dashboard/current`.projects[] (so it shows on
  the main Projects tab without needing a separate report) and mirrors the same two
  writes into `~/katie-hq/shared/dashboard.json`.

## Packaging rules (titles, thumbnails, hashtags, tags, captions)

- **Title + thumbnail must not repeat each other.** Thumbnail carries the emotional
  hook, title carries the informational one.
- **Keep a consistent visual template per channel** (palette, art style, character
  model) so returning viewers recognize the video in-feed before reading anything.
- **Sleepy Meadow specifically: keep thumbnails calm, not exaggerated.** Research on
  kids-channel trust signals shows exaggerated/clickbait thumbnails on children's
  content actively *hurt* recommendations — the opposite of adult-niche advice.
- **Hashtags:** 3–5 in the description (one in the first 100 characters), 1–2 max in
  the title if any. Hard ceiling of 15 — YouTube may ignore all hashtags on a video past
  that. Never reuse an identical hashtag set video-to-video (reads as spam); keep 1–2
  branded hashtags constant (e.g. `#ForgottenAndFound`) and vary the rest per topic.
- **Tags box (hidden, 500-char limit):** long-tail and commonly-misspelled variants of
  the visible hashtags/keywords.
- **Captions:** auto-generate and leave on — most watch time is mobile, captions matter
  for accessibility and retention.
- **End screens / series pointer:** every video's closing line + end screen should point
  at the next video in its content pillar, to build session-watching (already built into
  both channels' narrative structures).
- **Playlists per content pillar** once there are 3+ videos in a pillar (Forgotten &
  Found: UU / LP / FH / SB from Idea 8; Sleepy Meadow: by theme once it has more than one
  story family).

## Promotion

- A/B test thumbnails: if CTR falls below the channel's own rolling average after
  24–48 hours, swap it — YouTube allows thumbnail changes any time.
- Avoid anything that reads as mass-templated — YouTube's "inauthentic content" policy
  specifically targets template-only, no-human-judgment output. Keep genuine variation
  in angle, pacing, and visuals between videos even within the same format.
- Track traffic source breakdown (Studio → Reach tab) per video; tune packaging to
  whichever surface (Browse/Suggested vs. Search) is actually driving each video's views.
- Weekly/monthly review cadence already defined in Idea 7 of the Playbook doc — run it
  against these new videos too, not just as a one-off audit.

## Known limitation: scheduled runs can't actually execute `--yes`

Discovered 2026-11-03. The scheduled task (`trig_01Cqhoxe6NxbohqsMRQrPLgb`,
`permission_mode: "auto"`) already has automatic tool approval — but when a
run tried to execute `postiz.py post ... --yes` for a video Katie had already
approved on the dashboard (via the documented approval flow in this file), it
was blocked by a *separate* environment-level guardrail: "Permission for this
action was denied by the Claude Code auto mode classifier. Reason: [Create
Public Surface]." This is not the same thing as the trigger's own
`permission_mode` — a scheduled task set to `auto` still hits this block, so
raising/changing the trigger's approval setting does not fix it on its own.

Practical effect: STEP 1 of the routine (publishing a prior approval) can
build the to-do, read Katie's Approve tap, and confirm it's genuine — but it
cannot actually run the `--yes` command. It should stop there and report
clearly that a valid approval is waiting but could not be executed, so Katie
can run the `postiz.py post ... --yes` command herself (she can copy it
directly from the to-do's `prompt` field). Do not try to route around this by
using a different tool, a different session type, or a workaround shell
trick — it's a deliberate guardrail against autonomous sessions taking
irreversible public-facing actions unattended, and routing around it defeats
the point of hard rule 1 (never publish without Katie's actual yes being
*executed* by someone who can be held to it).

Open question for Katie: is there a way to configure this specific scheduled
task (or a dedicated "publish-only" task) so that it CAN execute an already
Katie-approved `--yes` publish unattended, without weakening the guardrail
for anything else? This needs investigating with Anthropic's scheduled-task /
Cowork documentation — not guessed at. Until resolved, every publish needs a
human to run the final `--yes` command by hand, even when the Katie HQ
dashboard approval flow already captured a genuine, verifiable yes.

**Research findings (2026-11-03):** This is Claude Code's "auto mode"
classifier — a model that reviews actions that would otherwise prompt for
approval, even when a scheduled task's `permission_mode` is `"auto"` (which
only skips the *human-in-the-loop prompt*, not the classifier itself). The
classifier returns a bracketed rule name on denial (`[Create Public
Surface]` here; official docs mention `[Data Exfiltration]` as another
example) — "Create Public Surface" itself isn't named in the public docs we
could reach, so its exact scope is inferred from the denial message, not
confirmed. What IS documented:
  - An **org admin** can disable auto mode entirely for the organization via
    managed settings (`permissions.disableAutoMode: "disable"`) — this
    would make every action in every scheduled run require a real human
    approval, which is the opposite of what we want here.
  - A **user-level** `~/.claude/settings.json` can set `autoMode.allow` /
    `autoMode.environment` entries to mark specific repos/services as
    trusted, and `permissions.allow` rules can explicitly allow a specific
    command. **Unverified**: whether a `permissions.allow` rule for the
    exact `postiz.py ... --yes` command actually overrides this specific
    classifier category, since "Create Public Surface" looks like a
    content-level judgment (publishing something public) rather than a
    path/command-level permission the usual allow-list mechanism targets.
  - No config was found that targets "Create Public Surface" by name
    specifically, or that would let a *cloud scheduled task* (as opposed to
    a local CLI session) carry a custom settings.json at all — scheduled
    cloud runs may not read `~/.claude/settings.json` on Katie's Mac the
    way a local session would.
  - The honest conclusion: there is no confirmed, documented way to make an
    unattended scheduled run actually execute a real `--yes` publish. The
    safest reading is that this is a deliberate, largely non-configurable
    guardrail against autonomous agents taking irreversible public-facing
    actions unattended — which is actually in line with hard rule 1's
    intent, just enforced one layer deeper (at the harness level) than the
    Katie HQ dashboard approval flow this project built.

**Until/unless this changes:** keep STEP 1 of the routine exactly as
written — verify the approval is genuine, but stop short of running
`--yes`, and report the ready-to-run command so Katie can paste it into her
own terminal (as she's done in practice on 2026-11-03). Don't attempt
workarounds (different tool, different session type, shell tricks) to route
around the classifier; that defeats its purpose.

## Known limitation: `device_commit_files` can fail independently of the publish guardrail

Discovered 2026-11-06. During a scheduled run, after fully producing a Sleepy
Meadow video (script, Canva illustrations, Piper narration, ffmpeg assembly,
thumbnail) in the cloud session, every attempt to stage the finished files onto
Katie's Mac via `device_commit_files` (needed before `postiz.py upload` can run,
since Postiz and its API key only exist on her Mac) failed with `wall-clock
timeout` — 6 attempts over about 5 minutes, including a trivial 1-line test
file written to a folder that already existed. `device_bash` (running shell
commands on the same Mac over the same bridge) worked correctly the entire
time, which rules out the bridge being down generally — this looks like a
narrower fault in the file-commit relay specifically.

This is a different failure from the documented auto-mode classifier block
above: that one stops the `--yes` publish step itself; this one stops *staging
a preview* well before any publish step is reached, so hard rule 1 was never
even in play that run. Practical effect: STEP 3 of the routine can fully
produce a video but cannot always get it onto Katie's Mac for the Postiz
preview, and per the same "don't route around a guardrail/tool failure"
principle as above, a run that hits this should stop, not try an alternate
transfer path (base64 over `device_bash`, re-encoding, etc.), and should
clearly log in the channel's `pending-approval.md` that production finished
but staging failed, with no dashboard to-do created (there's nothing real yet
to approve). The rendered video/images/narration are not committed to the repo
(gitignored by design) and are only reliably recoverable within the session
that made them — if the bridge comes back before that session ends, it's
worth retrying `device_commit_files` on the same files before giving up.

Open question for Katie: was this a one-off (Wi-Fi hiccup, Mac asleep, app
backgrounded) or a sign `device_commit_files` needs a longer timeout / retry
logic for larger files specifically? Worth a quick recheck next time a run
hits this before assuming it's systemic.

## Open items / needs Katie's call

- **One YouTube channel is currently carrying both concepts** ("Katie Tuell" channel).
  Posting folklore/history and toddler bedtime stories to the same channel works for
  this early test phase, but before scaling to 3x/week long-term, consider whether
  Sleepy Meadow should move to its own branded channel — mixing audiences can hurt both
  channels' recommendation targeting.
- **Flipping an already-published video's privacy (private → public)** has no
  documented safe API path through Postiz — do it manually in YouTube Studio
  (Content → privacy dropdown). Don't guess at the API here; a wrong call risks
  duplicate-posting to a live channel.
- **Higgsfield vs. Runway (decided Nov 1, 2026):** Katie was weighing whether to keep
  paying for Runway vs. Higgsfield and use only one. Neither can generate speech or video
  without a paid-plan upgrade (both checked on free-tier connections), so narration stays
  on Piper regardless. For images, Higgsfield's model is fully plan-gated on the free
  tier (unusable), while Runway's image models work on its free tier right now with
  ~530 leftover credits. **Decision: drop Higgsfield, use Canva (primary) + Runway
  (secondary, spend down the leftover credits) for visuals.** Revisit if Runway's free
  tier changes or the credits run out.
