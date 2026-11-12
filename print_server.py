#!/usr/bin/env python3
"""
Simple local print server for ZStore -> Xprinter XP-365B on macOS.
Listens on http://127.0.0.1:9998/print and pipes raw TSPL commands to CUPS.
"""

import json
import subprocess
import tempfile
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

PRINTER_NAME = "XP365B"
PORT = 9998

class PrintHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Private-Network", "true")

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self._set_cors_headers()
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"ZStore Print Server for XP-365B is running.")

    def do_POST(self):
        if self.path.rstrip("/") != "/print":
            self.send_response(404)
            self._set_cors_headers()
            self.end_headers()
            return

        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)

        try:
            # Body may be JSON array of byte integers: [67, 76, 83, ...]
            # or JSON string or raw text
            data_bytes = None
            try:
                parsed = json.loads(raw_body.decode("utf-8", errors="ignore"))
                if isinstance(parsed, list):
                    # List of integers
                    data_bytes = bytes(parsed)
                elif isinstance(parsed, str):
                    try:
                        inner = json.loads(parsed)
                        if isinstance(inner, list):
                            data_bytes = bytes(inner)
                    except Exception:
                        data_bytes = parsed.encode("cp1251", errors="replace")
            except Exception:
                pass

            if data_bytes is None:
                data_bytes = raw_body

            # Write to temporary file and send to printer via lpr -o raw
            with tempfile.NamedTemporaryFile(delete=False) as tf:
                tf.write(data_bytes)
                tmp_path = tf.name

            try:
                cmd = ["lpr", "-P", PRINTER_NAME, "-o", "raw", tmp_path]
                proc = subprocess.run(cmd, capture_output=True, text=True)
                if proc.returncode != 0:
                    raise Exception(proc.stderr or "Error printing via lpr")
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", "0")
            self.end_headers()

        except Exception as e:
            err_msg = str(e).encode("utf-8")
            self.send_response(500)
            self._set_cors_headers()
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(err_msg)))
            self.end_headers()
            self.wfile.write(err_msg)

    def log_message(self, format, *args):
        # Concise logging
        print(f"[PrintServer] {self.address_string()} - {format % args}")

def run():
    server_address = ("127.0.0.1", PORT)
    httpd = HTTPServer(server_address, PrintHandler)
    print(f"Print server listening on http://127.0.0.1:{PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
