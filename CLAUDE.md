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
   title, description, and privacy setting — never on a standing "go ahead."
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

## Cadence target

**3 new videos a week, public, across the two channels combined** (split roughly evenly
while both are being tested — e.g. 2 Forgotten & Found + 1 Sleepy Meadow one week, flip
the next). This is Katie's instruction as of Nov 1, 2026. If she meant 3 *each* instead
of 3 *combined*, that changes the production load significantly — confirm before scaling
the pipeline further.

- **Floor:** never drop below 1/week per active channel — research (vidIQ, 10M+ channel
  study) shows under-1/month channels barely grow at all, while ~weekly is the first
  tier with real traction.
- **Timing:** publish weekday afternoons, 2–4 PM Eastern, Wednesday performs best for
  long-form. Publish 1–2 hours before the actual audience peak so YouTube can index
  first. (Matters more once a channel is past ~10K subs — below that, consistency beats
  precision.)
- **Suggested slot pattern once at 3/week:** Mon / Wed / Fri afternoons.

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
   (Higgsfield's paid narration is a fallback only if Piper's quality isn't good enough
   for a given video — it costs real credits per generation, confirm spend with Katie
   first.)
3. **Visuals — Canva's `generate-image` tool.** Not plan-gated the way Higgsfield's
   image model is. For any recurring character (e.g. Pip the bunny), generate one
   reference image first, then pass its Canva media id as `imageReferences` on every
   subsequent image of that character for visual consistency.
4. **Assembly — ffmpeg, local, no cost.** Ken Burns pan/zoom per still, duration sliced
   evenly across the image set to match total narration length, then muxed with the
   narration track. Template in `pipeline/assemble_video.sh`.
5. **Upload + preview — Postiz, via the shared script.**
   ```
   python3 ~/katie-hq/shared/postiz.py upload --project forgotten-and-found FILE.mp4
   python3 ~/katie-hq/shared/postiz.py post --project forgotten-and-found payload.json
   ```
   without `--yes` first — this only previews, nothing is sent. Show Katie the preview
   (title, description, tags, privacy, kids declaration) before ever adding `--yes`.
6. **Publish** — only after Katie's explicit yes on that exact preview.

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

## Open items / needs Katie's call

- **One YouTube channel is currently carrying both concepts** ("Katie Tuell" channel).
  Posting folklore/history and toddler bedtime stories to the same channel works for
  this early test phase, but before scaling to 3x/week long-term, consider whether
  Sleepy Meadow should move to its own branded channel — mixing audiences can hurt both
  channels' recommendation targeting.
- **Confirm "3 a week" is combined, not 3 each** (see Cadence section above).
- **Flipping an already-published video's privacy (private → public)** has no
  documented safe API path through Postiz — do it manually in YouTube Studio
  (Content → privacy dropdown). Don't guess at the API here; a wrong call risks
  duplicate-posting to a live channel.
- **Higgsfield credits:** the account is on the free plan (image generation is fully
  plan-gated there; audio costs real credits per generation, ~5 credits for a
  medium-length segment with ~10 free credits total). Canva + Piper are the real
  production path now — only reach for Higgsfield if a specific video needs something
  they can't do, and confirm spend with Katie first.
