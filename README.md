# YouTube Automation

Fully-automated, zero-filming YouTube production for Katie's two test channels:
**Forgotten & Found** (history/folklore) and **Sleepy Meadow Stories** (kids' bedtime
stories).

**Start here → [CLAUDE.md](./CLAUDE.md)** — the operating rules every session follows:
hard rules (approval gating, compliance, no copyrighted IP), cadence target, the full
production pipeline (script → free narration → Canva visuals → ffmpeg assembly →
Postiz publish), and packaging/promotion guidance.

Full strategy and research lives in the "Business Ideas Playbook" Claude Doc (Ideas 8
and 9): https://claude.ai/artifact/fb773ed3-b385-41b6-8489-a1b4d5704920

## Layout

- `CLAUDE.md` — operating rules (read this first)
- `pipeline/` — reusable scripts (TTS voice setup, narration generation, video assembly)
- `channels/forgotten-and-found/` — scripts, posted payloads, channel identity notes
- `channels/sleepy-meadow-stories/` — same, for the kids channel
- `research/` — dated research notes (cadence, CTR, hashtags, trends, promotion)

Posting itself runs through the shared, approval-gated script at
`~/katie-hq/shared/postiz.py` (not duplicated in this repo — see CLAUDE.md for why).
