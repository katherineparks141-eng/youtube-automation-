"""Direct YouTube Data API v3 upload (own Google Cloud project, own quota). Stdlib only."""
import json
import os
import urllib.error
import urllib.parse
import urllib.request

CATEGORY = {"forgotten-and-found": "27", "sleepy-meadow-stories": "24"}  # Education / Entertainment

# Retry class per YouTube error reason. Different failures need different handling.
DEFER_TO_NEXT_DAY = {"quotaExceeded", "dailyLimitExceeded"}   # project quota; resets midnight Pacific
CHANNEL_LIMIT = {"uploadLimitExceeded"}                        # channel-level; human must look
SHORT_THROTTLE = {"uploadRateLimitExceeded", "userRateLimitExceeded", "rateLimitExceeded"}


class YouTubeError(Exception):
    def __init__(self, reason, message, status=None):
        super().__init__(f"{reason}: {message}")
        self.reason, self.status = reason, status

    @property
    def kind(self):
        if self.reason in DEFER_TO_NEXT_DAY:
            return "defer"
        if self.reason in CHANNEL_LIMIT:
            return "human"
        if self.reason in SHORT_THROTTLE or (self.status or 0) >= 500:
            return "retry"
        return "fatal"


def _reason(err):
    body = err.read().decode(errors="replace")
    try:
        j = json.loads(body)["error"]
        return j["errors"][0].get("reason", "unknown"), j.get("message", body), err.code
    except Exception:
        return "unknown", body[:300], err.code


def _call(req):
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as err:
        raise YouTubeError(*_reason(err)[:2], status=err.code)


def access_token():
    data = urllib.parse.urlencode({
        "client_id": os.environ["YT_CLIENT_ID"],
        "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ["YT_REFRESH_TOKEN"],
        "grant_type": "refresh_token",
    }).encode()
    _, _, body = _call(urllib.request.Request("https://oauth2.googleapis.com/token", data=data))
    return json.loads(body)["access_token"]


def build_body(p):
    return {
        "snippet": {
            "title": p["title"],
            "description": p["description"],
            "tags": p["tags"],
            "categoryId": CATEGORY[p["channel"]],
        },
        "status": {
            "privacyStatus": p["privacy"],
            "selfDeclaredMadeForKids": p["made_for_kids"] == "yes",
            "containsSyntheticMedia": True,  # AI disclosure, also set in-API
        },
    }


def upload(p, video_path, token):
    """Resumable upload; returns the new video id. Costs ~1600 quota units."""
    size = os.path.getsize(video_path)
    init = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
        data=json.dumps(build_body(p)).encode(), method="POST",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json",
                 "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)})
    _, headers, _ = _call(init)
    loc = {k.lower(): v for k, v in headers.items()}["location"]
    with open(video_path, "rb") as f:
        put = urllib.request.Request(loc, data=f.read(), method="PUT",
                                     headers={"Content-Type": "video/mp4", "Content-Length": str(size)})
        _, _, body = _call(put)
    return json.loads(body)["id"]


def verify(video_id, p, token):
    """Independently re-read the video; never trust the upload response alone."""
    q = urllib.parse.urlencode({"part": "status,snippet", "id": video_id})
    req = urllib.request.Request(f"https://www.googleapis.com/youtube/v3/videos?{q}",
                                 headers={"Authorization": f"Bearer {token}"})
    _, _, body = _call(req)
    items = json.loads(body).get("items", [])
    if not items:
        raise YouTubeError("notFound", f"video {video_id} not readable after upload")
    st, sn = items[0]["status"], items[0]["snippet"]
    bad = []
    if sn["title"] != p["title"]:
        bad.append("title")
    if st["privacyStatus"] != p["privacy"]:
        bad.append("privacy")
    if st.get("selfDeclaredMadeForKids") != (p["made_for_kids"] == "yes"):
        bad.append("madeForKids")
    if bad:
        raise YouTubeError("verifyMismatch", "live video differs on: " + ", ".join(bad))
    return st
