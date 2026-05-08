from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import time
import json

FRAME_DIR = "ascii_frames"

def load_frames():
	files = sorted(os.listdir(FRAME_DIR))
	frames = []
	for f in files:
		with open(os.path.join(FRAME_DIR, f), "r") as file:
			frames.append(file.read())
	return frames

FRAMES = load_frames()

class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path == "/ascii_frames":
			payload = json.dumps(FRAMES).encode()
			self.send_response(200)
			self.send_header("Content-Type", "application/json")
			self.send_header("Access-Control-Allow-Origin", "*")
			self.end_headers()
			self.wfile.write(payload)

		elif self.path.startswith("/frame/"):
			i = int(self.path.split("/")[-1])
			frame = FRAMES[i % len(FRAMES)]
			self.send_response(200)
			self.end_headers()
			self.wfile.write(frame.encode())

		else:
			self.send_response(404)
			self.end_headers()
			self.wfile.write(b"Not found")