from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import time

FRAMES_DIR = "ascii_frames"
frames = sorted(os.listdir(FRAMES_DIR))

class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/plain")
		self.end_headers()

		while True:
			for f in frames:
				with open(f"{FRAMES_DIR}/{f}", "r") as file:
					self.wfile.write(b"\033[2J\033[H")
					self.wfile.write(file.read().encode())
					self.wfile.flush()
				time.sleep(0.05)

HTTPServer(("0.0.0.0", int(os.environ.get("PORT", 8080))), Handler).serve_forever()