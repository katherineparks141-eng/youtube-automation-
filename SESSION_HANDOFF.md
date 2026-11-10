## 2026-11-09 19:40 · New routine with media repo access
**Done:** Old routine (`trig_01Cqhoxe6NxbohqsMRQrPLgb`) could not reach the media repo, and its repo list can't be safely edited, so it's paused. New routine `trig_012ew37Hpa53gcRdTRL4TZ3q` has both repos, same schedule and prompt, Canva + Runway connectors, Default cloud environment. Test run attached both repos.
**Blocked:** `huggingface.co` is denied in the Default cloud environment, so Piper voices can't download and no video gets made. Sleepy Meadow script 04 is written; nothing staged.
**Next:** Fix voice access (own copy in the private media repo, or allow the host in the environment). Then re-run. Canva, upload and `publish.yml` dispatch are still unproven in the new routine.
**Branch/uncommitted:** docs/routine-v2 · runs to check: next routine run

## 2026-11-09 11:40 · Publisher rebuild
**Done:** PRs 1-8 merged. Direct YouTube API publisher (`automation/`), hash-bound approval via `publish-approval` environment (you = required reviewer; repo made public for that), private media repo `youtube-automation-media` read with `MEDIA_TOKEN`, daily `analytics.yml`, `.result.json` written back after publish, routine prompt in `docs/ROUTINE_PROMPT.md` (pasted into routine, live). Google Cloud project `youtube-automation` (app in production). Two private end-to-end tests passed; test artifacts archived.
**Decided by Katie:** Option 1 (chat routine produces, code publishes). Approval = GitHub, not dashboard. Repo public.
**Next:** Watch first routine run (Mon 12:37 PM ET). If it can't reach the media repo or start workflows via `gh`, fix that access. Then stage the stuck Sleepy Meadow video 03 via the new flow (media is on Katie's Mac) or drop it. `MEDIA_TOKEN` expires 2027-02-07.
**Waiting on:** first live routine run. **Watch out:** never publish outside `publish.yml`; media must stay in the private repo; analytics for new videos only from `data/youtube-analytics.json`.
**Branch/uncommitted:** main · 0 uncommitted · 0 unpushed · runs to check: routine run today
