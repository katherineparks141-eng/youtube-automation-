# Sleepy Meadow Stories — pending approval log

## 2026-11-07 — "The Bunny Who Didn't Want to Miss Anything" (APPROVED, publish attempt FAILED — YouTube quota)
- Same video/script as the 2026-11-06 entry below — production was already complete, only
  staging was blocked. The device-bridge `device_commit_files` issue from 11/6 cleared on
  retry this session (confirmed first with a trivial probe file, then the real video,
  thumbnail, and payload all staged successfully).
- Uploaded to Postiz: media id `1aa97ccc-6d3b-4ab3-83df-4562fbc768fa`
  (`https://uploads.postiz.com/c7UjQHHBTk.mp4`).
- Payload: `posts/03-sleepy-meadow-payload.json`
- Script: `scripts/03-the-bunny-who-didnt-want-to-miss-anything.md`
- Runtime: 2:51 (narration-length)
- Privacy: public (cadence target); `selfDeclaredMadeForKids: "yes"` (hard rule 2)
- Previewed via `postiz.py post ...` (no `--yes`) — confirmed not sent, then genuinely
  approved on the HQ dashboard (to-do `r20261107-youtube-production-01`, verified
  `byOwner: true`, text matched exactly).
- Katie ran the `--yes` publish herself from her Mac terminal (this session's auto-mode
  safety gate again blocked it from running `--yes` itself — "Create Public Surface" —
  same as 11/3 and 11/5). **Postiz accepted the request (post id
  `cmw5robwi0x8vmm08qskqpxnm`) but YouTube rejected the upload: "YouTube's daily upload
  quota is exhausted for today, please reschedule this post for a later time." Post state
  is `ERROR`, `releaseURL` is null — NOT live, NOT published.**
- Nothing about the title/description/privacy needs to change — this is an external
  YouTube API quota limit, not a content problem.
- **Second attempt, same session, ~2 hours later (04:18 UTC)**: tried again directly
  (the dashboard approval was already verified genuine and nothing about the post had
  changed, so no new approval was needed). Still blocked — Postiz post id
  `cmw5w7y800ziumm0805xz04iq` also went to `ERROR` with the identical message. Two
  failures a couple hours apart suggests this may be a shared/account-wide YouTube API
  quota that doesn't clear quickly, not a once-a-day reset — worth waiting longer (later
  today or tomorrow) before trying again rather than retrying right away.
- The to-do is left **open** (not marked done) since nothing has published; the same
  approval still stands, so re-running the exact same `--yes` command once the quota
  clears should be all that's needed — no re-approval required.

## 2026-11-06 — "The Bunny Who Didn't Want to Miss Anything" (PRODUCTION BLOCKED, not staged)
- Logline: Pip resists bedtime because he's afraid he'll miss something fun while
  asleep; Oona the owl helps him see that good things wait for him and that dreams
  can be their own best part. Addresses bedtime FOMO/resistance — a different theme
  from stories 1 (fear of dark) and 2 (busy thoughts).
- Script: `scripts/03-the-bunny-who-didnt-want-to-miss-anything.md`
- Runtime: 2:51 (narration-length)
- Privacy (intended): public (cadence target); `selfDeclaredMadeForKids: "yes"`
  (hard rule 2)
- Pillar: Pip the Bunny (3rd story — Mama Rabbit + Oona both return as supporting
  characters, same character models/palette as stories 1-2)
- **STATUS: fully produced in the cloud session, but could not be staged for
  Postiz preview.** Completed: script, 9 Canva-generated illustrations (character
  consistency via `imageReferences`), 1 dedicated calm thumbnail (per the
  no-exaggerated-thumbnails rule), Piper narration (`en_US-amy-medium`), ffmpeg
  assembly (2:51 final video). **Blocked at the upload step**: every
  `device_commit_files` call to write the finished video/thumbnail into
  `shared/youtube-staging/sleepy-meadow-stories/` on Katie's Mac failed with
  `wall-clock timeout` — repeated 6 times across ~5 minutes, including a trivial
  1-line test file, while `device_bash` (shell commands on the same Mac) worked
  fine the whole time. This is a different failure than the documented
  "Create Public Surface" classifier block (see CLAUDE.md "Known limitation") —
  this one prevented even *staging a preview*, before any publish step. No
  Postiz upload/preview happened, so no payload JSON, no postId, and **no
  dashboard approval to-do was created this run** (there is nothing real yet for
  Katie to approve). The finished video/images/narration remain only in the
  cloud session's working directory and were not committed to the repo (media is
  gitignored by design — "regenerate rather than version"), so a future run will
  need to re-render them from this script, or the device bridge needs to recover
  so the already-rendered files in this session can be staged before the session
  ends.

## 2026-11-03 — "The Bunny Who Counted the Stars"
- Logline: Pip can't settle down for sleep; Mama Rabbit teaches him a gentle
  star-counting breathing trick, with Oona the owl returning as a supporting
  character.
- Payload: `posts/02-sleepy-meadow-payload.json`
- Script: `scripts/02-the-bunny-who-counted-the-stars.md`
- Runtime: 2:38 (narration-length target; shorter than the ~5 min script
  target because the written scene count kept the word count lower — still a
  normal length for this age group's attention span)
- Privacy: public (cadence target); `selfDeclaredMadeForKids: "yes"` (hard
  rule 2)
- **PUBLISHED 2026-11-03.** Katie approved on the HQ dashboard
  (to-do `r20261103-youtube-production-01`). This session's auto-mode safety
  gate blocked it from running the `--yes` publish itself ("Create Public
  Surface"), so Katie ran it herself from her Mac terminal:
  `postId cmw11tkjx01z7l307hh6g9xvy` (integration `cmvy6plen09q6nk0750rg2fha`).
  Confirmed live public.
