# Forgotten & Found — pending approval log

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
