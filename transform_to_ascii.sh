#!/bin/bash

rm -f ascii_frames/*.txt

mkdir -p ascii_frames

# for f in frames/*.png; do
# 	chafa "$f" \
# 		--format symbols \
# 		--size 60x30 \
# 		--symbols ascii \
# 		--colors none \
# 		> "ascii_frames/$(basename "$f" .png).txt"
# done

for f in frames/*.png; do
	jp2a --width=40 "$f" \
		> "ascii_frames/$(basename "$f" .png).txt"
done