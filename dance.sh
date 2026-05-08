#!/bin/bash

while true; do
	for f in ascii_frames/*.txt; do
		clear
		cat "$f"
		sleep 0.02
	done
done