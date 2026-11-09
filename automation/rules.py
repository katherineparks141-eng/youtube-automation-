"""Hard rules from CLAUDE.md enforced in code. Pure functions, no network."""
import hashlib
import json
import re
from pathlib import Path

# Hard rule 2: made-for-kids is declared per channel, never defaulted.
MADE_FOR_KIDS = {"forgotten-and-found": "no", "sleepy-meadow-stories": "yes"}
# Hard rule 8: only these destinations. Add a channel only when Katie names it.
ALLOWED_INTEGRATIONS = {"cmvy6plen09q6nk0750rg2fha"}
AI_DISCLOSURE = re.compile(r"\bAI[- ](narration|generated|voice)", re.I)
HASHTAG = re.compile(r"(?<!\w)#\w+")
SOURCES = re.compile(r"\bsources?\b\s*:", re.I)
ADVICE = re.compile(r"\b(medical|legal|financial|investment) advice\b", re.I)


class RuleError(Exception):
    pass


def channel_of(post_path):
    return Path(post_path).resolve().parent.parent.name


def load_post(post_path):
    """Flatten a Postiz-format payload into the fields that matter."""
    raw = json.loads(Path(post_path).read_text())
    post = raw["posts"][0]
    s = post["settings"]
    return {
        "channel": channel_of(post_path),
        "integration": post["integration"]["id"],
        "title": s["title"],
        "description": post["value"][0]["content"],
        "privacy": s["type"],
        "made_for_kids": s["selfDeclaredMadeForKids"],
        "tags": [t["value"] for t in s.get("tags", [])],
    }


def validate(p):
    """Return a list of violations (empty = ok)."""
    e = []
    ch = p["channel"]
    if ch not in MADE_FOR_KIDS:
        e.append(f"unknown channel '{ch}'")
    elif p["made_for_kids"] != MADE_FOR_KIDS[ch]:
        e.append(f"selfDeclaredMadeForKids must be '{MADE_FOR_KIDS[ch]}' for {ch}")
    if p["integration"] not in ALLOWED_INTEGRATIONS:
        e.append("destination channel not on the allow-list")
    if not AI_DISCLOSURE.search(p["description"]):
        e.append("description missing AI-disclosure line")
    if ch == "forgotten-and-found" and not SOURCES.search(p["description"]):
        e.append("history video must cite sources ('Sources:') in description")
    if ADVICE.search(p["description"]):
        e.append("description frames content as credentialed advice")
    if len(p["title"]) > 100:
        e.append("title over 100 chars")
    tags = HASHTAG.findall(p["description"])
    if not 3 <= len(tags) <= 15:
        e.append(f"need 3-15 hashtags in description, found {len(tags)}")
    if len(HASHTAG.findall(p["title"])) > 2:
        e.append("more than 2 hashtags in title")
    if len(",".join(p["tags"])) > 500:
        e.append("tags over 500 chars")
    if p["privacy"] not in ("public", "unlisted", "private"):
        e.append("bad privacy value")
    return e


def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def approval_hash(p, video_path):
    """Binds an approval to the exact title/description/privacy/kids/tags/video."""
    body = {k: p[k] for k in ("channel", "title", "description", "privacy", "made_for_kids", "tags")}
    body["video_sha256"] = file_sha256(video_path)
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
