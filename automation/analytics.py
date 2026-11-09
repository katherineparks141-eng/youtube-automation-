#!/usr/bin/env python3
"""Pull real stats for every published video into data/youtube-analytics.json. Never estimates."""
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from automation import youtube

ROOT = Path(__file__).resolve().parent.parent


def published():
    out = []
    for f in sorted(ROOT.glob("channels/*/posts/*.result.json")):
        r = json.loads(f.read_text())
        if r.get("videoId"):
            out.append(r)
    return out


def _get(path, params, token):
    req = urllib.request.Request(f"https://www.googleapis.com/youtube/v3/{path}?{urllib.parse.urlencode(params)}",
                                 headers={"Authorization": f"Bearer {token}"})
    _, _, body = youtube._call(req)
    return json.loads(body)


def build(videos, video_stats, channel):
    per = []
    for v in videos:
        s = video_stats.get(v["videoId"])
        per.append({"title": v["title"], "channel": v["channel"], "videoId": v["videoId"],
                    "privacy": v["privacy"],
                    "views": int(s["viewCount"]) if s else None,
                    "likes": int(s["likeCount"]) if s and "likeCount" in s else None,
                    "comments": int(s["commentCount"]) if s and "commentCount" in s else None})
    cs = channel or {}
    return {"lastRefreshed": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "channel": {"subscribers": None if cs.get("hiddenSubscriberCount") or "subscriberCount" not in cs else int(cs["subscriberCount"]),
                        "totalViews": int(cs["viewCount"]) if "viewCount" in cs else None,
                        "videoCount": int(cs["videoCount"]) if "videoCount" in cs else None},
            "perVideo": per,
            "spendUsd": 0, "revenueUsd": 0, "monetized": False,
            "note": "null = no data. Spend/revenue are not measured here."}


def main():
    vids = published()
    token = youtube.access_token()
    stats = {}
    for i in range(0, len(vids), 50):
        chunk = [v["videoId"] for v in vids[i:i + 50]]
        for it in _get("videos", {"part": "statistics", "id": ",".join(chunk)}, token).get("items", []):
            stats[it["id"]] = it["statistics"]
    ch = _get("channels", {"part": "statistics", "mine": "true"}, token).get("items", [])
    data = build(vids, stats, ch[0]["statistics"] if ch else None)
    out = ROOT / "data" / "youtube-analytics.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(data, indent=2) + "\n")
    print(f"wrote {out} ({len(vids)} videos)")


if __name__ == "__main__":
    sys.exit(main())
