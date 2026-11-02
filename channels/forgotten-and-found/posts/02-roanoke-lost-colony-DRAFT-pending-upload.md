# 02 — The Lost Colony of Roanoke: Every Theory, Ranked
Status: **PRODUCED, NOT YET PREVIEWED ON POSTIZ** (blocked — see note at bottom)
Channel: Forgotten & Found | Pillar: Unsolved & Unexplained (UU) | Date produced: 2026-11-02

This is a draft record of the finished video's packaging, so the next run (once the device
bridge can reach Katie's Mac) can finish Step 3 (Postiz upload + preview) and Step 4
(dashboard to-do) without redoing the creative work. **Do not treat this file as a payload —
it has no real Postiz media id yet.** Once uploaded, replace this file with
`02-roanoke-payload.json` in the same shape as `01-bell-witch-payload.json`.

## Title
The Lost Colony of Roanoke: Every Theory, Ranked

## Description
The Lost Colony of Roanoke disappeared in 1590, leaving behind only one carved word. #LostColony We rank the six real theories for what happened — from weakest to strongest — using only what's actually documented.

This video uses AI narration and AI-generated illustrations to tell a researched, source-checked history.

Sources: National Park Service, Fort Raleigh National Historic Site — "Major Theories of the Lost Colony" (home.nps.gov/fora); NCpedia (North Carolina Government & Heritage Library) — "Virginia Dare and the Lost Colony: Fact and Legend"; History Hit — "The Mystery of the Lost Roanoke Colony"

#ForgottenAndFound #RoanokeIsland #AmericanHistory #UnsolvedMystery

## Hidden tags box (≤500 chars)
roanoke colony, lost colony of roanoke, roanoke island mystery, croatoan, john white roanoke, virginia dare, american history mystery, unsolved mysteries history, colonial america, roanoke colony theories, what happened to roanoke colony, dare stone, fort raleigh, 1587 roanoke, english colonists disappeared

## Settings for the Postiz payload (once uploaded)
- `selfDeclaredMadeForKids`: "no" (Forgotten & Found — hard rule 2)
- `type`: "public" (cadence target)
- `integration.id`: cmvy6plen09q6nk0750rg2fha (Katie Tuell YouTube channel)

## Production record
- Script: `channels/forgotten-and-found/scripts/02-roanoke-lost-colony.md`
- Narration: Piper TTS, `en_US-lessac-medium`, length-scale 1.10 — ~7:15 runtime
- Visuals: 9 images, Runway `nano-banana-pro` (16:9, 1K) — cold open, Atlantic-crossing map,
  1587 dockside farewell, abandoned settlement, CROATOAN carving close-up (also used as the
  dedicated thumbnail), six-theory map, present-day Fort Raleigh site, Lost Colony outdoor
  drama, closing shoreline shot
- Assembly: `pipeline/assemble_video.sh` — 1920x1080 h264/aac, ~7:15, ~48MB
- Thumbnail: CROATOAN carving close-up (carries the emotional hook; title carries the
  informational one, per packaging rules)

## Why this is blocked
Step 3 (`postiz.py upload` + `postiz.py post` preview, run on Katie's Mac via
`~/katie-hq/shared/postiz.py`) needs the finished ~48MB .mp4 physically on her Mac first.
This run's device bridge (`mcp__remote-devices__device_request_folder_access`) was declined
when requesting `~/katie-hq` — expected in an unattended run with nobody there to approve it.
A separate local tool (desktop-commander) does have standing shell/file access to Katie's Mac
and was used successfully for Steps 1 and 1.5 (text-only commands), but it has no
binary-file-transfer path suited to a 48MB video, and routing around the declined folder
access with an improvised transfer was avoided per this routine's explicit instruction not to
guess around a blocked step.

The finished video, thumbnail, and script were sent directly to Katie via chat instead, so the
production work isn't lost. **Nothing was uploaded to Postiz, nothing was staged as a
dashboard to-do, and nothing was published.** A future run — or Katie manually — can run:

```
python3 ~/katie-hq/shared/postiz.py upload --project forgotten-and-found 02-roanoke-lost-colony.mp4
python3 ~/katie-hq/shared/postiz.py post --project forgotten-and-found 02-roanoke-payload.json
```
(without `--yes`) once the video file is on Katie's Mac, then follow the normal Approval flow.
