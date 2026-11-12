#!/usr/bin/env python3
"""
ZStore Print Server for Windows -> Xprinter XP-365B.
Listens on http://127.0.0.1:9998 and http://127.0.0.1:8080.
Renders Ukrainian Cyrillic text via Pillow into TSPL BITMAP.
Splits multi-label batches into individual jobs to ensure zero drift.

Prerequisites:
  pip install pillow pywin32
"""

import json
import os
import re
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from PIL import Image, ImageDraw, ImageFont

# Назва принтера у "Пристрої та принтери" Windows (наприклад XP-365B або Xprinter XP-365B)
PRINTER_NAME = "XP-365B"

FONT_PATH = "C:\\Windows\\Fonts\\arial.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "C:\\Windows\\Fonts\\tahoma.ttf"

def has_cyrillic(text):
    return bool(re.search(r'[\u0400-\u04FF]', text))

def render_text_to_bitmap_cmd(line1, line2, y=0, font_size=16):
    width = 240
    height = 34
    width_bytes = width // 8

    img = Image.new('1', (width, height), color=1)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except Exception:
        font = ImageFont.load_default()

    bbox1 = font.getbbox(line1) if line1 else (0, 0, 0, 0)
    w1 = bbox1[2] - bbox1[0]
    x1 = max(6, (width - w1) // 2)

    bbox2 = font.getbbox(line2) if line2 else (0, 0, 0, 0)
    w2 = bbox2[2] - bbox2[0]
    x2 = max(6, (width - w2) // 2)

    top_offset = bbox1[1] if bbox1 else 0
    draw.text((x1, -top_offset), line1, font=font, fill=0)
    if line2:
        draw.text((x2, -top_offset + 16), line2, font=font, fill=0)

    raw_bytes = bytearray()
    for row in range(height):
        row_byte = 0
        bit_count = 0
        for col in range(width):
            pixel = img.getpixel((col, row))
            bit = 0 if pixel == 0 else 1
            row_byte = (row_byte << 1) | bit
            bit_count += 1
            if bit_count == 8:
                raw_bytes.append(row_byte)
                row_byte = 0
                bit_count = 0

    cmd = f"BITMAP 0,{y},{width_bytes},{height},0,".encode('ascii') + bytes(raw_bytes) + b"\n"
    return cmd

def process_tspl(data_bytes):
    text = ""
    used_cp = "cp866"
    for cp in ["cp866", "cp1251", "utf-8"]:
        try:
            candidate = data_bytes.decode(cp)
            if has_cyrillic(candidate):
                text = candidate
                used_cp = cp
                break
        except Exception:
            pass

    if not text:
        try:
            text = data_bytes.decode("cp866", errors="ignore")
        except Exception:
            return data_bytes

    labels = re.split(r'(?i)PRINT\s+\d+,\d+', text)
    result_bytes = bytearray()

    for l in labels:
        if not l.strip():
            continue

        text_matches = list(re.finditer(r'TEXT\s+([^,]+),([^,]+),\"([^\"]+)\",0,(\d+),(\d+),\"([^\"]+)\"', l))
        has_ukr = any(has_cyrillic(m.group(6)) for m in text_matches)

        if has_ukr:
            line1 = ""
            line2 = ""
            lines = [row.strip() for row in l.split('\n') if row.strip()]
            name_count = 0
            for row in lines:
                m = re.match(r'TEXT\s+[^,]+,[^,]+,\"[12]\",0,\d+,\d+,\"([^\"]+)\"', row)
                if m and name_count < 2:
                    if name_count == 0:
                        line1 = m.group(1)
                    else:
                        line2 = m.group(1)
                    name_count += 1

            bitmap_cmd = render_text_to_bitmap_cmd(line1, line2, y=0, font_size=16)
            
            rebuilt_header = b"""SIZE 30 mm, 20 mm
GAP 5.3 mm, 0 mm
SPEED 4
DENSITY 8
SHIFT -8
DIRECTION 0
CLS
"""
            rebuilt_rest = []
            m_bar = re.search(r'BARCODE\s+.*?\"([^\"]+)\"\s*$', l, re.MULTILINE)
            if m_bar:
                code = m_bar.group(1)
                est_modules = 35 + len(code) * 11
                bar_w = est_modules * 2
                bar_x = max(15, (240 - bar_w) // 2)
                rebuilt_rest.append(f'BARCODE {bar_x},36,"128",38,0,0,2,2,"{code}"')

            m_shop = re.search(r'TEXT\s+.*?\"#\s*([^\"]+)\"', l)
            if m_shop:
                code = m_shop.group(1)
                text_val = f"# {code}"
                text_x = max(10, (240 - len(text_val) * 16) // 2)
                rebuilt_rest.append(f'TEXT {text_x},78,"4",0,1,1,"{text_val}"')

            rebuilt_body = ('\n'.join(rebuilt_rest) + "\nPRINT 1,1\n").encode(used_cp, errors='replace')
            result_bytes.extend(rebuilt_header + bitmap_cmd + rebuilt_body)
        else:
            cleaned_l = l.strip() + "\nPRINT 1,1\n"
            result_bytes.extend(cleaned_l.encode(used_cp, errors='replace'))

    return bytes(result_bytes) if result_bytes else data_bytes

def send_to_windows_printer(printer_name, data):
    import win32print
    hPrinter = win32print.OpenPrinter(printer_name)
    try:
        hJob = win32print.StartDocPrinter(hPrinter, 1, ("ZStore_Label", None, "RAW"))
        try:
            win32print.StartPagePrinter(hPrinter)
            win32print.WritePrinter(hPrinter, data)
            win32print.EndPagePrinter(hPrinter)
        finally:
            win32print.EndDocPrinter(hPrinter)
    finally:
        win32print.ClosePrinter(hPrinter)

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
        self.wfile.write(b"ZStore Print Server for Windows (XP-365B) is running.")

    def do_POST(self):
        if self.path.rstrip("/") != "/print":
            self.send_response(404)
            self._set_cors_headers()
            self.end_headers()
            return

        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)

        try:
            data_bytes = None
            try:
                parsed = json.loads(raw_body.decode("utf-8", errors="ignore"))
                if isinstance(parsed, list):
                    data_bytes = bytes(parsed)
                elif isinstance(parsed, str):
                    try:
                        inner = json.loads(parsed)
                        if isinstance(inner, list):
                            data_bytes = bytes(inner)
                    except Exception:
                        data_bytes = parsed.encode("cp866", errors="replace")
            except Exception:
                pass

            if data_bytes is None:
                data_bytes = raw_body

            data_bytes = process_tspl(data_bytes)

            # Split into individual label jobs so printer aligns gap on every label!
            raw_labels = re.split(b'(?i)PRINT\\s+\\d+,\\d+', data_bytes)
            job_chunks = []
            for chunk in raw_labels:
                if chunk.strip():
                    job_chunks.append(chunk.strip() + b"\nPRINT 1,1\n")

            if not job_chunks:
                job_chunks = [data_bytes]

            for chunk in job_chunks:
                send_to_windows_printer(PRINTER_NAME, chunk)

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
        pass

def serve(port):
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, PrintHandler)
    httpd.serve_forever()

def run():
    print(f"Starting ZStore Windows Print Server on ports 9998 and 8080 (Printer: {PRINTER_NAME})...")
    t1 = threading.Thread(target=serve, args=(9998,), daemon=True)
    t2 = threading.Thread(target=serve, args=(8080,), daemon=True)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == "__main__":
    run()
