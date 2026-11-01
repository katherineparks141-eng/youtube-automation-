#!/usr/bin/env bash
# Assemble a Ken-Burns-style video from a folder of stills + one narration track.
# No paid tools — ffmpeg only.
#
# Usage: assemble_video.sh IMAGES_DIR NARRATION.wav OUTPUT.mp4
#
# IMAGES_DIR should contain numbered PNGs (01_*.png, 02_*.png, ...) in the order they
# should appear. Duration is split evenly across the images to match the narration's
# total length.

set -euo pipefail
IMAGES_DIR="$1"
NARRATION="$2"
OUTPUT="$3"
WORKDIR=$(mktemp -d)
trap 'rm -rf "$WORKDIR"' EXIT

TOTAL_DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$NARRATION")
IMAGES=("$IMAGES_DIR"/*.png)
N=${#IMAGES[@]}
PER_IMAGE=$(python3 -c "print($TOTAL_DUR / $N)")

i=0
CONCAT_LIST="$WORKDIR/concat.txt"
: > "$CONCAT_LIST"
for img in "${IMAGES[@]}"; do
  i=$((i + 1))
  clip="$WORKDIR/clip_$i.mp4"
  frames=$(python3 -c "print(int($PER_IMAGE * 25))")
  ffmpeg -y -loop 1 -i "$img" -t "$PER_IMAGE" -vf \
    "scale=2200:-1,zoompan=z='min(zoom+0.0008,1.15)':d=$frames:s=1920x1080:fps=25,format=yuv420p" \
    -c:v libx264 -preset veryfast -crf 20 "$clip" -loglevel error
  echo "file '$clip'" >> "$CONCAT_LIST"
done

SILENT="$WORKDIR/silent.mp4"
ffmpeg -y -f concat -safe 0 -i "$CONCAT_LIST" -c copy "$SILENT" -loglevel error
ffmpeg -y -i "$SILENT" -i "$NARRATION" -c:v copy -c:a aac -b:a 192k -shortest "$OUTPUT" -loglevel error

echo "Wrote $OUTPUT ($(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUTPUT")s)"
