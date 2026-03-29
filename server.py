"""Minimal HTTP stub for Arga twin quickstart provisioning.

This serves as a placeholder app surface so the cluster deploy pipeline
has something to build and route to. The actual work is done by the twins.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok", "service": "arga-twin-stub"}).encode())

    def log_message(self, format, *args):
        pass  # suppress access logs


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), Handler)
    print("Twin stub listening on :8000")
    server.serve_forever()
