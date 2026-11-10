# Automation: how it runs now

Implements `REBUILD_SPEC.md` on GitHub Actions + the direct YouTube Data API (no Postiz,
no Mac bridge, no auto-mode classifier at publish time).

**Split of work**
- **Produce** (script, Piper, Canva/Runway images, ffmpeg): the scheduled Claude routine, per
  `CLAUDE.md`. Canva is an MCP tool, so this step stays in Claude. Output: payload JSON
  committed to `channels/<ch>/posts/`, video committed to the private media repo as
  `staged/post-<channel>-<NN>/video.mp4`.
- **Approve + publish**: `.github/workflows/publish.yml`. Routine dispatches it
  (`gh workflow run publish.yml -f post=<payload> -f tag=<tag>`). Job 1 prints exactly what
  would go live. Job 2 waits on the `publish-approval` environment (Katie approves in
  GitHub web or mobile), re-checks the content hash, uploads, then re-reads the live video
  to verify title/privacy/made-for-kids.

**Enforced in code** (`automation/rules.py`, tested): made-for-kids per channel, AI
disclosure, sources for history, no credentialed-advice wording, hashtag limits, destination
allow-list. The API call also sets `containsSyntheticMedia`.

**Failure handling** (`automation/youtube.py`): `quotaExceeded` -> exit 75, issue opened, retry
after midnight Pacific. `uploadLimitExceeded` -> human. Rate throttles -> backoff retry.

## One-time setup (Katie)
1. Google Cloud: new project, enable YouTube Data API v3, OAuth client, authorize the
   channel once to get a refresh token. File the quota extension audit if usage nears 6
   uploads/day.
2. Run `python3 -m automation.get_refresh_token` (needs YT_CLIENT_ID/YT_CLIENT_SECRET exported); it sets all three repo secrets.
3. Repo Settings > Environments > new `publish-approval` > Required reviewers = you.
4. Tell the routine to dispatch instead of calling `postiz.py --yes`.

Tests: `python3 -m unittest discover -s tests -t .`

## Approval gate (important)
Required reviewers on environments are not available for private repos on GitHub Free.
Until the `publish-approval` environment really has you as a required reviewer, the publish job
refuses to run (fails closed). Once it does, set repo variable `APPROVAL_GATE_CONFIRMED=true`.
Options: GitHub Pro/Team (paid, needs Katie's dollar yes) or make the repo public.

## Private media
Videos live in the private repo `katherineparks141-eng/youtube-automation-media`
(never this public repo). The publisher reads them with secret `MEDIA_TOKEN`: a fine-grained
personal access token limited to that one repo, permission Contents: read-only. Create it at
github.com/settings/personal-access-tokens/new, then run (it prompts, hidden):
`gh secret set MEDIA_TOKEN --repo katherineparks141-eng/youtube-automation-`
Routine upload: commit `staged/post-<ch>-<NN>/video.mp4` to that repo and push (under 95 MB; GitHub's hard limit is 100 MB).
Cloud routine sessions get HTTP 403 on creating releases, so releases are no longer used for new
videos. `automation/fetch_video.sh` reads the staged file and falls back to a release for old tags.

## How the routine and the code talk
- Routine -> code: commits the payload, uploads `video.mp4` to the private media repo, starts `publish.yml`.
- Code -> routine: `publish.yml` commits `<payload>.result.json` (video id, URL, time) after a verified upload; `analytics.yml` commits `data/youtube-analytics.json` daily. The routine reads both from the repo. Failures open a GitHub issue.
