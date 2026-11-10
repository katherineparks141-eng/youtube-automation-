## 2026-11-10 11:05 · Routine fixed, Pip redesigned
**Done:** Routine `trig_012ew37Hpa53gcRdTRL4TZ3q` (old one paused) has both repos, can't start helper agents, and must check git/gh before logging. Voices come from the media repo `voices/` (#11). Videos are committed as `staged/<tag>/video.mp4` and `automation/fetch_video.sh` reads them (#12). Log correction (#15). Pip redesigned in `character-reference.json` (#16).
**Decided by Katie:** redesign Pip (cream, one lop ear, ginger eye patch, mustard scarf, willow hollow; never brown/blue/burrow/round window/lantern/basket). Keep the routine running.
**Next:** check today's 12:30 run: new Pip reference id saved, video staged, `publish.yml` run waiting for approval. The publish dispatch and Actions fetch are still unproven.
**Waiting on:** Katie reviewing live Sleepy Meadow 01-03 (issue #14); `lessac` voice is research-only licensed (to-do added).
**Watch out:** `staged/post-sleepy-meadow-stories-04/` is the old-look video. Never publish it.
**Branch/uncommitted:** main · 0 uncommitted · 0 unpushed · runs to check: routine run 2026-11-10 12:30 ET

## 2026-11-10 09:15 · Routine fixes: voices + video staging
**Done:** Piper voices are now in the private media repo `voices/` (PR #11), and narration works in the cloud. Cloud sessions get HTTP 403 creating GitHub Releases, so the routine now commits `staged/<tag>/video.mp4` to the media repo. `publish.yml` reads it via `automation/fetch_video.sh`, falling back to a release for old tags (PR #12). Routine `trig_012ew37Hpa53gcRdTRL4TZ3q` prompt updated to match.
**Unproven:** the routine pushing the video file, `gh workflow run` from the cloud session, and the Actions fetch with `MEDIA_TOKEN`. First real test is today's 12:30 run.
**Flag for Katie:** the `lessac` voice (Forgotten & Found) is trained on recordings licensed for "Research Purposes only". Check before monetizing.
**Next:** check the 12:30 run (`list_runs` on the routine, then `publish.yml` runs). Sleepy Meadow 04 video from last night was not saved; today's run makes a new one.
**Branch/uncommitted:** main · runs to check: routine run 2026-11-10 12:30 ET

## 2026-11-09 19:40 · New routine with media repo access
**Done:** Old routine (`trig_01Cqhoxe6NxbohqsMRQrPLgb`) could not reach the media repo, and its repo list can't be safely edited, so it's paused. New routine `trig_012ew37Hpa53gcRdTRL4TZ3q` has both repos, same schedule and prompt, Canva + Runway connectors, Default cloud environment. Test run attached both repos.
**Blocked:** `huggingface.co` is denied in the Default cloud environment, so Piper voices can't download and no video gets made. Sleepy Meadow script 04 is written; nothing staged.
**Next:** Fix voice access (own copy in the private media repo, or allow the host in the environment). Then re-run. Canva, upload and `publish.yml` dispatch are still unproven in the new routine.
**Branch/uncommitted:** docs/routine-v2 · runs to check: next routine run

