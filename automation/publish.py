#!/usr/bin/env python3
"""Approval-gated publisher.

  publish.py check   POST VIDEO              validate + print approval summary/hash
  publish.py publish POST VIDEO --hash H     re-validate, require hash match, upload, verify

Exit codes: 0 ok, 2 rule violation, 3 hash mismatch (content changed after approval),
75 quota exhausted (retry next day), 76 needs a human, 1 other failure.
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

from automation import rules, youtube


def summary(p, video, h):
    return (f"channel: {p['channel']}\ntitle: {p['title']}\nprivacy: {p['privacy']}\n"
            f"madeForKids: {p['made_for_kids']}\ntags: {', '.join(p['tags'])}\n"
            f"video sha256: {rules.file_sha256(video)}\n--- description ---\n{p['description']}\n"
            f"--- approval hash ---\n{h}")


def write_result(post_path, p, result):
    """Record what actually went live so the routine and analytics can read it (no guessing)."""
    from datetime import datetime, timezone
    out = Path(post_path).with_suffix("").as_posix() + ".result.json"
    rec = {"channel": p["channel"], "title": p["title"], "privacy": p["privacy"],
           "publishedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"), **result}
    Path(out).write_text(json.dumps(rec, indent=2) + "\n")


def cmd_check(a):
    p = rules.load_post(a.post)
    errs = rules.validate(p)
    if errs:
        print("RULE VIOLATIONS:\n- " + "\n- ".join(errs), file=sys.stderr)
        return 2
    print(summary(p, a.video, rules.approval_hash(p, a.video)))
    return 0


def cmd_publish(a):
    p = rules.load_post(a.post)
    errs = rules.validate(p)
    if errs:
        print("RULE VIOLATIONS:\n- " + "\n- ".join(errs), file=sys.stderr)
        return 2
    if rules.approval_hash(p, a.video) != a.hash:
        print("content changed since approval; refusing to publish", file=sys.stderr)
        return 3
    token = youtube.access_token()
    for attempt in range(4):
        try:
            vid = youtube.upload(p, a.video, token)
            break
        except youtube.YouTubeError as e:
            print(f"upload failed ({e.kind}): {e}", file=sys.stderr)
            if e.kind == "defer":
                return 75
            if e.kind == "human":
                return 76
            if e.kind != "retry" or attempt == 3:
                return 1
            time.sleep(30 * 2 ** attempt)
    st = youtube.verify(vid, p, token)
    result = {"videoId": vid, "url": f"https://youtu.be/{vid}", "privacy": st["privacyStatus"],
              "uploadStatus": st.get("uploadStatus")}
    print(json.dumps(result))
    write_result(a.post, p, result)
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"video_id={vid}\n")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("check", "publish"):
        s = sub.add_parser(name)
        s.add_argument("post")
        s.add_argument("video")
    sub.choices["publish"].add_argument("--hash", required=True)
    a = ap.parse_args()
    sys.exit({"check": cmd_check, "publish": cmd_publish}[a.cmd](a))


if __name__ == "__main__":
    main()
