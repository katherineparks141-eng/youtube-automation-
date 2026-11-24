## 2026-11-24 18:15 · Stories 07+08 published
**Done:** Katie approved Sleepy Meadow story 07 (run 44787449303) and story 08 (run 45458685207) in chat; both runs succeeded and both are public: https://youtu.be/5g8uHlEoNdU and https://youtu.be/mU3b2K33XSk (result files in `channels/sleepy-meadow-stories/posts/`). Checked each payload first (public, made-for-kids yes, AI disclosure). Dashboard card updated; to-do `r20261124-youtube-production-01` ticked. Confirmed F&F Mary Celeste public since 11/20.
**Decided by Katie:** "approve story 07", then "Approve 08 now" (same day, her call over the stagger suggestion).
**Next:** nothing is waiting on approval; the routine's next run produces the next video and logs these two publishes in `pending-approval.md`.
**Waiting on:** Katie: `lessac` voice license; unpublished Sleepy Meadow video 3; Pip review of 01-03 (issue #14).
**Watch out:** to-do `r20261117-youtube-production-01` (story 06) is still open though story 06 went public 11/19; tick it when checked. The publisher still has no thumbnail upload. Local clone `main` was 43 commits behind origin; pull before reading. A chat approval = `gh api -X POST repos/<repo>/actions/runs/<id>/pending_deployments` with `state=approved`, only on Katie's yes for that exact video.
**Branch/uncommitted:** wrap/2026-11-24-stories-07-08 -> PR into main · 0 uncommitted · 0 unpushed · runs to check: none

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
