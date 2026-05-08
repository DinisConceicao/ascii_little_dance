import sys
import traceback

try:
    from http.server import BaseHTTPRequestHandler, HTTPServer
    import os
    import json

    FRAME_DIR = "ascii_frames"
    
    print(f"CWD: {os.getcwd()}", flush=True)
    print(f"Files: {os.listdir('.')}", flush=True)

    def load_frames():
        files = sorted(os.listdir(FRAME_DIR))
        frames = []
        for f in files:
            with open(os.path.join(FRAME_DIR, f), "r") as file:
                frames.append(file.read())
        return frames

    FRAMES = load_frames()
    print(f"Loaded {len(FRAMES)} frames", flush=True)

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/ascii_frames":
                payload = json.dumps(FRAMES).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(payload)
            elif self.path.startswith("/ascii_frames/"):
                i = int(self.path.split("/")[-1])
                frame = FRAMES[i % len(FRAMES)]
                self.send_response(200)
                self.end_headers()
                self.wfile.write(frame.encode())
            elif self.path == "/dance.sh":
                with open("dance.sh", "r") as f:
                    script = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(script.encode())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Not found")

    PORT = int(os.environ.get("PORT", 8080))
    print(f"Starting server on port {PORT}", flush=True)
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()

except Exception as e:
    print(f"CRASH: {e}", flush=True)
    traceback.print_exc()
    sys.exit(1)