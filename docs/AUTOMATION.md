# Automation: how it runs now

Implements `REBUILD_SPEC.md` on GitHub Actions + the direct YouTube Data API (no Postiz,
no Mac bridge, no auto-mode classifier at publish time).

**Split of work**
- **Produce** (script, Piper, Canva/Runway images, ffmpeg): the scheduled Claude routine, per
  `CLAUDE.md`. Canva is an MCP tool, so this step stays in Claude. Output: payload JSON
  committed to `channels/<ch>/posts/`, video uploaded to a GitHub Release tagged
  `post-<channel>-<NN>` as `video.mp4`.
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
2. Repo Settings > Secrets: `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`.
3. Repo Settings > Environments > new `publish-approval` > Required reviewers = you.
4. Tell the routine to dispatch instead of calling `postiz.py --yes`.

Tests: `python3 -m unittest discover -s tests -t .`
