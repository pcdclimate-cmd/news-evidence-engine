"""Web server for the interactive map and existing evidence analysis."""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit, parse_qs
import json
import os
from engine import analyze
from news_data import COUNTRIES, country_news
ROOT=Path(__file__).resolve().parent
class Handler(BaseHTTPRequestHandler):
    def send_json(self,obj,status=200):
        body=json.dumps(obj,ensure_ascii=False).encode()
        self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
    def do_GET(self):
        parts=urlsplit(self.path);p=parts.path
        if p=='/api/health':return self.send_json({'status':'ok','version':'2.0-map-demo'})
        if p=='/api/countries':return self.send_json([{'code':k,'name':v[0],'english_name':v[1],'demo_count':2} for k,v in COUNTRIES.items()])
        if p=='/api/news':
            code=parse_qs(parts.query).get('country',[''])[0].upper()
            if len(code)!=2 or not code.isalpha():return self.send_json({'error':'Ange landskod med två bokstäver.'},400)
            return self.send_json(country_news(code))
        pages={'/':'index.html','/index.html':'index.html','/granska':'granska.html','/granska.html':'granska.html'}
        if p not in pages:self.send_error(404);return
        body=(ROOT/pages[p]).read_bytes()
        self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
    def do_POST(self):
        if urlsplit(self.path).path!='/api/analyze':self.send_error(404);return
        try:
            size=int(self.headers.get('Content-Length','0'))
            if size<=0 or size>200_000:raise ValueError('Otillåten indatastorlek.')
            payload=json.loads(self.rfile.read(size));output=analyze(payload)
        except (ValueError,TypeError,KeyError) as exc:return self.send_json({'error':str(exc)},400)
        self.send_json(output)
if __name__=='__main__':
    port=int(os.environ.get('PORT','8765'));host='0.0.0.0' if os.environ.get('PORT') else '127.0.0.1'
    print(f'News from Facts listening on http://{host}:{port}',flush=True)
    ThreadingHTTPServer((host,port),Handler).serve_forever()
