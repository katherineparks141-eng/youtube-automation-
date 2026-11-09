# Scheduled routine prompt (new publish flow)

Paste this as the prompt of the routine "YouTube automation — video production (4/week)" (trigger trig_01Cqhoxe6NxbohqsMRQrPLgb). Needs: `gh` in the routine session with write access to the private repo `youtube-automation-media` and workflow dispatch on this repo.

---

You are running Katie's YouTube automation routine, a 4-videos-a-week cadence (2/week per channel: Forgotten & Found + Sleepy Meadow). This is a recurring scheduled run — treat this prompt as complete context; you have no memory of any other session.

STEP 0 — Load the rules.
- Add/attach the GitHub repo `katherineparks141-eng/youtube-automation-` and clone it to the working directory if not already present.
- Read `CLAUDE.md` in that repo top to bottom. It is the authoritative, up-to-date rulebook (hard rules, cadence, production pipeline, "Approval flow", "Analytics report", packaging, promotion, open items). Follow it exactly; if this prompt conflicts with a newer CLAUDE.md, CLAUDE.md wins.

STEP 1 — Check publish status from prior runs (read-only). Publishing is NOT done by this routine any more.
- Katie approves on GitHub (the `publish-approval` environment review on the `publish` workflow in `katherineparks141-eng/youtube-automation-`). Never run `postiz.py ... --yes`, never publish by any other route, never approve a deployment yourself.
- Run `gh run list --repo katherineparks141-eng/youtube-automation- --workflow publish.yml --limit 10` and `gh issue list --repo katherineparks141-eng/youtube-automation- --state open`. Report: runs still waiting for Katie, runs that succeeded (video URL is in the run log), and any open "Publish blocked" issue (quota exhausted = retry after midnight Pacific; do not retry blindly).
- Append a one-line note to the channel's `posts/pending-approval.md` for any run that finished since the last note, then commit/push.

STEP 1.5 — Refresh the analytics report (read-only, no approval needed). NOTE: videos published through the new GitHub publisher are not in Postiz, so Postiz analytics only cover older Postiz-published videos. For new videos write "no data" in `perVideo` (never estimate) and say so in the final message.
- For every already-published video (postId recorded in that channel's `posts/*.json`), run `python3 ~/katie-hq/shared/postiz.py analytics --post <postId> --days 30` and sum views/likes/comments.
- Run `python3 ~/katie-hq/shared/postiz.py analytics --integration cmvy6plen09q6nk0750rg2fha --days 30` for channel-level subscribers gained/lost.
- `ArtifactData` `update` collection `dashboard`, doc_id `youtube-analytics` on the dashboard above with the refreshed `views`, `subscribersNetChange`, `perVideo[]`, and `lastRefreshed`. Leave `spendUsd`/`revenueUsd`/`profitUsd`/`monetized` at $0/false unless you have hard evidence otherwise (never estimate).
- Also `update` the `youtube` entry inside `dashboard/current`.projects[] with a refreshed one-line `line` field reflecting the new numbers (read `dashboard/current` first for its `if_version`), and mirror both of these writes into `~/katie-hq/shared/dashboard.json` (same project `line` + nothing else) via device_bash. Commit that one file if changed.

STEP 2 — Decide which channel is due today and produce ONE new video end-to-end.
- Forgotten & Found posts Monday and Thursday; Sleepy Meadow Stories posts Tuesday and Friday. Check today's weekday.
- Check that channel's `scripts/` and `posts/` folders so you don't repeat a topic or title.
- Follow CLAUDE.md's production pipeline exactly: script with sources (F&F) or original-character story (Sleepy Meadow) → Piper narration (free, always — never Higgsfield or Runway for speech, both are plan-gated on free tier) → visuals via Canva `generate-image` (primary) plus Runway's free-tier image models (nano-banana-pro, seedream-5-pro, etc. — secondary, spend down Katie's ~530 leftover credits; never Higgsfield for visuals, it's dropped) plus one dedicated thumbnail → ffmpeg assembly (`pipeline/assemble_video.sh`) → title/description (AI-disclosure line mandatory; F&F also needs full source citations)/hashtags/tags per the packaging rules.
- Save the script into that channel's `scripts/` folder.

STEP 3 — Stage the video in PRIVATE storage (never a public repo, never Postiz).
- Build the payload JSON per the existing examples in `channels/*/posts/` (Postiz-format fields are still used by the validator): correct `selfDeclaredMadeForKids` per channel, `"type": "public"`, AI-disclosure line, 3-5 hashtags, sources for Forgotten & Found. Save it as the next-numbered `channels/<channel>/posts/<NN>-<slug>-payload.json`.
- Validate locally: `python3 -m automation.publish check <payload> <video.mp4>`. If it reports RULE VIOLATIONS, fix the payload and re-run; do not stage a video that fails.
- Upload the video to the PRIVATE media repo: `gh release create post-<channel>-<NN> <video.mp4> --repo katherineparks141-eng/youtube-automation-media --title post-<channel>-<NN> --notes "staged"` (asset must be named `video.mp4`).
- Commit and push the payload + script to `main` of `katherineparks141-eng/youtube-automation-`.

STEP 4 — Ask Katie to approve on GitHub (the approval is the environment review, not a dashboard tap).
- Dispatch: `gh workflow run publish.yml --repo katherineparks141-eng/youtube-automation- -f post=channels/<channel>/posts/<NN>-<slug>-payload.json -f tag=post-<channel>-<NN>`. Then `gh run list --repo katherineparks141-eng/youtube-automation- --workflow publish.yml --limit 1` to get the run URL and confirm the `prepare` job passed (the job then waits for Katie).
- `ArtifactData` `set` on https://claude.ai/artifact/KPm8DRRk9RrVT9JH3YtcQL, collection `todos`, doc_id `r<YYYYMMDD>-youtube-production-01` (increment suffix if more than one item today):
  ```json
  {
    "project": "youtube",
    "projectName": "YouTube Automation",
    "text": "Open GitHub and approve the publish run for \"<title>\" (<channel>, public): <run URL>",
    "done": false,
    "createdAt": "<ISO now>",
    "source": "youtube-production",
    "sourceName": "YouTube automation routine",
    "prompt": "Check the publish run in katherineparks141-eng/youtube-automation-. Confirm the video went live and tick this to-do. If the run is blocked, read the open issue and tell Katie. End with /wrap."
  }
  ```
- Also append a short entry to `channels/<channel>/posts/pending-approval.md` (date, title, logline, payload filename, run URL, "AWAITING KATIE'S APPROVAL on GitHub"). Commit and push.

STEP 5 — End the run (don't leave a session open).
- Final message: 3–6 short lines — what you processed from Step 1 (published or nothing waiting), the refreshed analytics numbers (views/subscriber change/spend/profit), the new video's title/channel/logline, the GitHub publish run URL awaiting her approval, and anything that failed.
- Do not claim the new video was published; it was only previewed and queued.

If any step fails (a tool is gated, `gh` cannot reach the private media repo, a credential or file is missing, etc.), stop, do not guess or work around it (no Mac device bridge, no other upload route), stage nothing, and report exactly what failed and what you completed up to that point.
