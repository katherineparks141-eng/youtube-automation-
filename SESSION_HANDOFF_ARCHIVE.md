
## 2026-11-09 11:40 · Publisher rebuild
**Done:** PRs 1-8 merged. Direct YouTube API publisher (`automation/`), hash-bound approval via `publish-approval` environment (you = required reviewer; repo made public for that), private media repo `youtube-automation-media` read with `MEDIA_TOKEN`, daily `analytics.yml`, `.result.json` written back after publish, routine prompt in `docs/ROUTINE_PROMPT.md` (pasted into routine, live). Google Cloud project `youtube-automation` (app in production). Two private end-to-end tests passed; test artifacts archived.
**Decided by Katie:** Option 1 (chat routine produces, code publishes). Approval = GitHub, not dashboard. Repo public.
**Next:** Watch first routine run (Mon 12:37 PM ET). If it can't reach the media repo or start workflows via `gh`, fix that access. Then stage the stuck Sleepy Meadow video 03 via the new flow (media is on Katie's Mac) or drop it. `MEDIA_TOKEN` expires 2027-02-07.
**Waiting on:** first live routine run. **Watch out:** never publish outside `publish.yml`; media must stay in the private repo; analytics for new videos only from `data/youtube-analytics.json`.
**Branch/uncommitted:** main · 0 uncommitted · 0 unpushed · runs to check: routine run today
