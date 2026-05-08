from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import time

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
		if self.path == "/passinho":
			output = "\n".join(FRAMES)
			self.send_response(200)
			self.send_header("Content-type", "text/plain")
			self.end_headers()
			self.wfile.write(output.encode())
		else:
			self.send_response(404)
			self.end_headers()
			self.wfile.write(b"Not found")

PORT = int(os.environ.get("PORT", 8080))
HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()