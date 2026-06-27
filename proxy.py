"""
StoreOps - 네이버 API 프록시 서버
실행: python proxy.py
접속: http://localhost:8080/app.html
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.request, json, os

NAVER_CLIENT_ID     = "6BwAsws_xLfrSAbq2O_4"
NAVER_CLIENT_SECRET = "dRToUtjNC3"

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/naver/book"):
            query = self.path.split("?q=")[-1]
            url = f"https://openapi.naver.com/v1/search/book.json?query={query}&display=10"
            req = urllib.request.Request(url, headers={
                "X-Naver-Client-Id":     NAVER_CLIENT_ID,
                "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
            })
            try:
                with urllib.request.urlopen(req) as res:
                    data = res.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(data)
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
        else:
            TYPES = {
                '.html': 'text/html; charset=utf-8',
                '.js':   'application/javascript; charset=utf-8',
                '.json': 'application/json; charset=utf-8',
                '.png':  'image/png',
                '.ico':  'image/x-icon',
            }
            path = self.path.split('?')[0].lstrip('/') or 'app.html'
            ext  = os.path.splitext(path)[1].lower()
            ctype = TYPES.get(ext, 'application/octet-stream')
            try:
                with open(path, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', ctype)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()

    def log_message(self, fmt, *args):
        print(f"  {args[0]} {args[1]}")

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("=" * 45)
print("  StoreOps 프록시 서버 시작")
print("  http://localhost:8080/app.html 열기")
print("  종료: Ctrl+C")
print("=" * 45)
HTTPServer(("", 8080), Handler).serve_forever()
