"""Zero-dependency local API and static-file server. Run: python server.py"""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import json
import os
from engine import analyze

ROOT = Path(__file__).resolve().parent

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ('/', '/index.html'):
            self.send_error(404)
            return
        body = (ROOT / 'index.html').read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != '/api/analyze':
            self.send_error(404)
            return
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if size <= 0 or size > 200_000:
                raise ValueError('Otillåten indatastorlek.')
            payload = json.loads(self.rfile.read(size))
            output = analyze(payload)
            status = 200
        except (ValueError, json.JSONDecodeError) as exc:
            output = {'error': str(exc)}
            status = 400
        body = json.dumps(output, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '8765'))
    host = '0.0.0.0' if os.environ.get('PORT') else '127.0.0.1'
    print(f'Lyssnar på http://{host}:{port}')
    ThreadingHTTPServer((host, port), Handler).serve_forever()
