from http.server import BaseHTTPRequestHandler, HTTPServer
import os

FRAMES = sorted(os.listdir("ascii_frames"))

class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		path = self.path

		if path == "/dance":
			self.send_response(200)
			self.end_headers()
			self.wfile.write("\n".join(FRAMES).encode())

		elif path.startswith("/dance/"):
			idx = int(path.split("/")[-1])
			frame = FRAMES[idx % len(FRAMES)]

			self.send_response(200)
			self.end_headers()

			with open(f"ascii_frames/{frame}") as f:
				self.wfile.write(f.read().encode())

HTTPServer(("0.0.0.0", int(os.environ.get("PORT", 8080))), Handler)