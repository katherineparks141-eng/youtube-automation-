#!/usr/bin/env bash
# Fetch a staged video from the PRIVATE media repo into media/video.mp4.
# Usage: automation/fetch_video.sh <tag>   (needs GH_TOKEN with read access to the media repo)
# New flow: the routine commits staged/<tag>/video.mp4 (cloud sessions can't create releases).
# Old flow: a release <tag> with asset video.mp4. Tried second so older tags still work.
set -euo pipefail
tag="$1"
repo="katherineparks141-eng/youtube-automation-media"
case "$tag" in *[!A-Za-z0-9._-]*|"") echo "bad tag: $tag" >&2; exit 2;; esac
mkdir -p media
if gh api "repos/$repo/contents/staged/$tag/video.mp4" -H "Accept: application/vnd.github.raw" > media/video.mp4 2>/dev/null; then
  echo "Fetched staged/$tag/video.mp4"
else
  rm -f media/video.mp4
  gh release download "$tag" -p video.mp4 -D media --repo "$repo"
  echo "Fetched release $tag"
fi
test -s media/video.mp4
