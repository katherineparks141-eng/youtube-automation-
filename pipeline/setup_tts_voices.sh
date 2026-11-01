#!/usr/bin/env bash
# Free, offline TTS setup — Piper. Run once per environment.
# No API key, no per-generation cost.
set -euo pipefail

pip install --break-system-packages piper-tts

mkdir -p piper_voices
cd piper_voices
BASE="https://huggingface.co/rhasspy/piper-voices/resolve/main"

# Forgotten & Found narrator — calm, measured male voice
curl -sS -L -o en_US-lessac-medium.onnx "$BASE/en/en_US/lessac/medium/en_US-lessac-medium.onnx"
curl -sS -L -o en_US-lessac-medium.onnx.json "$BASE/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"

# Sleepy Meadow Stories narrator — warm female voice
curl -sS -L -o en_US-amy-medium.onnx "$BASE/en/en_US/amy/medium/en_US-amy-medium.onnx"
curl -sS -L -o en_US-amy-medium.onnx.json "$BASE/en/en_US/amy/medium/en_US-amy-medium.onnx.json"

echo "Voices ready in piper_voices/. Generate narration with pipeline/generate_narration.py"
