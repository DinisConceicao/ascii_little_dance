#!/bin/bash

URL="${1:-https://ascii-little-dance.onrender.com}"
FPS="${2:-15}"
DELAY=$(echo "scale=3; 1/$FPS" | bc)

echo "Loading animation..."
FRAMES_JSON=$(curl -sf "$URL/ascii_frames")

if [ -z "$FRAMES_JSON" ]; then
	echo "Failed to load frames from $URL/ascii_frames"
	exit 1
fi

mapfile -t FRAMES < <(python3 -c "
import json, sys
frames = json.loads(sys.stdin.read())
for f in frames:
	print(f)
	print('---FRAME_END---')
" <<< "$FRAMES_JSON")

declare -a ANIM_FRAMES
current=""
for line in "${FRAMES[@]}"; do
	if [ "$line" = "---FRAME_END---" ]; then
		ANIM_FRAMES+=("$current")
		current=""
	else
		current+="$line"$'\n'
	fi
done

echo "Loaded ${#ANIM_FRAMES[@]} frames. Press Ctrl+C to stop."
sleep 1

tput civis  # hide cursor
trap 'tput cnorm; echo; exit' INT

while true; do
	for frame in "${ANIM_FRAMES[@]}"; do
		clear
		printf "%s" "$frame"
		sleep "$DELAY"
	done
done