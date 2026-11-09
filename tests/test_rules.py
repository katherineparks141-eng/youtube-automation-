import copy
import json
import tempfile
import unittest
from pathlib import Path

from automation import rules
from automation.youtube import YouTubeError, build_body

ROOT = Path(__file__).resolve().parent.parent


class Rules(unittest.TestCase):
    def post(self, ch="sleepy-meadow-stories", n="03-sleepy-meadow-payload.json"):
        return rules.load_post(ROOT / "channels" / ch / "posts" / n)

    def test_existing_payloads_pass_or_report(self):
        for f in (ROOT / "channels").glob("*/posts/*-payload.json"):
            errs = rules.validate(rules.load_post(f))
            self.assertEqual([e for e in errs if "kids" in e or "allow-list" in e], [], f.name)

    def test_kids_flag_enforced(self):
        p = self.post(); p["made_for_kids"] = "no"
        self.assertTrue(any("MadeForKids" in e for e in rules.validate(p)))

    def test_ai_disclosure_required(self):
        p = self.post(); p["description"] = "hi #a #b #c"
        self.assertTrue(any("AI-disclosure" in e for e in rules.validate(p)))

    def test_unknown_destination_blocked(self):
        p = self.post(); p["integration"] = "other"
        self.assertTrue(any("allow-list" in e for e in rules.validate(p)))

    def test_hash_binds_content(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4") as v:
            v.write(b"x"); v.flush()
            p = self.post(); h = rules.approval_hash(p, v.name)
            q = copy.deepcopy(p); q["title"] += "!"
            self.assertNotEqual(h, rules.approval_hash(q, v.name))
            v.write(b"y"); v.flush()
            self.assertNotEqual(h, rules.approval_hash(p, v.name))

    def test_error_classes(self):
        self.assertEqual(YouTubeError("quotaExceeded", "", 403).kind, "defer")
        self.assertEqual(YouTubeError("uploadLimitExceeded", "", 400).kind, "human")
        self.assertEqual(YouTubeError("userRateLimitExceeded", "", 403).kind, "retry")
        self.assertEqual(YouTubeError("forbidden", "", 403).kind, "fatal")

    def test_body_declares_synthetic_and_kids(self):
        b = build_body(self.post())
        self.assertTrue(b["status"]["containsSyntheticMedia"])
        self.assertTrue(b["status"]["selfDeclaredMadeForKids"])


if __name__ == "__main__":
    unittest.main()
