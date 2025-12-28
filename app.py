from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import uuid
from generate_qrcode import generate_qrcode

ROOT = os.path.dirname(__file__)

class QRHandler(BaseHTTPRequestHandler):
    def _send_file(self, path, content_type):
        try:
            with open(path, 'rb') as f:
                data = f.read()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except FileNotFoundError:
            self.send_error(404)

    def do_GET(self):
        if self.path == '/' or self.path.startswith('/index.html'):
            self._send_file(os.path.join(ROOT, 'index.html'), 'text/html; charset=utf-8')
            return

        if self.path.startswith('/static/'):
            rel = self.path.lstrip('/')
            safe = os.path.normpath(rel)
            if not safe.startswith('static/'):
                self.send_error(403)
                return
            full = os.path.join(ROOT, safe)
            ctype = 'text/plain'
            if full.endswith('.css'):
                ctype = 'text/css; charset=utf-8'
            elif full.endswith('.js'):
                ctype = 'application/javascript; charset=utf-8'
            elif full.endswith('.png'):
                ctype = 'image/png'
            self._send_file(full, ctype)
            return

        if self.path.startswith('/generated/'):
            rel = self.path.lstrip('/')
            safe = os.path.normpath(rel)
            if not safe.startswith('generated/'):
                self.send_error(403)
                return
            full = os.path.join(ROOT, safe)
            self._send_file(full, 'image/png')
            return

        self.send_error(404)

    def do_POST(self):
        if self.path != '/api/generate':
            self.send_error(404)
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            body = self.rfile.read(length)
            payload = json.loads(body.decode('utf-8'))
        except Exception:
            self.send_error(400, 'Invalid JSON')
            return

        url = (payload.get('url') or '').strip()
        if not url:
            self.send_error(400, 'url is required')
            return

        color_name = (payload.get('color') or '').strip().lower()
        # Safe dark palette to preserve scanability
        palette = {
            'black': (0, 0, 0),
            'charcoal': (33, 33, 33),
            'navy': (15, 23, 42),
            'indigo': (49, 46, 129),
            'blue': (23, 37, 84),
            'emerald': (6, 95, 70),
            'red': (127, 29, 29),
            'purple': (88, 28, 135),
        }
        fg = palette.get(color_name, (0, 0, 0))

        filename = f"qr_{uuid.uuid4().hex}.png"
        out_path = os.path.join(ROOT, 'generated', filename)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        try:
            generate_qrcode(data=url, filename=out_path, fg_color=fg, bg_color=(255, 255, 255))
        except Exception as e:
            self.send_error(500, str(e))
            return

        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps({'success': True, 'qr_url': f"/generated/{filename}"}).encode('utf-8'))


def run(port=5000):
    server_address = ('', port)
    HTTPServer.allow_reuse_address = True
    httpd = HTTPServer(server_address, QRHandler)
    print(f"Starting server on port {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    run()
