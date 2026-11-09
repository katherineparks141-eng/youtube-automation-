# YouTube Automation — Rebuild & Scheduling Spec (handoff to engineering)

**Status:** Draft handoff document. This is a request to rebuild the pipeline below as a
real, reliably-scheduled automated system instead of a series of manually-triggered
Claude Code sessions. Everything in this doc reflects what has actually been built,
tested, and learned running the pipeline by hand for the first ~3 videos per channel
(Nov 1–9, 2026). Nothing here is hypothetical — every failure mode described was hit in
production.

**Owner:** Katie Tuell (katherine.parks141@gmail.com)
**Source repo today:** `katherineparks141-eng/youtube-automation-`
**Playbook today:** [`CLAUDE.md`](../CLAUDE.md) — the full current operating rules. This
spec summarizes and extends it; `CLAUDE.md` remains the source of truth for business
rules (hard rules, cadence, compliance) that must carry over unchanged into the rebuild.

---

## 1. What this system is

Two YouTube channels run as a zero-filming, fully-automated content operation, currently
sharing one YouTube channel ("Katie Tuell") during an early test phase:

- **Forgotten & Found** — history/folklore videos, general audience.
- **Sleepy Meadow Stories** — original-character kids' bedtime stories, genuinely
  made-for-kids content.

Target cadence: **2 new public videos/week per channel (4/week total)**, weekday
afternoons 2–4pm Eastern, staggered so the two channels don't land the same day.

Per-video pipeline, fully scriptable/automatable end to end except for one deliberate
human checkpoint (publish approval):

1. **Research + script** — timestamped script with visual notes per beat. History videos
   cite sources; kids videos keep an explicit consistent character model.
2. **Narration** — Piper TTS (free, offline, no API cost). Voice per channel
   (`en_US-lessac-medium` / `en_US-amy-medium`).
3. **Visuals** — Canva `generate-image` (primary), Runway free-tier image models
   (secondary, spending down existing credits). Recurring characters use a saved
   reference-image id for visual consistency across a scene set.
4. **Assembly** — ffmpeg Ken-Burns pan/zoom per still, sliced evenly across the image set
   to match total narration length, then muxed with narration audio.
5. **Upload + preview** — Postiz API (`~/katie-hq/shared/postiz.py` wrapper today), which
   previews by default and only actually posts with an explicit `--yes`.
6. **Publish** — only after Katie's explicit approval of that exact video (title,
   description, privacy setting). See hard rule 1 below — this gate must not be weakened
   in the rebuild, only made reliable.

---

## 2. Hard rules that MUST carry over unchanged

These are non-negotiable business/compliance rules from `CLAUDE.md`. The rebuild should
enforce them in code (not just in a prompt), since a real backend can make these
actually-unbypassable rather than convention-based:

1. **Never publish without Katie's explicit, verifiable yes on that *exact* post** —
   same video file, title, description, and privacy setting that was approved. No
   standing "go ahead," no approval-by-silence, no approval that doesn't match the
   content being published byte-for-byte (title/description text must match exactly).
2. **`selfDeclaredMadeForKids` must be set per channel, never defaulted**:
   - Forgotten & Found → `"no"` (general audience).
   - Sleepy Meadow Stories → `"yes"` (this is a real FTC/COPPA compliance requirement,
     not a style choice — misdeclaring this is a legal risk, not just a policy slip).
3. **Every video description includes an AI-disclosure line** (e.g. "This video uses AI
   narration and AI-generated illustrations.") — required by YouTube's synthetic-media
   disclosure policy and both channels' stated identity.
4. **No copyrighted or trademarked characters/IP, ever.** Original characters and
   original research only.
5. **No credentialed-advice framing** — nothing presented as medical/legal/financial
   advice. This is also what keeps the content eligible for monetization under YouTube's
   policy for AI-narrated content.
6. **Every factual/history video cites its sources** in the description.
7. **Never commit secrets to the repo.** API keys live only in a secrets store, never in
   version control. (Today: `~/katie-hq/shared/.env` on Katie's Mac, outside this repo.)
8. **Posting is channel-scoped** — this pipeline posts only to pre-registered
   channel/integration IDs. New destination channels require Katie explicitly naming
   them, never an inferred or auto-added destination.

A rebuild that doesn't enforce rule 1 as a real, code-level gate (not a documentation
convention) is not acceptable — see §4 for why the current implementation of this gate is
broken and what it needs instead.

---

## 3. Why this needs to be rebuilt (the actual failures hit in production)

The current implementation runs this entire pipeline inside scheduled/interactive Claude
Code sessions, using a bridge to Katie's own Mac for secrets and file transfer, plus a
Claude-Code-specific "Katie HQ" dashboard (an `ArtifactData`-backed to-do list) as the
approval mechanism. Three distinct, reproducible failure modes have blocked real
publishing so far. All three need to be designed out, not papered over, in the rebuild.

### 3.1 The publish step cannot actually execute, even after a verified approval

**What happens:** Even once Katie's approval is verified as genuine (exact text match,
confirmed tap, no prior handling), the automated session is blocked from running the
final `postiz.py post ... --yes` command by a classifier-level guardrail inside Claude
Code's "auto mode" — denial reason `[Create Public Surface]`. This is **separate** from
the scheduled task's own permission settings (which were already set to auto-approve) —
it's a deeper, non-configurable layer specifically meant to stop autonomous agents from
taking irreversible public-facing actions unattended. Research into Claude Code's
settings turned up no documented, reliable way to allow a specific, pre-approved,
verifiably-human-authorized publish action through this guardrail from a cloud scheduled
session.

**Practical effect today:** every single publish has required Katie to manually copy a
command and run it herself, from her own Mac terminal, after the automation has done
everything else. This defeats the purpose of "automate it" — the one step that most needs
to run on a reliable schedule (publishing at the right time of day) is the one step that
currently *cannot* run unattended at all.

**What the rebuild needs to solve this:** a publish step that runs as a real backend
service/API call (not inside an agentic coding tool's auto-mode sandbox), gated by a
*real* human-approval mechanism the backend itself verifies (e.g., a signed approval
token generated when Katie approves in a dashboard/Slack/email, checked server-side
before the publish call fires) — with no agentic-tool-level guardrail in the loop at
publish time at all. The rebuild's approval gate is the actual rule; it should not depend
on an LLM session's own safety classifier as a backstop, because that classifier is (by
design) going to keep blocking exactly this action.

### 3.2 File transfer between the automation and the human's machine is unreliable

**What happened:** moving the finished video/thumbnail files from the cloud session onto
Katie's Mac (needed only because Postiz's API key lives there) failed outright for one
entire production run — 6 consecutive timeouts over ~5 minutes, including on a trivial
1-line test file — while every other operation on the same connection kept working. It
self-resolved on a later retry with no code change, which points to transient
infrastructure flakiness in that specific transfer path, not a logic bug — but it's a
single point of failure with no retry/backoff built in today, and no way to know in
advance whether a given run will hit it.

**What the rebuild needs to solve this:** the generated media (video files, thumbnails)
and the secrets needed to publish them (Postiz/YouTube API credentials) should live in
the same place — a real cloud environment/object store with the automation's own
credentials — so there is no "hop" between a cloud job and a personal laptop at all. The
Mac-bridge dependency should be eliminated entirely in the rebuild, not just made more
reliable.

### 3.3 YouTube Data API upload quota gets exhausted and doesn't clear predictably

**What happened:** three consecutive publish attempts for the same approved video failed
over ~20 hours (spanning at least one midnight-Pacific boundary, which is the documented
daily reset time for this quota) with the identical error: *"YouTube's daily upload quota
is exhausted for today, please reschedule this post for a later time."* This is YouTube's
standard `quotaExceeded` error on the `videos.insert` endpoint (1,600 quota units per
upload; default allowance 10,000 units/day ≈ 6 uploads/day). Because the error persisted
across a reset boundary, this is very likely a **project-level** quota — i.e., shared
across however many of Postiz's users route uploads through the same backing Google Cloud
project — rather than something caused by Katie's own usage, which has been well under
6 uploads/day.

**What the rebuild needs to solve this:**
- Use (or request) a **dedicated Google Cloud project and OAuth client** for this
  pipeline specifically, rather than inheriting a third-party tool's shared quota —
  this is the only way to guarantee the quota pool isn't being consumed by unrelated
  traffic.
- If staying on Postiz (or any third-party posting layer), get written confirmation from
  that vendor on whether their YouTube integration uses a shared app-level quota, and
  file Google's own **YouTube API Services Audit and Quota Extension** request if
  day-to-day usage is expected to approach the default limit (this is a compliance
  review process on Google's side and can take weeks — budget for it, don't rely on it
  being fast).
- Build real **quota-aware scheduling and backoff** into the publish step: track quota
  usage, queue/delay uploads intelligently rather than retrying blind, and alert a human
  (don't just silently fail) when a publish can't go through — exactly the gap that
  caused three identical failures to look like they might be three different problems
  before being traced to one root cause.
- Monitoring/alerting on `quotaExceeded` specifically, distinct from other upload errors
  (`uploadLimitExceeded` is channel-level and different; `uploadRateLimitExceeded`/
  `userRateLimitExceeded` are short-window throttles, also different) — the rebuild
  should not treat all upload failures the same way.

---

## 4. Approval flow — what must be preserved, and what should change

**Preserve:** a single, auditable, per-video approval step that happens before any
public-facing action, where the approval is tied to the *exact* content (title,
description, privacy, video) being published — never a standing "go ahead."

**Change:** today this runs through a Claude-Code-specific `ArtifactData` dashboard (a
to-do collection + a separate approvals collection, cross-checked for an exact text match
and a genuine owner tap) that only exists because the automation itself is a sequence of
Claude Code sessions. In a rebuilt system this should be a first-class feature of
whatever the new backend is — e.g.:

- A simple internal dashboard/API endpoint showing pending videos with their title,
  description, thumbnail, and a one-click approve/reject, OR
- A Slack/email approval message with a signed link, OR
- Any mechanism where the **approval event itself is what authorizes the publish API
  call** — not a human manually copying a terminal command, which is the current
  workaround for §3.1 and should not become the permanent design.

The rebuild should also preserve the existing pattern of **never marking something
approved/published until it's independently verified** — every publish attempt in the
current system has been checked against Postiz's own API state (`QUEUE` → `PUBLISHED`/
`ERROR`) rather than trusting a command's apparent success or a verbal "I ran it." Build
this verification step into the backend itself (poll or webhook on publish status) rather
than relying on a human or an LLM session to double-check after the fact.

---

## 5. Scheduling requirements

- Real recurring scheduler (cron / cloud scheduler / task queue), not an LLM agent session
  that has to be manually re-triggered or that depends on a chat product's own scheduled-
  task infrastructure.
- Cadence: 2 videos/week/channel, staggered (e.g. Forgotten & Found Mon/Thu, Sleepy
  Meadow Tue/Fri), published weekday afternoons 2–4pm Eastern, 1–2 hours before actual
  audience peak so YouTube can index first.
- Floor: never drop below 1/week per active channel.
- The production pipeline (steps 1–5 in §1) can run fully unattended on this schedule.
  Only the final publish (step 6) waits on human approval — and per §3.1/§4, that wait
  should not require a human to also manually execute the publish command.

---

## 6. Secrets & infrastructure

- Remove the dependency on a personal laptop (`~/katie-hq/shared/.env`, Katie's Mac) for
  any credential or file storage needed by the pipeline. Use a proper secrets manager
  (e.g. the cloud provider's native secrets service) for the Postiz/YouTube API
  credentials, Canva/Runway API keys, etc.
- Never commit secrets to this repo — only non-secret config (channel/integration IDs)
  belongs in version control, same as today.
- Generated media (video, images, audio) should live in cloud object storage, not be
  committed to git (current `.gitignore` already excludes it — "regenerate rather than
  version" — this should carry over) and not depend on a round-trip to a personal device.

---

## 7. Analytics reporting

Carry over the existing reporting requirements:
- Per-video views/likes/comments, pulled per published post.
- Channel-level minutes watched, subscribers gained/lost, average view %.
- Spend (should stay $0 on free-tier Piper/Canva/ffmpeg/Runway-free-credits unless that
  changes — log any real dollar spend, never estimate).
- Revenue/profit ($0 until YouTube Partner Program monetization — 1,000 subscribers +
  4,000 public watch hours in trailing 12 months — never estimate this either).
- Refresh on every scheduled production run, surfaced on whatever dashboard replaces the
  current Katie HQ `ArtifactData` board.

---

## 8. Packaging & compliance rules to carry over

From `CLAUDE.md` — these should become either backend validation checks or template
defaults, not just prompt instructions, where practical:

- Title and thumbnail must not repeat each other (thumbnail = emotional hook, title =
  informational hook).
- Sleepy Meadow thumbnails must stay calm, not exaggerated/clickbait (kids-content trust
  signal — exaggerated thumbnails measurably hurt recommendations on children's content).
- Hashtags: 3–5 in the description (one in the first 100 characters), 1–2 max in title,
  hard ceiling of 15. Never reuse an identical hashtag set video-to-video; keep 1–2
  branded hashtags constant and vary the rest.
- Captions auto-generated and left on.
- End screens/closing line point at the next video in the content pillar.
- Playlists per content pillar once a pillar has 3+ videos.

---

## 9. Open questions for engineering / Katie to resolve during the rebuild

1. **Postiz vs. direct YouTube Data API integration** — given §3.1 and §3.3 are both
   arguably caused by relying on a third-party layer (Postiz) and a general-purpose
   coding agent's safety guardrails for what is fundamentally a scheduled-publish
   service, should the rebuild go direct to the YouTube Data API (with its own Google
   Cloud project/OAuth) instead of through Postiz? This would resolve the shared-quota
   ambiguity in §3.3 outright and remove one integration layer, at the cost of needing to
   reimplement whatever cross-platform posting convenience Postiz currently provides.
2. **One channel vs. two** — both content concepts currently post to the same "Katie
   Tuell" YouTube channel as an early test. Before scaling cadence further, decide
   whether Sleepy Meadow should move to its own branded channel (mixing audiences can
   hurt both channels' recommendation targeting).
3. **Privacy flips (private → public) on an already-published video** — no safe
   documented API path was found through Postiz; confirm the direct YouTube Studio path
   or find the correct API call if going direct to the YouTube Data API.
4. **Runway credit drawdown** — Katie has ~530 leftover free-tier Runway image credits
   she decided to spend down (Nov 1, 2026) rather than leave unused; decide whether the
   rebuild should keep using them as a secondary image source or standardize on Canva
   alone once they run out.

---

## 10. Appendix: incident log referenced above

Full detail and exact error text/timestamps for every attempt described in §3 is
preserved in the channel's run log:
[`channels/sleepy-meadow-stories/posts/pending-approval.md`](../channels/sleepy-meadow-stories/posts/pending-approval.md)
— specifically the 2026-11-06 and 2026-11-07 entries for "The Bunny Who Didn't Want to
Miss Anything," which is also still sitting in the approved-but-unpublished state this
spec is partly written to prevent from recurring. The two "Known limitation" sections in
[`CLAUDE.md`](../CLAUDE.md) are the original write-ups of the §3.1 and §3.2 failures and
should be treated as supporting evidence, not duplicated effort.
