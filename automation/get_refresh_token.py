#!/usr/bin/env python3
"""One-time: authorize the YouTube channel and store the refresh token as a GitHub secret.

Run it yourself in a terminal (never paste secrets into chat):

    export YT_CLIENT_ID=...        # from Google Cloud OAuth client (Desktop app)
    export YT_CLIENT_SECRET=...
    python3 -m automation.get_refresh_token

It opens a browser, you sign in as the channel owner and approve, then it sets the
YT_CLIENT_ID / YT_CLIENT_SECRET / YT_REFRESH_TOKEN repo secrets with `gh secret set`.
Nothing is printed or written to disk.
"""
import http.server
import json
import os
import secrets
import subprocess
import sys
import urllib.parse
import urllib.request
import webbrowser

SCOPE = "https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube.readonly"
REPO = "katherineparks141-eng/youtube-automation-"


def main():
    cid, csec = os.environ.get("YT_CLIENT_ID"), os.environ.get("YT_CLIENT_SECRET")
    if not (cid and csec):
        sys.exit("Set YT_CLIENT_ID and YT_CLIENT_SECRET first.")
    state, got = secrets.token_urlsafe(16), {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            got.update({k: v[0] for k, v in q.items()})
            self.send_response(200); self.end_headers()
            self.wfile.write(b"Done. You can close this tab.")
        def log_message(self, *a): pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    redirect = f"http://127.0.0.1:{srv.server_port}"
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": cid, "redirect_uri": redirect, "response_type": "code",
        "scope": SCOPE, "access_type": "offline", "prompt": "consent", "state": state})
    print("Opening browser. Sign in as the owner of the 'Katie Tuell' YouTube channel.")
    webbrowser.open(url)
    srv.handle_request()
    if got.get("state") != state or "code" not in got:
        sys.exit("Authorization failed or state mismatch.")
    data = urllib.parse.urlencode({
        "code": got["code"], "client_id": cid, "client_secret": csec,
        "redirect_uri": redirect, "grant_type": "authorization_code"}).encode()
    with urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=data)) as r:
        tok = json.load(r)
    if "refresh_token" not in tok:
        sys.exit("No refresh token returned. Revoke the app at myaccount.google.com/permissions and retry.")
    for name, val in (("YT_CLIENT_ID", cid), ("YT_CLIENT_SECRET", csec), ("YT_REFRESH_TOKEN", tok["refresh_token"])):
        subprocess.run(["gh", "secret", "set", name, "--repo", REPO], input=val.encode(), check=True)
    print("Secrets set: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN")


if __name__ == "__main__":
    main()
