#!/usr/bin/env python3
"""Generate narration audio from a script text file using free, offline Piper TTS.

Usage:
    python3 generate_narration.py SCRIPT.txt OUTPUT.wav [--voice lessac|amy] [--speed 1.0]

Voices (see pipeline/setup_tts_voices.sh to download them first):
    lessac -> en_US-lessac-medium  (Forgotten & Found — calm, measured male)
    amy    -> en_US-amy-medium    (Sleepy Meadow Stories — warm female)

A length-scale around 1.08-1.12 (i.e. --speed 1.08) slows the default pace slightly for
a calmer narration cadence; 1.0 is Piper's natural speed.
"""
import argparse
import subprocess
import sys
from pathlib import Path

VOICES = {
    "lessac": "en_US-lessac-medium.onnx",
    "amy": "en_US-amy-medium.onnx",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--voice", choices=VOICES, default="lessac")
    ap.add_argument("--speed", type=float, default=1.10,
                     help="Piper length-scale; >1.0 slows the pace (default 1.10)")
    args = ap.parse_args()

    model = Path(__file__).resolve().parent.parent / "piper_voices" / VOICES[args.voice]
    if not model.exists():
        sys.exit(f"Voice model missing: {model}\nRun pipeline/setup_tts_voices.sh first.")

    text = args.script.read_text()
    subprocess.run(
        ["python3", "-m", "piper", "-m", str(model), "-f", str(args.output),
         "--length-scale", str(args.speed)],
        input=text, text=True, check=True,
    )
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
